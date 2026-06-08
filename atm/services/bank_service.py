from services.card_service import CardService
from services.account_service import AccountService
from models.account import Account
from models.card import Card


class BankService:
    card_service: CardService
    account_service: AccountService
    card_account_map: dict[str, Account]

    def __init__(self) -> None:
        self.card_account_map = {}
        self.account_service = AccountService()
        self.card_service = CardService()

    def link_card(self, card: Card, account: Account) -> None:
        self.card_account_map[card.card_number] = account
        self.card_service.add_card(card)

    def authenticate(self, card: Card, pin: str) -> bool:
        is_auth = self.card_service.verify_pin(card, pin)
        return is_auth

    def _get_account(self, card: Card) -> Account | None:
        return self.card_account_map.get(card.card_number)

    def get_balance(self, card: Card) -> float:
        account = self._get_account(card)
        if account is None:
            raise ValueError("Card is not linked to any account")
        balance = self.account_service.fetch_balance(account=account)
        return balance

    def withdraw(self, card: Card, amount: float) -> bool:
        account = self._get_account(card)
        if account is None:
            return False
        withdraw_success = self.account_service.process_debit(
            account=account, amount=amount
        )
        return withdraw_success

    def deposit(self, card: Card, amount: float) -> None:
        account = self._get_account(card)
        if account is None:
            return None
        self.account_service.process_credit(account=account, amount=amount)
