# Pub/Sub Broker — Design Rationale & Code Walkthrough

> Companion to the implementation. Part 1 = the decisions in Q&A form (rejected approach → its problem → what we chose).
> Part 2 = a line-of-reasoning walkthrough of the actual code: why each piece exists and what it solves.
> Part 3 = the concurrency correctness argument (interview gold). Part 4 = honest limitations.

---

## 0. Review verdict (TL;DR)

| Area | Status |
|------|--------|
| Ownership model (Broker routes, Topic owns) | ✅ correct |
| Async delivery via per-subscriber bounded queue | ✅ correct |
| Snapshot fan-out (no mutation-during-iteration) | ✅ correct |
| Serial executor: claim + bounded batch + re-arm | ✅ **correct** (interleavings check out) |
| Claim released on exception (`finally`) | ✅ correct |
| Backpressure (`put_nowait` + policy, never blocks publisher) | ✅ correct |
| **`Broker._name_to_topic` thread-safety** | 🟠 **bug — unguarded check-then-act** |
| `DropOldest.on_full` compound get→put | 🟡 non-atomic (minor, document) |
| `unsubscribe` takes redundant `topic_name` | 🟡 minor |
| Some missing type hints (`pool`) | 🟡 minor |

---

# PART 1 — Design decisions (Q&A)

### Q1. Who holds the list of subscribers — the Publisher, the Broker, or the Topic?
- **Rejected — Broker holds a flat `{topic: [subscribers]}`.** *Problem:* the Broker becomes a god-object with one hot lock; every publish to any topic contends on the same structure.
- **Chosen — the Topic holds its own subscriptions; the Broker only holds `{name: Topic}` and routes.**
- **Why:** per-topic lock granularity → publishing to `orders` never contends with `payments`. Independent contention domains. *Same reason you shard.*

### Q2. When a publisher publishes and a subscriber is slow, should the publisher wait?
- **Rejected — synchronous fan-out** (publisher calls `on_message` directly in a loop). *Problem:* head-of-line blocking — one slow subscriber stalls the publisher **and every other subscriber**; one throwing subscriber breaks `publish` for everyone.
- **Rejected — "just add a DLQ."** *Problem:* a DLQ is for *failing/poison* messages, not *slow* ones. Dead-lettering a slow subscriber's messages loses data it would have processed. **Slow ≠ failing.**
- **Chosen — asynchronous delivery via a per-subscriber queue.** The publisher enqueues and returns; each subscriber drains at its own pace.
- **Why:** decouples publisher latency from consumer speed; isolates a slow/failing subscriber to itself.

### Q3. What entity sits between a Subscriber and a Topic and holds the pending messages?
- **Rejected — "a buffer / storage."** *Problem:* that names the *field*, not the *thing*. A buffer is data; the relationship is the entity.
- **Chosen — a `Subscription`** binding `subscriber + topic + queue + claim`.
- **Why:** the message can't live on the Topic (shared, but each subscriber consumes at a different pace), so the holding place is per-(subscriber, topic). Name the relationship.

### Q4. A subscriber unsubscribes while the broker is iterating the topic's list to fan out. What happens?
- **Rejected — iterate the live list.** *Problem:* mutation-during-iteration → in Python, `RuntimeError: list changed size during iteration` (or silently skipped delivery).
- **Rejected — hold the topic lock for the whole fan-out loop.** *Problem:* subscribe/unsubscribe blocks until delivery ends; worse, if an `enqueue` ever blocked while holding the lock, one subscriber freezes the whole topic.
- **Chosen — snapshot under a brief lock, release, iterate the copy.**
- **Why:** delivery runs lock-free. Accepted semantic: a just-unsubscribed subscriber may get **one trailing message** (it was in the snapshot) — *correct, not a bug.* Membership is eventually consistent.

### Q5. Do you ever hold the lock across the enqueue / delivery?
- **Rejected — yes.** *Problem:* a blocking put while holding the topic lock freezes all publish/subscribe on that topic over one slow consumer.
- **Chosen — no.** Snapshot under the lock; enqueue/dispatch outside it.
- **Keeper:** *Holding the topic lock across a blocking put lets one slow subscriber freeze the whole topic.*

### Q6. Who drains the per-subscriber queues — one thread each, or a shared pool?
- **Rejected — one thread per subscription.** *Problem:* dies at thousands of subscriptions (≈1 MB stack each, context-switch storm).
- **Chosen — a shared `ThreadPoolExecutor`.**
- **Why:** a small pool multiplexes across many subscriptions.

### Q7. With a shared pool, how do you keep per-subscriber ordering?
- **Rejected — lock the queue across `take + on_message`.** *Problem:* that serializes the subscription to one thread at a time — i.e. recreates thread-per-subscription **plus** lock contention. Worst of both.
- **Rejected — pin each subscription to a worker via `hash(S) % N`.** *Problem:* one slow subscriber starves every other subscription pinned to the same worker (relocated head-of-line blocking).
- **Chosen — a non-blocking *claim* + bounded batch.** Any free pool thread may drain a subscription, but a claim guarantees ≤ 1 thread per subscription at a time; each turn drains a bounded batch then yields.
- **Keeper:** *Decouple "which thread runs it" (any free worker) from "how many run it at once" (≤ 1). Serialize by claiming, not by blocking.*

### Q8. The bounded batch — what is it, really?
- It's **cooperative round-robin**: `BATCH_SIZE` is the scheduler quantum. Big batch → throughput, less fairness; small batch → fairness, more overhead.
- **Limitation (cooperative, not preemptive):** a single `on_message` that *blocks forever* wedges the worker inside the batch — round-robin can't preempt it. Defense (v2): a timeout → treat a stuck handler as *failing*.

### Q9. The per-subscriber queue is unbounded — what breaks, and what's the policy when it fills?
- **Rejected — unbounded queue.** *Problem:* a permanently-slow subscriber grows it forever → OOM → whole broker down.
- **Rejected — block the publisher when full.** *Problem:* re-introduces the original coupling (publisher waits on the slow consumer). *In a fan-out you never block on one consumer.*
- **Chosen — bounded queue + an `OverflowPolicy` (default drop-oldest).** `put_nowait`; on `Full`, the policy decides.
- **Two axes:** *decoupling* (does the publisher wait? — only "block") vs *completeness* (is data lost? — drop policies). Block is the trap dressed as the safe default. **Backpressure policy is a function of topology.**

### Q10. (Out of scope, know the boundary) How would you keep order if a message could arrive via a slow durable spill?
- **Answer:** make order intrinsic to the message — a **per-topic offset** — and resequence on the consumer (Kafka's model). *We deliberately did NOT build this* (it's HLD): in-memory, ordering is held by the FIFO queue + single drainer, so the offset isn't needed yet.

---

# PART 2 — Code walkthrough (why each piece exists)

### `message.py`
```python
@dataclass(frozen=True)
class Message:
    payload: Any
    topic_name: str
    timestamp: datetime
```
- **`frozen=True`** → immutable. *Problem it solves:* the same Message object is fanned out to many subscriber queues across threads. If it were mutable, one subscriber could mutate a message another is about to read → a data race with no lock. Immutability makes sharing safe by construction.
- **No `offset`** → correct for the in-memory scope (ordering comes from the queue, not the offset; see Q10).

### `subscriber.py`
```python
class Subscriber(ABC):
    @abstractmethod
    def on_message(self, message: Message) -> None: ...
```
- **ABC interface.** *Problem it solves:* the Broker/Subscription depend on the *abstraction*, never a concrete subscriber (DIP). New subscriber types plug in with zero changes to the broker. It's the system's one extension point.

### `overflow_policy.py`
```python
class OverflowPolicy(ABC):
    def on_full(self, q, message) -> None: ...

class DropOldest(OverflowPolicy):   # evict head, then put newest
class DropNewest(OverflowPolicy):   # do nothing → reject incoming
```
- **Strategy pattern.** *Problem it solves:* the *full-queue behavior* is a policy that should change without touching the queue or the Subscription (Open/Closed). Swap `DropOldest` ↔ `DropNewest` ↔ a future `Block`/`Spill` with no other edits.
- **`DropNewest.on_full` = `pass`** is correct: when full, rejecting the incoming (newest) message *is* the behavior. ✅
- ⚠️ **`DropOldest` caveat:** `get_nowait()` then `put_nowait()` are two separate atomic ops. Under multiple concurrent producers, another producer can fill the freed slot between them, so the `put_nowait` hits `Full` and the *new* message is dropped instead. Acceptable for an in-memory toy; **document it**, don't pretend it's atomic.

### `subscription.py` — the heart
```python
self._claim = threading.Lock()
self._queue = queue.Queue(maxsize=capacity)
self._policy = policy or DropOldest()
```
- **`queue.Queue(maxsize=capacity)`** → thread-safe *and* bounded in one object. Solves both producer/consumer safety and the OOM/backpressure problem.
- **`_claim = threading.Lock()`** → the "≤ 1 drainer" token. Critically **`Lock`, not `RLock`**: the claim is acquired by one thread (the producer's `try_dispatch` or a re-arm) and **released by a different thread** (the pool worker running `_drain_batch`). `threading.Lock` allows cross-thread release; `RLock` is owner-bound and would raise. *Using `Lock` here is load-bearing, not incidental.*

```python
def enqueue(self, message):
    try: self._queue.put_nowait(message)
    except queue.Full: self._policy.on_full(self._queue, message)
```
- **`put_nowait` (never blocks)** → the publisher thread never waits on a full subscriber. Solves Q9's coupling problem. On `Full`, defer to the policy.

```python
def try_dispatch(self, pool):
    if self._claim.acquire(blocking=False):
        pool.submit(self._drain_batch, pool)
```
- **`acquire(blocking=False)` = the CAS-claim.** Only the thread that wins the claim schedules a drain → guarantees no second drainer is started. If the claim is already held, do nothing (the current drainer will re-arm). Solves "two threads draining one subscription → ordering shatters."

```python
def _drain_batch(self, pool):
    try:
        for _ in range(BATCH_SIZE):
            try: message = self._queue.get_nowait()
            except queue.Empty: break
            try: self._subscriber.on_message(message)
            except Exception as e: print(...)
    finally:
        self._claim.release()
    if not self._queue.empty() and self._claim.acquire(blocking=False):
        pool.submit(self._drain_batch, pool)
```
- **Bounded `for _ in range(BATCH_SIZE)`** → cooperative yield (Q8). The subscription processes at most N messages, then releases, so it can't monopolize a worker and starve other subscriptions.
- **`try/except` around `on_message`** → a *throwing* subscriber doesn't kill the drain loop. Combined with `finally: release()`, a failing handler **never leaks the claim** (which would permanently wedge that subscription). Solves the "failing subscriber" half of slow-vs-failing.
- **`finally: release()`** → the claim is freed on *every* path (normal, break, exception).
- **The re-arm (`if not empty and acquire: resubmit`)** → solves the **lost-wakeup** problem: a message enqueued during this batch isn't stranded. (Why it's airtight is in Part 3.)

### `topic.py`
```python
def add_subscriber/remove_subscriber:  with self._lock: ...
def fan_out(self, message, pool):
    with self._lock:
        snapshot = list(self._subscriptions)
    for subscription in snapshot:
        subscription.enqueue(message)
        subscription.try_dispatch(pool)
```
- **Mutations under `_lock`** → membership changes are serialized.
- **`snapshot = list(...)` inside the lock, iterate outside** → no mutation-during-iteration (Q4), and the lock is held only for the copy, never across enqueue/dispatch (Q5).
- **`enqueue` then `try_dispatch` per subscription** → the producer both delivers the message *and* nudges the drainer. This ordering is exactly what makes the re-arm airtight (Part 3).

### `broker.py`
- **Facade + router.** `publish` looks up the Topic and delegates `fan_out`; `subscribe` builds the `Subscription` and registers it; `unsubscribe` removes it.
- 🟠 **Bug:** `_name_to_topic` is a plain dict mutated/read across `create_topic`/`subscribe`/`publish` with **no lock**. `create_topic`'s `if name in ...: raise; ... [name] = topic` is check-then-act → two concurrent creators can both pass the check. *Fix direction:* guard topic-map access (a `Lock`), or fold create-if-absent into a single atomic step. The GIL does **not** make a check-then-act sequence atomic.

---

# PART 3 — Why the serial executor is correct (the interview answer)

Two invariants must hold: **(A) never two drainers for one subscription**, and **(B) a queued message is never stranded** (always a drainer running or scheduled).

**(A) Single drainer.** Every entry to `_drain_batch` is gated by a successful `acquire(blocking=False)` (in `try_dispatch` or the re-arm). A `Lock` admits exactly one holder, so at most one `_drain_batch` runs at a time. The brief window between `release()` and the re-arm `acquire()` doesn't permit two drainers — whoever acquires next becomes *the* single drainer.

**(B) No lost wakeup.** The producer always runs `enqueue(m)` **then** `try_dispatch`. Case-split on the message `m`:
- If `m` is enqueued *before* the drainer's `release()`: the drainer's re-arm sees `not empty` → re-acquires → resubmits. ✅
- If `m` is enqueued *after* `release()`: the claim is free, so the producer's own `try_dispatch` acquires it → schedules a drain. ✅
- If `m` is enqueued *after* the re-arm's empty-check but the claim is free: same as above — the producer's `try_dispatch` catches it. ✅

The producer's post-enqueue `try_dispatch` is the safety net that closes every gap the drainer's re-arm might miss. That's why both halves (worker re-arm **and** producer dispatch) are required.

---

# PART 4 — Current limitations & fix list

| # | Item | Severity | Fix direction |
|---|------|----------|---------------|
| 1 | `Broker._name_to_topic` unguarded (check-then-act) | 🟠 | Lock around topic-map access, or atomic create-if-absent |
| 2 | `DropOldest` get→put not atomic under many producers | 🟡 | Accept + document, or guard the evict+put as one critical section |
| 3 | `unsubscribe(topic_name, subscription)` passes topic redundantly | 🟡 | Derive topic from `subscription._topic`; drop the param |
| 4 | Missing type hints (`fan_out`'s `pool`, etc.) | 🟡 | Annotate `pool: ThreadPoolExecutor` |
| 5 | Blocking `on_message` wedges a worker (cooperative) | ⚪ v2 | Timeout around `on_message` → quarantine as *failing* |
| 6 | No publisher-visible backpressure signal (silent drop) | ⚪ v2 | Expose queue-depth/lag metrics |

**Out of scope (HLD, intentional):** offsets/resequencer, durable spillover, distributed/per-partition ordering, ack/retry semantics.

---

## Meta-theme
> **You don't eliminate head-of-line blocking — you choose where it lives and shrink its blast radius.**
> sync publish → per-sub queues → snapshot fan-out → serial executor → bounded queue: each step traded a wider blast radius for a narrower one.