from deck import Deck
from player import Player, Dealer
from blackjack_errors import BustedError, InsufficientFundsError
from colorama import Fore, Style


class BlackjackGame:
    def __init__(self):
        """Initializes the game with a deck of cards, a player, and a dealer."""
        self.decs_amount = None
        self.deck = None
        self.dealer = None
        self.players = list()
        self.players_out = list()

    def add_player(self, player_name: str):
        """
        This method will add a player to the game.
        :param player_name: The name of the player to add.
        """
        self.players.append(Player(player_name))

    def remove_player(self, player: Player):
        self.players_out.append(player)
        self.players.remove(player)

    def get_player(self):
        """This method will return the players that are still in the game."""
        for player in self.players:
            yield player

    def start_game(self, decs_amount: int):
        """
        This method will start the game by creating a deck.
        :param decs_amount: The number of decks to use in the game.
        """
        self.decs_amount = decs_amount
        self.deck = Deck(self.decs_amount)
        self.deck.shuffle()
        self.dealer = Dealer()

    def initialize_round(self):
        """This method will initialize the round by dealing cards to the players and the dealer."""
        for _ in range(2):
            for player in self.players:
                player.hit(self.deck.cards)
            self.dealer.parent_hit(self.deck.cards)

    def end_round(self):
        """This method will end the round by resetting the players' hands and the dealer's hand."""
        for player in self.players:
            player.reset_hand()
        self.dealer.reset_hand()
        self.deck.build_deck(self.decs_amount)
        self.deck.shuffle()

    def hit(self, player: Player) -> str | None:
        """This method will hit the player with a card."""
        try:
            player.hit(self.deck.cards)
        except BustedError as e:
            self.remove_player(player)
            return e.message

    def make_bet(self, player: Player, amount: int) -> str | None:
        """This method will take a bet from the player."""
        try:
            player.make_bet(amount)
        except InsufficientFundsError as e:
            return e.message

    def determine_winner(self, player: Player) -> str:
        """This method will determine the winner of the round."""
        dealer_points = self.dealer.card_points
        player_points = player.card_points
        if dealer_points > Player.HIT_THRESHOLD or player_points > dealer_points:
            player.bank += player.current_bet * 2
            player.current_bet = 0
            return f"{Fore.GREEN}{player.name} has won!{Style.RESET_ALL}"
        elif player_points == dealer_points:
            player.bank += player.current_bet
            player.current_bet = 0
            return f"{Fore.CYAN}{player.name} has tied with the dealer!{Style.RESET_ALL}"
        else:
            response = f"{player.name} has lost to the dealer!"
            player.current_bet = 0
            if player.bank == 0:
                self.players_out.append(player)
                self.players.remove(player)
                response += f"\n{player.name} is out of the game!"
            return f'{Fore.RED}{response}{Style.RESET_ALL}'

    def dealer_turn(self):
        self.dealer.hit(self.deck.cards)

    def show_results(self) -> list[Player]:
        return sorted(self.players_out, key=lambda x: x.bank, reverse=True)
