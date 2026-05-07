from logic import (
    start_game,
    add_new_tile,
    print_board,
    move_left,
    move_right,
    move_up,
    move_down,
    board_changed,
    has_won,
    has_moves_left,
)

MOVES = {
    "w": move_up,
    "s": move_down,
    "a": move_left,
    "d": move_right,
}

MOVE_NAMES = {"w": "Up", "s": "Down", "a": "Left", "d": "Right"}

def get_input():
    """Prompt the player for a valid move key."""
    while True:
        key = input("\nMove (W/A/S/D) or Q to quit: ").strip().lower()
        if key in MOVES or key == "q":
            return key
        print("  Invalid input. Use W (up), A (left), S (down), D (right), or Q to quit.")

def main():
    print("=" * 37)
    print("           Welcome to 2048!")
    print("=" * 37)
    print("  Combine tiles to reach 2048.")
    print("  W = Up   S = Down   A = Left   D = Right")

    board = start_game()
    score = 0

    while True:
        print_board(board)
        print(f"  Score: {score}")

        if has_won(board):
            print("\n  *** Congratulations! You reached 2048! ***")
            again = input("  Keep playing? (Y/N): ").strip().lower()
            if again != "y":
                break

        if not has_moves_left(board):
            print("\n  No moves left. Game over!")
            break

        key = get_input()

        if key == "q":
            print("\n  Thanks for playing. Final score:", score)
            break

        move_fn = MOVES[key]
        new_board, gained = move_fn(board)

        if not board_changed(board, new_board):
            print(f"  Can't move {MOVE_NAMES[key]} — try a different direction.")
            continue

        board = add_new_tile(new_board)
        score += gained

    print("\n  Final board:")
    print_board(board)
    print(f"  Final score: {score}")
    print("=" * 37)

if __name__ == "__main__":
    main()
