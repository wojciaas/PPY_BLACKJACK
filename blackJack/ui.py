from game import BlackjackGame
from colorama import Fore, Style
import tkinter as tk
import os
import file_manager as fm
from player import Player
from deck import Card


def cls():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


def join_lines(strings):
    """
    Joins multiple strings line by line.
    :param strings: The strings to join.
    :return: The joined strings.
    """
    lines = [string.splitlines() for string in strings]
    return '\n'.join(''.join(line) for line in zip(*lines))


def ascii_version_of_card(*cards):
    """
    Returns the ASCII representation of the card.
    :param cards: The card objects.
    :return: The ASCII representation of the card.
    """
    def card_to_string(card):
        return Card.CARD.format(rank=card.value, suit=Card.SYMBOLS.get(card.suit))

    return join_lines(map(card_to_string, cards))


def ascii_version_of_hidden_card(*cards):
    """
    Returns the ASCII representation of the hidden card.
    :param cards: The card objects.
    :return: The ASCII representation of the hidden card.
    """
    return join_lines((Card.HIDDEN_CARD, ascii_version_of_card(*cards[1:])))


def show_rules(path: str):
    try:
        rules = fm.read_rules(path)
        rules_window = tk.Tk()
        rules_window.title("Blackjack Rules")
        rules_window.resizable(False, False)

        text_widget = tk.Text(rules_window, height=20, width=60, wrap="word")
        text_widget.insert(tk.END, rules)
        text_widget.config(state=tk.DISABLED, font=("Courier", 18))
        text_widget.pack()

        close_button = tk.Button(rules_window, text="Close", command=rules_window.destroy)
        close_button.pack()

        rules_window.mainloop()
    except Exception as e:
        print(f"An error occurred while trying to show the rules: {e}")


class BlackjackUI:
    def __init__(self, logic: BlackjackGame):
        """
        Initializes the UI with the game logic.
        :param logic: The game logic.
        """
        self.logic = logic

    def run(self):
        choice = ""
        try:
            while choice != "3":
                cls()
                print(self.print_blackjack_logo())
                print("(1) Start Game")
                print("(2) Show rules")
                print("(3) Exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    self.__start_game()
                elif choice == "2":
                    show_rules("rules/blackjack_rules.txt")
                    cls()
                elif choice == "3":
                    print("Goodbye!")
                else:
                    print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nGoodbye!")

    def __start_game(self):
        cls()
        print(self.print_blackjack_logo())
        result = fm.load_game()
        if result is not None:
            choice = ''
            while choice != 'y' and choice != 'n':
                choice = input("A saved game was found. Do you want to continue? (y/n): ")
                match choice:
                    case 'y':
                        self.logic = result
                        self.__play_round(False)
                    case 'n':
                        fm.delete_game()
                    case _:
                        cls()
                        print(self.print_blackjack_logo())
                        print("Invalid choice. Please try again.")
        self.__init_new_game()
        self.__play_game()
        self.__show_results()

    def __init_new_game(self):
        cls()
        print(self.print_blackjack_logo())
        num_of_players = ''
        while not num_of_players.isdigit():
            num_of_players = input("Enter the number of players: ")
            if not num_of_players.isdigit():
                cls()
                print(self.print_blackjack_logo())
                print("Invalid input. Please enter a number.")
        for i in range(int(num_of_players)):
            player_name = input(f"Enter the name of player {i + 1}: ")
            self.logic.add_player(player_name)
        decs_amount = ''
        while not decs_amount.isdigit():
            decs_amount = input("Enter the number of decks to use: ")
            if not decs_amount.isdigit():
                cls()
                print(self.print_blackjack_logo())
                print("Invalid input. Please enter a number.")
        self.logic.start_game(int(decs_amount))

    def __play_game(self):
        try:
            while self.logic.players:
                self.__play_round()
                self.logic.end_round()
        except KeyboardInterrupt:
            fm.save_game(self.logic)

    def __play_round(self, is_new_round: bool = True):
        cls()
        if is_new_round:
            self.logic.initialize_round()
        player_gen = self.logic.get_player()
        player = next(player_gen, None)
        while player is not None:
            if self.__init_bet(player):
                player_gen = self.logic.get_player()
                player = next(player_gen, None)
                continue
            self.display_hands(True, player)
            action = input("\nDo you want to '(h) hit', '(s) stand' or '(c) chash out'? ").lower()
            if action == 'h':
                hit_res = self.logic.hit(player)
                if hit_res is not None:
                    self.display_hands(True, player)
                    print(hit_res)
                    input("Press any key to continue..")
                    player_gen = self.logic.get_player()
                    player = next(player_gen, None)
            elif action == 's':
                player = next(player_gen, None)
            elif action == 'c':
                self.logic.remove_player(player)
                player_gen = self.logic.get_player()
                player = next(player_gen, None)
            else:
                cls()
                self.display_hands(True, player)
                print("Invalid action. Please try again..")
        self.__show_winners()

    def __init_bet(self, player: Player) -> bool | None:
        if player.current_bet == 0:
            cls()
            print(self.print_blackjack_logo())
            choice = input(f"{player.name}'s bank: {player.bank}$\n(1) Bet\n(2) Cash out\nEnter your choice: ")
            while choice != '1' and choice != '2':
                cls()
                print(self.print_blackjack_logo())
                print("Invalid choice. Please try again.")
                choice = input(f"{player.name}'s bank: {player.bank}\n(1) Bet\n(2) Cash out\nEnter your choice: ")
            if choice == '1':
                bet = ''
                while not bet.isdigit():
                    cls()
                    print(self.print_blackjack_logo())
                    bet = input(f"{player.name}'s bank: {player.bank}\nHow much do you want to bet? ")
                    if not bet.isdigit() or int(bet) < 1:
                        cls()
                        print(self.print_blackjack_logo())
                        print("Invalid input. Please enter a valid amount.")
                bet_res = self.logic.make_bet(player, int(bet))
                if bet_res is not None:
                    cls()
                    print(self.print_blackjack_logo())
                    print(bet_res)
                    input("Press any key to bet again..")
            else:
                self.logic.remove_player(player)
                return True

    def display_hands(self, hide_dealer_first_card: bool, player: Player):
        cls()
        print(f"\n{self.logic.dealer.name}'s hand:")
        if hide_dealer_first_card:
            print(f'{ascii_version_of_hidden_card(*self.logic.dealer.hand)}'
                  f'\nValue: {self.logic.dealer.get_points_hidden()}')
        else:
            print(f'{ascii_version_of_card(*self.logic.dealer.hand)}\nValue: {self.logic.dealer.card_points}')
        print(f"\n{player.name}'s hand:\n")
        print(f"{ascii_version_of_card(*player.hand)}\nValue: {player.card_points}\nBank: {player.bank}$\n"
              f"Current bet: {player.current_bet}$")

    def __show_winners(self):
        cls()
        for player in self.logic.players:
            self.logic.dealer_turn()
            self.display_hands(False, player)
            print(self.logic.determine_winner(player))
            input("Press any key to continue..")

    def __show_results(self):
        cls()
        print(self.print_blackjack_logo())
        print("Results:")
        players = self.logic.show_results()
        for pair in enumerate(players, start=1):
            print(f"{pair[0]}. {pair[1].name}: {pair[1].bank - Player.BANK if pair[1].bank - Player.BANK > 0 else 0}$")
        input("Press any key to continue..")

    @staticmethod
    def print_blackjack_logo() -> str:
        """
        This method will return the blackjack logo.
        :return: The blackjack logo.
        """
        logo_black = f"""
                {Fore.BLACK}
                ██████╗ ██╗      █████╗  ██████╗██╗  ██╗
                ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝
                ██████╔╝██║     ███████║██║     █████╔╝ 
                ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ 
                ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗
                ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                {Style.RESET_ALL}
                """
        logo_red = f"""
                {Fore.RED}
                     ██╗ █████╗  ██████╗██╗  ██╗
                     ██║██╔══██╗██╔════╝██║ ██╔╝
                     ██║███████║██║     █████╔╝ 
                ██   ██║██╔══██║██║     ██╔═██╗ 
                ╚█████╔╝██║  ██║╚██████╗██║  ██╗
                 ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                {Style.RESET_ALL}
                """
        logo = f"{logo_black}{logo_red}"
        centered_logo = "\n".join(line.center(os.get_terminal_size().columns) for line in logo.splitlines())
        return centered_logo
