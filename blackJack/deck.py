import random


class Card:
    SYMBOLS = {
        'Hearts': '\u2665',  # '♥'
        'Diamonds': '\u2666',  # '♦'
        'Clubs': '\u2663',  # '♣'
        'Spades': '\u2660'  # '♠'
    }
    VALUES = {
        'J': 10,
        'Q': 10,
        'K': 10,
        'A': 11
    }

    CARD = """\
    ┌─────────┐
    │{}       │
    │         │
    │         │
    │    {}   │
    │         │
    │         │
    │       {}│
    └─────────┘
    """.format('{rank: <2}', '{suit: <2}', '{rank: >2}')

    HIDDEN_CARD = """\
    ┌─────────┐
    │░░░░░░░░░│
    │░░░░░░░░░│
    │░░░░░░░░░│
    │░░░░░░░░░│
    │░░░░░░░░░│
    │░░░░░░░░░│
    │░░░░░░░░░│
    └─────────┘
    """

    def __init__(self, value: str, suit: str):
        self.value = value
        self.suit = suit
        self.card_value = self.__get_card_value()

    def __get_card_value(self) -> int:
        """
        This method will return the value of the card.
        :return: The value of the card.
        """
        value = self.VALUES.get(self.value)
        return value if value is not None else int(self.value)

    def __str__(self) -> str:
        """
        This method will return the string representation of the card.
        :return: The string representation of the card.
        """
        return f'{self.value}{self.SYMBOLS[self.suit]}'


class Deck:
    SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    VALUES = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def __init__(self, decks_amount: int = 1):
        """
        Initializes the deck with a list of cards and the number of decks.
        :param decks_amount: The number of decks to use.
        """
        self.cards = list()
        self.build_deck(decks_amount)

    def build_deck(self, decs_amount: int):
        """
        This method will build the deck of cards.
        :param decs_amount: The number of decks to use.
        """
        for _ in range(decs_amount):
            for suit in self.SUITS:
                for value in self.VALUES:
                    self.cards.append(Card(value, suit))

    def shuffle(self):
        """This method will shuffle the deck of cards."""
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        """
        This method will draw a card from the deck.
        :return: A card from the deck.
        """
        return self.cards.pop()
