from payment.payment_strategy import PaymentStrategy
from entities.seat import Seat


class PaymentService:
    _strategy: PaymentStrategy

    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def calculate_total(self, seats: list[Seat]) -> float:
        total = 0.0
        for seat in seats:
            total += seat.cost

        return total

    def process_payment(self, amount: float) -> bool:
        is_success = self._strategy.process_payment(amount)
        return is_success

    def initiate_refund(self, amount: float) -> bool:
        is_success = self._strategy.initiate_refund(amount)
        return is_success
