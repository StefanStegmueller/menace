import sys
from tqdm import tqdm
from pyfiglet import Figlet
from src.board_state import BoardState, Field, Result
from src.train_args import TrainArgs

__standard_error_text = "\n>>> Wrong Input. "


def print_startup():
    f = Figlet(font="slant")
    print(f.renderText("MENACE"))


def print_state(state: BoardState, train_args: TrainArgs):
    if not(train_args.train):
        print(state)


def get_train_args() -> TrainArgs:
    """Checks Cli-Args if train mode is set."""
    if len(sys.argv) >= 2:
        input_text = sys.argv[1]
        if __check_int(input_text):
            max_train_steps = int(input_text)
            pbar = tqdm(range(0, max_train_steps))
            train_args = TrainArgs(True, 0, max_train_steps, pbar)
            return train_args
        else:
            print(__standard_error_text +
                  "Training steps have to be an integer.")
            sys.exit()
    print("No train mode detected.")
    print("If you want to train the model use the amount of training steps as first argument.\n")
    return TrainArgs(False, 0, 0, None)


def ask_next_move(state: BoardState) -> int:
    """
    Asks player for the coordinates of the next move.
    Returns tuple (success: bool, index_next_move: int).
    """

    input_text = input(">>> Next move (xy):")

    if (not(__check_length(2, input_text))
        or not(__check_int(input_text[0]))
            or not(__check_int(input_text[1]))):
        return ask_next_move(state)

    x = int(input_text[0])
    y = int(input_text[1])

    if not __check_value_range(x) or not __check_value_range(y):
        return ask_next_move(state)

    index = state.coords_to_index(x, y)

    if not __check_unset_field(index, state):
        return ask_next_move(state)

    return index


def ask_continue_trainig(train_args: TrainArgs) -> (bool, TrainArgs):
    if train_args.train:
        if train_args.train_steps >= train_args.max_train_steps:
            def ask_continue() -> bool:
                input_text = input("Continue training?(y/n):")
                if (not(__check_length(1, input_text))
                        or not(__check_yes_no(input_text))):
                    return (True if input_text == "y" or input_text == "Y" else False)
                else:
                    return ask_continue()

            print("AI win rate: {}%".format(
                int(train_args.ai_wins / (train_args.train_steps / 100))))
            train_args.ai_wins = 0
            train_args.train = ask_continue()

    return train_args


def print_game_over(state: BoardState, winner: Result):
    print(state)
    game_over_text = "\n+++ GAME OVER: "

    if winner == Result.X_WINS:
        game_over_text += "X WINS"
    elif winner == Result.O_WINS:
        game_over_text += "O WINS"
    else:
        game_over_text += "DRAW"

    game_over_text += " +++\n"

    print(game_over_text)


def __check_length(n: int, input_text: str) -> bool:
    """Check if input is not longer than 2 characters."""
    if len(input_text) != n:
        print(__standard_error_text + "Input length has to be 2.\n")
        return False
    return True


def __check_int(input_text: str) -> bool:
    """Checks if input is an integer."""
    success = True
    if input_text[0] in ('-', '+'):
        success = input_text[1:].isdigit()
    else:
        success = input_text.isdigit()
    if not(success):
        print(__standard_error_text + "Input has to be integers.\n")
    return success


def __check_value_range(x: int) -> bool:
    """
    Checks if integer is in valid value range to
    be a coordinate for Tic-Tac-Toe.
    """
    if x < 1 or x > 3:
        print(__standard_error_text +
              "Coordinates have to be between 1 and 3.\n")
        return False
    return True


def __check_unset_field(index: int, state: BoardState) -> bool:
    """Check if input coordinates are for an unset field."""
    if state.get_field(index) != Field.NONE:
        print(__standard_error_text + "Field is already set.\n")
        return False
    return True


def __check_yes_no(input_text: str) -> bool:
    """Check if input is yes or no."""
    txt = input_text
    if txt != "y" and txt != "n" and txt != "Y" and txt != "N":
        print(__standard_error_text + "Please type \"y\" or \"n\".\n")
        return False
    return True
