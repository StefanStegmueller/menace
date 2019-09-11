import sys
import random
from tqdm import tqdm
from src.board_state import Field, Result, BoardState
from src.model import Model


def coords_to_index(x: int, y: int) -> int:
    return ((x - 1) * 3 + y) - 1


def ask_next_move(state: BoardState) -> (bool, int):
    input_text = input("Next move (xy):")
    error_text = "Wrong Input."
    if len(input_text) != 2:
        print(error_text)
        return (False, 0)
    try:
        x = int(input_text[0])
        y = int(input_text[1])
    except:
        print(error_text)
        return (False, 0)
    if x < 1 or x > 3 or y < 1 or y > 3:
        print(error_text)
        return (False, 0)
    index = coords_to_index(x, y)
    if state.get_field(index) != Field.NONE:
        print(error_text)
        return (False, 0)
    return (True, index)


def ask_continue_trainig(train: bool, train_steps: int, ai_wins: int) -> (bool, int):
    if train:
        if train_steps >= 10000:
            print("AI win rate: {}%".format(int(ai_wins / (train_steps / 100))))
            input_text = input("Continue training?(y/n):")
            if input_text == "y":
                return (True, 0)
            else:
                return (False, 0)
        else:
            return (True, train_steps)
    return (False, train_steps)


def evalute_game(state: BoardState, model: Model, progress: [(BoardState, int)], train: int) -> (bool, BoardState, Result):
    winner = state.check_winner()

    if winner == Result.NONE:
        return (False, state, winner)

    if not(train):
        print(state)
        print("\n+++ GAME OVER +++\n")
    model.reward(progress, winner)
    return (True, BoardState(), winner)


def main():
    train = False
    if sys.argv[1] == "train":
        train = True

    current_state = BoardState()
    model = Model()
    ai_progress = []
    ai_wins = 0

    train_steps = 0
    pbar = tqdm(range(0, 10000))

    while True:

        # Display current state
        if not(train):
            print(current_state)

        # Ask player for next move or train
        if train:
            if train_steps == 0:
                pbar.reset()

            indices = [i for i in range(
                len(current_state.board)) if current_state.board[i] == Field.NONE]
            index = random.choice(indices)
            train_steps += 1
            pbar.update(1)
        else:
            res = ask_next_move(current_state)
            if res[0] is False:
                continue
            index = res[1]

        current_state = current_state.set_field(index, Field.X)
        (game_over, current_state, _) = evalute_game(
            current_state, model, ai_progress, train)
        if game_over:
            ai_progress = []
            (train, train_steps) = ask_continue_trainig(
                train, train_steps, ai_wins)
            continue

        # Pick ai move from discrete random distribution
        ai_move = model.pick_move(current_state)
        ai_progress.append((current_state, ai_move))

        current_state = current_state.set_field(ai_move, Field.O)
        (game_over, current_state, winner) = evalute_game(
            current_state, model, ai_progress, train)
        if game_over:
            if winner == Result.O_WINS:
                ai_wins += 1
            ai_progress = []
            (train, train_steps) = ask_continue_trainig(
                train, train_steps, ai_wins)


if __name__ == "__main__":
    main()
