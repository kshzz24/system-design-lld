from payment.payment_strategy import PaymentStrategy


class DebitPayment(PaymentStrategy):

    def __init__(self, card_number: str, pin: str) -> None:
        self._card_number = card_number
        self._pin = pin

    def process_payment(self, amount: float) -> bool:
        print(f"Charging {amount} to debit card {self._card_number[-4:]}")
        return True

    def initiate_refund(self, amount: float) -> bool:
        print(f"Refunding {amount} to debit card {self._card_number[-4:]}")
        return True
