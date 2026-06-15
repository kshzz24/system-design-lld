"""
main.py - end-to-end demonstration & test harness for the in-memory Pub/Sub broker.

Each test maps to a version / invariant from the build charter (pubsub.md):

    TEST 1   basic fan-out, in order              (v1)
    TEST 2   topic routing / isolation            (v1 - Broker routes by topic)
    TEST 3   slow subscriber does not block        (v2 - async per-sub queues)
    TEST 4   per-sub ordering at scale            (v3 - shared pool + claim)
    TEST 5   single-drainer guarantee             (v3 - the claim)
    TEST 6   concurrent publishers, no loss       (v3 - re-arm closes lost-wakeup)
    TEST 7   worker survives a bad on_message     (v2 - exception safety)
    TEST 8   unsubscribe stops delivery
    TEST 9   concurrent sub/unsub never raises    (v2 - snapshot fan-out)
    TEST 10  bounded queue + drop-oldest          (v4 - backpressure)
    TEST 11  drop-newest policy swap              (v4 - Strategy / Open-Closed)
    TEST 12  publishing to an unknown topic raises

Run:  python main.py
"""
from __future__ import annotations

import threading
import time
from datetime import datetime

from broker import Broker
from subscriber import Subscriber
from message import Message
from overflow_policy import DropNewest


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def publish(broker: Broker, topic_name: str, payload: object) -> None:
    """Build a stamped Message and hand it to the broker."""
    broker.publish(topic_name, Message(payload, topic_name, datetime.now()))


def wait_until(predicate, timeout: float = 3.0, interval: float = 0.005) -> bool:
    """Poll until predicate() is true or timeout elapses (delivery is async)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


_results: list[tuple[str, bool]] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    _results.append((name, passed))
    status = "PASS" if passed else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"\n           {detail}"
    print(line)


# --------------------------------------------------------------------------- #
# subscriber test doubles
# --------------------------------------------------------------------------- #
class Collector(Subscriber):
    """Records every payload it receives, in order."""

    def __init__(self, name: str = "") -> None:
        self.name = name
        self.received: list = []

    def on_message(self, message: Message) -> None:
        self.received.append(message.payload)


class SlowCollector(Subscriber):
    """Simulates a subscriber that takes time to process each message."""

    def __init__(self, delay: float) -> None:
        self._delay = delay
        self.received: list = []

    def on_message(self, message: Message) -> None:
        time.sleep(self._delay)
        self.received.append(message.payload)


class Flaky(Subscriber):
    """Raises on one specific payload - used to prove the worker survives it."""

    def __init__(self, fail_on: object) -> None:
        self._fail_on = fail_on
        self.received: list = []

    def on_message(self, message: Message) -> None:
        if message.payload == self._fail_on:
            raise RuntimeError(f"intentional failure on {message.payload}")
        self.received.append(message.payload)


class ConcurrencyProbe(Subscriber):
    """Flags if two threads are ever inside on_message at the same time."""

    def __init__(self) -> None:
        self.received: list = []
        self.violations = 0
        self._inside = False

    def on_message(self, message: Message) -> None:
        if self._inside:                 # another thread is already draining this sub
            self.violations += 1
        self._inside = True
        time.sleep(0.0005)               # widen any concurrency window
        self.received.append(message.payload)
        self._inside = False


# --------------------------------------------------------------------------- #
# TEST 1 - basic fan-out, in order (v1)
# --------------------------------------------------------------------------- #
def test_basic_fan_out() -> None:
    b = Broker()
    b.create_topic("news")
    a, c = Collector("A"), Collector("B")
    b.subscribe("news", a)
    b.subscribe("news", c)

    for i in range(3):
        publish(b, "news", i)

    ok = wait_until(lambda: a.received == [0, 1, 2] and c.received == [0, 1, 2])
    check("v1 basic fan-out: 2 subs receive all 3, in order", ok,
          f"A={a.received}  B={c.received}")


# --------------------------------------------------------------------------- #
# TEST 2 - topic routing / isolation (v1)
# --------------------------------------------------------------------------- #
def test_topic_isolation() -> None:
    b = Broker()
    b.create_topic("sports")
    b.create_topic("tech")
    sports, tech = Collector(), Collector()
    b.subscribe("sports", sports)
    b.subscribe("tech", tech)

    publish(b, "sports", "goal")
    publish(b, "tech", "release")

    ok = wait_until(lambda: sports.received == ["goal"] and tech.received == ["release"])
    check("routing: each subscriber only receives its own topic", ok,
          f"sports={sports.received}  tech={tech.received}")


# --------------------------------------------------------------------------- #
# TEST 3 - slow subscriber does not block publisher or others (v2)
# --------------------------------------------------------------------------- #
def test_slow_does_not_block() -> None:
    b = Broker()
    b.create_topic("t")
    slow, fast = SlowCollector(0.3), Collector()
    b.subscribe("t", slow)
    b.subscribe("t", fast)

    t0 = time.time()
    for i in range(3):
        publish(b, "t", i)
    publish_time = time.time() - t0

    fast_ok = wait_until(lambda: fast.received == [0, 1, 2], timeout=1.0)
    slow_ok = wait_until(lambda: slow.received == [0, 1, 2], timeout=2.0)

    check("v2 publisher not blocked by slow subscriber", publish_time < 0.1,
          f"publish of 3 returned in {publish_time:.4f}s (slow sub sleeps 0.3s each)")
    check("v2 fast subscriber not delayed by slow peer", fast_ok, f"fast={fast.received}")
    check("v2 slow subscriber still gets all, in order", slow_ok, f"slow={slow.received}")


# --------------------------------------------------------------------------- #
# TEST 4 - per-sub ordering at scale (v3: 50 subs over a 4-thread pool)
# --------------------------------------------------------------------------- #
def test_ordering_at_scale() -> None:
    b = Broker()
    b.create_topic("t")
    subs = [Collector() for _ in range(50)]
    for s in subs:
        b.subscribe("t", s)

    for i in range(100):
        publish(b, "t", i)

    ok = wait_until(lambda: all(s.received == list(range(100)) for s in subs), timeout=5.0)
    check("v3 per-sub ordering holds with 50 subs over 4 shared threads", ok)


# --------------------------------------------------------------------------- #
# TEST 5 - single-drainer guarantee (v3: the claim)
# --------------------------------------------------------------------------- #
def test_single_drainer() -> None:
    b = Broker()
    b.create_topic("t")
    probe = ConcurrencyProbe()
    b.subscribe("t", probe)

    for i in range(60):
        publish(b, "t", i)

    wait_until(lambda: len(probe.received) == 60, timeout=3.0)
    ok = probe.violations == 0 and probe.received == list(range(60))
    check("v3 single-drainer: never two workers in one subscription", ok,
          f"violations={probe.violations}  count={len(probe.received)}")


# --------------------------------------------------------------------------- #
# TEST 6 - concurrent publishers, no stranded / duplicated (v3: re-arm)
# --------------------------------------------------------------------------- #
def test_concurrent_publishers() -> None:
    b = Broker()
    b.create_topic("t")
    sink = Collector()
    # capacity comfortably exceeds the 2000-message burst, so nothing is dropped:
    # this isolates re-arm correctness (no stranded / duplicated) from v4 backpressure.
    b.subscribe("t", sink, capacity=4000)

    def pub(tag: int) -> None:
        for i in range(500):
            publish(b, "t", (tag, i))

    threads = [threading.Thread(target=pub, args=(k,)) for k in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    ok = wait_until(lambda: len(sink.received) == 2000, timeout=5.0)
    no_duplicates = len(sink.received) == len(set(sink.received))
    check("v3 4 concurrent publishers: every message delivered exactly once",
          ok and no_duplicates,
          f"delivered {len(sink.received)}/2000  duplicates={not no_duplicates}")


# --------------------------------------------------------------------------- #
# TEST 7 - worker survives a throwing on_message (v2: exception safety)
# --------------------------------------------------------------------------- #
def test_worker_survives_exception() -> None:
    b = Broker()
    b.create_topic("t")
    flaky = Flaky(fail_on=2)
    b.subscribe("t", flaky)

    for i in range(5):
        publish(b, "t", i)

    ok = wait_until(lambda: flaky.received == [0, 1, 3, 4], timeout=2.0)
    check("v2 worker survives a bad message and keeps draining", ok,
          f"received={flaky.received} (payload 2 raised, should be skipped)")


# --------------------------------------------------------------------------- #
# TEST 8 - unsubscribe stops delivery
# --------------------------------------------------------------------------- #
def test_unsubscribe() -> None:
    b = Broker()
    b.create_topic("t")
    c = Collector()
    handle = b.subscribe("t", c)

    publish(b, "t", "before")
    wait_until(lambda: c.received == ["before"])

    b.unsubscribe("t", handle)
    publish(b, "t", "after")
    time.sleep(0.2)

    check("unsubscribe stops further delivery", c.received == ["before"],
          f"received={c.received}")


# --------------------------------------------------------------------------- #
# TEST 9 - concurrent subscribe/unsubscribe during publish never raises (v2)
# --------------------------------------------------------------------------- #
def test_concurrent_membership() -> None:
    b = Broker()
    b.create_topic("t")
    b.subscribe("t", Collector())

    errors: list[str] = []
    stop = [False]

    def churn() -> None:
        try:
            while not stop[0]:
                h = b.subscribe("t", Collector())
                b.unsubscribe("t", h)
        except Exception as e:           # noqa: BLE001 - we want to catch ANY raise
            errors.append(repr(e))

    def pub() -> None:
        try:
            for i in range(3000):
                publish(b, "t", i)
        except Exception as e:           # noqa: BLE001
            errors.append(repr(e))

    ct = threading.Thread(target=churn)
    pt = threading.Thread(target=pub)
    ct.start()
    pt.start()
    pt.join()
    stop[0] = True
    ct.join()

    check("v2 concurrent sub/unsub during publishing never raises", not errors,
          f"errors={errors}")


# --------------------------------------------------------------------------- #
# TEST 10 - bounded queue + drop-oldest backpressure (v4)
# --------------------------------------------------------------------------- #
def test_backpressure_drop_oldest() -> None:
    b = Broker()
    b.create_topic("t")
    slow = SlowCollector(0.01)
    handle = b.subscribe("t", slow, capacity=5)     # default policy = DropOldest

    max_depth = [0]
    stop = [False]

    def sampler() -> None:
        # introspect the private queue depth purely for the demo
        while not stop[0]:
            max_depth[0] = max(max_depth[0], handle._queue.qsize())

    samp = threading.Thread(target=sampler, daemon=True)
    samp.start()

    t0 = time.time()
    for i in range(500):
        publish(b, "t", i)
    publish_time = time.time() - t0
    time.sleep(1.0)
    stop[0] = True

    check("v4 publisher never blocks under heavy overload", publish_time < 0.3,
          f"publish of 500 returned in {publish_time:.4f}s")
    check("v4 bounded memory: queue depth never exceeds C=5", max_depth[0] <= 5,
          f"max queue depth observed = {max_depth[0]}")
    check("v4 overflow is dropped (drop-oldest)", len(slow.received) < 500,
          f"delivered {len(slow.received)}/500")
    check("v4 drop-oldest keeps the newest (499 delivered)", 499 in slow.received)


# --------------------------------------------------------------------------- #
# TEST 11 - drop-newest policy swap (v4: Strategy / Open-Closed)
# --------------------------------------------------------------------------- #
def test_backpressure_drop_newest() -> None:
    b = Broker()
    b.create_topic("t")

    gate = threading.Event()

    class Gated(Subscriber):
        def __init__(self) -> None:
            self.received: list = []

        def on_message(self, message: Message) -> None:
            gate.wait()                  # hold the consumer so the queue fills
            self.received.append(message.payload)

    g = Gated()
    b.subscribe("t", g, capacity=3, policy=DropNewest())

    for i in range(20):
        publish(b, "t", i)
    time.sleep(0.2)                      # queue fills & overflows while gated
    gate.set()                          # release the consumer

    wait_until(lambda: 0 in g.received, timeout=2.0)
    kept_oldest = 0 in g.received
    dropped_newest = 19 not in g.received
    check("v4 drop-newest keeps the oldest, rejects incoming",
          kept_oldest and dropped_newest, f"received={sorted(g.received)}")


# --------------------------------------------------------------------------- #
# TEST 12 - unknown topic raises
# --------------------------------------------------------------------------- #
def test_unknown_topic_raises() -> None:
    b = Broker()
    raised = False
    try:
        publish(b, "ghost", "x")
    except ValueError:
        raised = True
    check("publishing to an unknown topic raises ValueError", raised)


# --------------------------------------------------------------------------- #
# runner
# --------------------------------------------------------------------------- #
def main() -> None:
    tests = [
        test_basic_fan_out,
        test_topic_isolation,
        test_slow_does_not_block,
        test_ordering_at_scale,
        test_single_drainer,
        test_concurrent_publishers,
        test_worker_survives_exception,
        test_unsubscribe,
        test_concurrent_membership,
        test_backpressure_drop_oldest,
        test_backpressure_drop_newest,
        test_unknown_topic_raises,
    ]

    print("=" * 64)
    print("  Pub/Sub Broker - end-to-end test harness")
    print("=" * 64)
    for t in tests:
        t()
    print("-" * 64)
    passed = sum(1 for _, ok in _results if ok)
    total = len(_results)
    verdict = "ALL GREEN" if passed == total else "SOME FAILURES"
    print(f"  {passed}/{total} checks passed   [{verdict}]")
    print("=" * 64)


if __name__ == "__main__":
    main()
