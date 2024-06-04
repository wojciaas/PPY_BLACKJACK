import os
import pickle
from game import BlackjackGame


def load_game() -> BlackjackGame | None:
    try:
        with open('game_continuation.pkl', 'rb') as save:
            return pickle.load(save)
    except FileNotFoundError:
        return None


def delete_game():
    if os.path.exists('game_continuation.pkl'):
        os.remove('game_continuation.pkl')


def save_game(game: BlackjackGame):
    with open('game_continuation.pkl', 'wb') as save:
        pickle.dump(game, save)


def read_rules(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise "Rules file not found."
