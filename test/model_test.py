import unittest
from functools import reduce
from src.model import Model
from src.board_state import BoardState, Result


class ModelTest(unittest.TestCase):

    def test_search(self):

        def search_t(mock_key, test_key):
            mock_probs = self.mock_state_probs(mock_key)
            model = Model(load_model=False)
            model.states[mock_key] = mock_probs

            searched_board = self.to_int_list(test_key)
            searched_board_state = BoardState.from_board(searched_board)

            for _ in range(0, 100):
                picked_move = model.pick_move(searched_board_state, 1)
                self.assertEqual(
                    searched_board[picked_move], 0, "Search Error with keys " + mock_key + " and " + test_key)

        # Test one field set
        search_t("000001000", "000000010")
        search_t("000100000", "000001000")
        search_t("001000000", "000000100")

        # Test two fields set
        search_t("102000000", "000000102")
        search_t("120000000", "000000021")
        search_t("102000000", "000000102")

        # Test three fields set
        search_t("102000100", "100000102")
        search_t("100020010", "001020100")

    def test_reward(self):
        model_keys = [
            "000000100",
            "000210100",
            "020112001"
        ]

        model_probs = [
            "112111011",
            "211001011",
            "101000120"
        ]
        model = Model(load_model=False)

        for i, k in enumerate(model_keys):
            model.states[k] = self.to_int_list(model_probs[i])

        ai_keys = [
            "001000000",
            "001012000",
            "001112020"
        ]
        ai_boards = [BoardState.from_board(
            self.to_int_list(s)) for s in ai_keys]

        ai_moves = [5, 7, 1]
        progress = list(zip(ai_boards, ai_moves))

        model.reward(progress, Result.X_WINS)

        target_probs = [
            "110110211",
            "110100102",
            "110000101"
        ]
        target_probs = [list(map(float, self.to_int_list(p)))
                        for p in target_probs]

        self.assertEqual(len(model.states), len(model_keys),
                         "Too much state entries in model.")

        for i, k in enumerate(ai_keys):
            model_probs = model.states[k]
            self.assertEqual(model_probs, target_probs[i])

    def to_int_list(self, key: str) -> list:
        return list(map(int, key))

    def mock_state_probs(self, key: str) -> list:
        return [1 if c == "0" else 0 for c in key]


if __name__ == "__main__":
    unittest.main()
