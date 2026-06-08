from models.account import Account


class AccountService:

    def process_debit(self, account: Account, amount: float) -> bool:
        success = account.debit(amount=amount)
        return success

    def process_credit(self, account: Account, amount: float) -> None:
        account.credit(amount=amount)

    def fetch_balance(self, account: Account) -> float:
        balance: float = account.get_balance()
        return balance
