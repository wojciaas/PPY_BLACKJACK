from abc import ABC
from colorama import Fore, Style


class BlackjackError(ABC, Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(f'{Fore.RED}{self.message}{Style.RESET_ALL}')


class InsufficientFundsError(BlackjackError):
    """Exception raised when a player has insufficient funds."""

    def __init__(self, player_name):
        self.message = f"{player_name} has insufficient funds."
        super().__init__(self.message)


class BustedError(BlackjackError):
    """Exception raised when a player exceeds 21 points."""

    def __init__(self, player_name):
        self.message = f"{player_name} has busted."
        super().__init__(self.message)
