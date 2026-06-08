from models.card import Card
import hashlib

MAX_PIN_ATTEMPTS = 3


class CardService:
    card_repository: dict[str, Card]

    def __init__(self) -> None:
        self.card_repository = {}

    def add_card(self, card: Card) -> None:
        card_number = card.card_number
        if card_number not in self.card_repository:
            self.card_repository[card_number] = card

    def verify_pin(self, card: Card, entered_pin: str) -> bool:
        if card.is_blocked:
            return False

        entered_pin_hash = hashlib.sha256(entered_pin.encode()).hexdigest()
        if card.pin_hash == entered_pin_hash:
            return True

        self.increment_attempt(card)
        if card.pin_attempt_count >= MAX_PIN_ATTEMPTS:
            self.block_card(card)

        return False

    def block_card(self, card: Card) -> None:
        card.is_blocked = True

    def increment_attempt(self, card: Card) -> None:
        card.pin_attempt_count += 1

    def get_card(self, card_number: str) -> Card | None:
        if card_number in self.card_repository:
            return self.card_repository[card_number]
        else:
            return None
