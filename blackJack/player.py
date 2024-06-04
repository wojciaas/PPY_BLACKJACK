from deck import Card
from blackjack_errors import InsufficientFundsError, BustedError


class Player:
    HIT_THRESHOLD = 21
    BANK = 100

    def __init__(self, name: str, bank: int = BANK):
        """Initializes the player with a name, a hand, and a score.
        :param name: The name of the player.
        """
        self.name = name
        self.hand = list()
        self.bank = bank
        self.current_bet = 0
        self.card_points = 0

    def __str__(self) -> str:
        """
        This method will return the name of the player.
        :return: The name of the player.
        """
        return self.name

    def make_bet(self, amount: int) -> int:
        """
        This method will take an amount and subtract it from the player's bank.
        :param amount: The amount to bet.
        :return: The player's bank after the bet.
        """
        if amount > self.bank:
            raise InsufficientFundsError(self.name)
        self.current_bet = amount
        self.bank -= amount
        return self.bank

    def hit(self, deck: list[Card]):
        """
        This method will add a card to the player's hand.
        :param deck: The deck of cards to draw from.
        """
        card = deck.pop()
        self.hand.append(card)
        self.card_points += card.card_value
        if card.value is 'A' and self.card_points > Player.HIT_THRESHOLD:
            self.card_points -= 10
        if self.card_points > Player.HIT_THRESHOLD:
            raise BustedError(self.name)

    def reset_hand(self):
        """This method will reset the player's hand and points."""
        self.hand.clear()
        self.card_points = 0


class Dealer(Player):
    NAME = "Jimmy the dealer"
    HIT_THRESHOLD = 17

    def __init__(self):
        """Initializes the dealer with a name, a hand, and a score."""
        super().__init__(self.NAME)

    def hit(self, deck: list[Card]):
        while self.card_points <= Dealer.HIT_THRESHOLD:
            try:
                super().hit(deck)
            except BustedError:
                return

    def parent_hit(self, deck: list[Card]):
        super().hit(deck)

    def get_points_hidden(self) -> int:
        """
        This method will return the points of the dealer's hand with the first card hidden.
        :return: The points of the dealer's hand with the first card hidden.
        """
        return self.hand[1].card_value
