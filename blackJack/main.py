from ui import BlackjackUI
from game import BlackjackGame


def main():
    game_logic = BlackjackGame()
    ui = BlackjackUI(game_logic)
    ui.run()


if __name__ == "__main__":
    main()
