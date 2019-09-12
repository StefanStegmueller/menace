from src.board_state import BoardState, Field


class UserInterface:

    def __init__(self):
        self.standard_error_text = "\nWrong Input. "

    def ask_next_move(self, state: BoardState) -> (bool, int):
        """
        Asks player for the coordinates of the next move.
        Returns tuple (success: bool, index_next_move: int).
        """

        input_text = input("Next move (xy):")

        if (not(self.__check_length(2, input_text))
            or not(self.__check_int(input_text[0]))
                or not(self.__check_int(input_text[1]))):
            return (False, 0)

        x = int(input_text[0])
        y = int(input_text[1])

        if not self.__check_value_range(x) or not self.__check_value_range(y):
            return (False, 0)

        index = state.coords_to_index(x, y)

        if not self.__check_unset_field(index, state):
            return (False, 0)

        return (True, index)

    def ask_continue_trainig(self, train: bool, train_steps: int, ai_wins: int) -> (bool, int):
        if train:
            if train_steps >= 10000:
                print("AI win rate: {}%".format(
                    int(ai_wins / (train_steps / 100))))
                input_text = input("Continue training?(y/n):")
                if input_text == "y":
                    return (True, 0)
                else:
                    return (False, 0)
            else:
                return (True, train_steps)
        return (False, train_steps)

    def __check_length(self, n: int, input_text: str) -> bool:
        """Check if input is not longer than 2 characters."""
        if len(input_text) != n:
            print(self.standard_error_text + "Input length has to be 2.\n")
            return False
        return True

    def __check_int(self, input_text: str) -> bool:
        """Checks if input is an integer."""
        success = True
        if input_text[0] in ('-', '+'):
            success = input_text[1:].isdigit()
        else:
            success = input_text.isdigit()
        if not(success):
            print(self.standard_error_text + "Input has to be integers.\n")
        return success

    def __check_value_range(self, x: int) -> bool:
        """
        Checks if integer is in valid value range to
        be a coordinate for Tic-Tac-Toe.
        """
        if x < 1 or x > 3:
            print(self.standard_error_text +
                  "Coordinates have to be between 1 and 3.\n")
            return False
        return True

    def __check_unset_field(self, index: int, state: BoardState) -> bool:
        """Check if input coordinates are for an unset field."""
        if state.get_field(index) != Field.NONE:
            print(self.standard_error_text + "Field is already set.\n")
            return False
        return True
