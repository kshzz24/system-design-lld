from payment.payment_strategy import PaymentStrategy


class UPIPayment(PaymentStrategy):

    def __init__(self, number: str, otp: str) -> None:
        self._number = number
        self._otp = otp

    def process_payment(self, amount: float) -> bool:
        print(f"Charging {amount} to Account linked to  {self._number}")
        return True

    def initiate_refund(self, amount: float) -> bool:
        print(f"Refunding {amount} to Account linked to {self._number}")
        return True
