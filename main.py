
import random
from tqdm import tqdm
import src.user_interface as ui
from src.train_args import TrainArgs
from src.board_state import Field, Result, BoardState
from src.model import Model


def evalute_game(state: BoardState,
                 model: Model,
                 progress: [(BoardState, int)],
                 train_args: TrainArgs) -> (bool, BoardState):
    winner = state.check_winner()

    if winner == Result.NONE:
        return (False, state)

    if winner == Result.O_WINS:
        train_args.ai_wins += 1
    elif winner == Result.X_WINS:
        train_args.trainer_wins += 1
    else:
        train_args.draws += 1

    if not(train_args.train):
        ui.print_game_over(state, winner)
    else:
        train_args.train_steps += 1
        train_args.pbar.update(1)

    model.reward(progress, winner)
    return (True, BoardState())


def main():
    ui.print_startup()
    train_args = ui.get_train_args()

    current_state = BoardState()
    model = Model(load_model=True)

    ai_progress = []
    ai_moves = 1

    while True:

        ui.print_state(current_state, train_args)

        if train_args.train:
            indices = [i for i in range(
                len(current_state.board)) if current_state.board[i] == Field.NONE]
            index = random.choice(indices)
        else:
            index = ui.ask_next_move(current_state)

        current_state = current_state.set_field(index, Field.X)
        (game_over, current_state) = evalute_game(
            current_state, model, ai_progress, train_args)
        if game_over:
            ai_progress = []
            ai_moves = 1
            train_args = ui.ask_continue_trainig(train_args)
            continue

        # Pick ai move from discrete random distribution
        ai_move = model.pick_move(current_state, ai_moves)
        ai_progress.append((current_state, ai_move))
        ai_moves += 1

        current_state = current_state.set_field(ai_move, Field.O)
        (game_over, current_state) = evalute_game(
            current_state, model, ai_progress, train_args)
        if game_over:
            ai_progress = []
            ai_moves = 0
            train_args = ui.ask_continue_trainig(train_args)


if __name__ == "__main__":
    main()
