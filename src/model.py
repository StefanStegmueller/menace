from collections import defaultdict
import json
import os.path
import sys
import numpy as np
from enum import IntEnum
from src.board_state import BoardState, Field, Result


class Operation(IntEnum):
    Rot = 0
    Flip = 1


class Model:
    def __init__(self, load_model=True):
        self.states = defaultdict(set)
        if load_model:
            self.__load_model()

    def pick_move(self, board_state: BoardState, n: int) -> int:
        """
        Determines the move next move of the model given the board state.
        The next move is taken from a discrete probability distribution.
        The probability distribution for a state changes after a game on the basis
        of the outcome.
        """
        probs = self.__get_probabilities(board_state, n)
        probs_normalized = self.__normalize(probs)
        choices = list(range(0, 9))
        choice = np.random.choice(choices, 1, p=probs_normalized)[0].item()
        return choice

    def reward(self, progress: [(BoardState, int)], winner: Result):
        for step in progress:
            board_state = step[0]
            move = step[1]
            probs = self.__get_probabilities(board_state, 0)
            if winner is Result.DRAW:
                probs[move] += 1.0
            elif winner is Result.O_WINS:
                probs[move] += 3.0
            else:
                if probs[move] > 0:
                    probs[move] -= 1.0

            key = board_state.to_string()
            self.states[key] = probs

        self.__safe_model()

    def __get_probabilities(self, board_state: BoardState, n: int) -> list:
        (success, probs) = self.__rot_invariant_search(board_state.board)
        if not success:
            initial_probs = self.__initial_probabilities(board_state, n)
            self.states[board_state.to_string()] = initial_probs
            return initial_probs
        return probs

    def __rot_invariant_search(self, board: list) -> (bool, list):
        """
        Searches for entries invariant of rotation.
        Returns probabilities with rotation of given board state
        rotation invartiant state as key.
        """
        operations = []
        max_depth = 8
        depth = 1

        def search(b: list, d: int, o: Operation) -> (bool, list):
            key = BoardState.from_board(b).to_string()
            if key in self.states:
                probs = self.__reverse_transform(operations, self.states[key])

                # Remove found key
                del self.states[key]

                # Save transformed probabilites with searched key
                searched_key = BoardState.from_board(board).to_string()
                self.states[searched_key] = probs

                return (True, probs)
            elif d == max_depth:
                return (False, [])
            else:
                if o == Operation.Flip:
                    transformed = self.__flip_vertically(b)
                    operations.append(o)
                    o = Operation.Rot
                elif o == Operation.Rot:
                    transformed = self.__flip_vertically(b)
                    del operations[-1]
                    transformed = self.__rotate(transformed, clockwise=True)
                    operations.append(o)
                    o = Operation.Flip
                d += 1
                return search(transformed, d, o)

        return search(board, depth, Operation.Flip)

    def __reverse_transform(self, operations: list, probs: list) -> list:
        transformed_probs = probs
        for op in reversed(operations):
            if op == Operation.Rot:
                transformed_probs = self.__rotate(
                    transformed_probs, clockwise=False)
            elif op == Operation.Flip:
                transformed_probs = self.__flip_vertically(transformed_probs)
        return transformed_probs

    def __rotate(self, board: list, clockwise=True) -> list:
        """Rotates given board list for 90 degrees."""
        m = np.array(board)
        m = m.reshape(3, 3)

        if clockwise:
            rotated = np.rot90(m, 3)
        else:
            rotated = np.rot90(m)

        return rotated.flatten().tolist()

    def __flip_vertically(self, board: list) -> list:
        """Flips given board list vertically."""
        m = np.array(board)
        m = m.reshape(3, 3)
        return np.fliplr(m).flatten().tolist()

    def __safe_model(self):
        path = self.__model_resource_path()
        with open(path, "w") as file:
            json.dump(self.states, file, sort_keys=True, indent=4)

    def __load_model(self):
        path = self.__model_resource_path()
        if os.path.isfile(path):
            with open(path, "r") as file:
                self.states = json.load(file)

    def __model_resource_path(self) -> str:
        dir = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]
        return os.path.join(dir, 'model.json')

    def __initial_probabilities(self, board_state: BoardState, n: int) -> list:
        return [5 - n if i == Field.NONE else -1 for i in board_state.board]

    def __normalize(self, probs: list) -> list:
        if all(p == -1 or p == 0 for p in probs):
            probs = [1 if i == 0 else 0 for i in probs]
        else:
            probs = [0 if i == -1 else i for i in probs]
        return list(map(lambda x: x / sum(probs), probs))
