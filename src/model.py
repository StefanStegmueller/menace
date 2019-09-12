from collections import defaultdict
import json
import os.path
import sys
import numpy as np
from enum import IntEnum
from src.board_state import BoardState, Field, Result


class Model:
    def __init__(self):
        self.states = defaultdict(set)
        self.__load_model()

    def pick_move(self, board_state):
        """
        Determines the move next move of the model given the board state.
        The next move is taken from a discrete probability distribution.
        The probability distribution for a state changes after a game on the basis
        of the outcome.
        """
        probs_normalized = self.__normalize(
            self.__get_probabilities(board_state))
        choices = list(range(0, 9))
        choice = np.random.choice(choices, 1, p=probs_normalized)[0].item()
        return choice

    def reward(self, progress: [(BoardState, int)], winner: Result):
        for step in progress:
            board_state = step[0]
            move = step[1]
            probs = self.__get_probabilities(board_state)
            if winner is Result.DRAW:
                probs[move] += probs[move]
            elif winner is Result.O_WINS:
                probs[move] += 3.0
            else:
                if probs[move] <= 1.0:
                    probs[move] = 1.0
                else:
                    probs[move] -= 1.0

            if sum(probs) >= 1000:
                probs = [p / 10 for p in probs]

            key = board_state.to_string()
            self.states[key] = probs
        self.__safe_model()

    def __get_probabilities(self, board_state: BoardState):
        if board_state.to_string() in self.states:
            return self.states[board_state.to_string()]
        return self.__initial_probabilities(board_state)

    def __safe_model(self):
        path = self.__model_resource_path()
        with open(path, "w") as file:
            json.dump(self.states, file, sort_keys=True, indent=4)

    def __load_model(self):
        path = self.__model_resource_path()
        if os.path.isfile(path):
            with open(path, "r") as file:
                self.states = json.load(file)

    def __model_resource_path(self):
        dir = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]
        return os.path.join(dir, 'model.json')

    def __initial_probabilities(self, board_state: BoardState):
        return [100.0 if i == Field.NONE else 0 for i in board_state.board]

    def __normalize(self, probs):
        return list(map(lambda x: x / sum(probs), probs))
