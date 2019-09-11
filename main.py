from src.board_state import Field, BoardState


def main():
    test = 120000000
    state = BoardState.from_int(test)
    state.set_field(2, Field.X)
    print(state)


if __name__ == "__main__":
    main()
