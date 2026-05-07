import random

# --- Board Setup ---

def start_game():
    """Initialize a 4x4 board with two starting tiles."""
    board = [[0] * 4 for _ in range(4)]
    board = add_new_tile(board)
    board = add_new_tile(board)
    return board

def add_new_tile(board):
    """Add a new tile (2 or 4) to a random empty cell."""
    empty_cells = [
        (r, c)
        for r in range(4)
        for c in range(4)
        if board[r][c] == 0
    ]
    if not empty_cells:
        return board
    r, c = random.choice(empty_cells)
    board[r][c] = 4 if random.random() > 0.9 else 2
    return board

# --- Display ---

def print_board(board):
    """Print the board in a readable grid format."""
    print("\n+-------+-------+-------+-------+")
    for row in board:
        print("|", end="")
        for val in row:
            if val == 0:
                print("       |", end="")
            else:
                print(f"{val:^7}|", end="")
        print("\n+-------+-------+-------+-------+")

# --- Moves ---

def _slide_and_merge(row):
    """Slide non-zero tiles left, merge equal adjacent tiles, pad with zeros."""
    tiles = [x for x in row if x != 0]
    score_gained = 0
    merged = []
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged_val = tiles[i] * 2
            merged.append(merged_val)
            score_gained += merged_val
            i += 2
        else:
            merged.append(tiles[i])
            i += 1
    merged += [0] * (4 - len(merged))
    return merged, score_gained

def move_left(board):
    new_board = []
    total_score = 0
    for row in board:
        new_row, gained = _slide_and_merge(row)
        new_board.append(new_row)
        total_score += gained
    return new_board, total_score

def move_right(board):
    new_board = []
    total_score = 0
    for row in board:
        reversed_row, gained = _slide_and_merge(row[::-1])
        new_board.append(reversed_row[::-1])
        total_score += gained
    return new_board, total_score

def move_up(board):
    transposed = [list(col) for col in zip(*board)]
    moved, total_score = move_left(transposed)
    return [list(row) for row in zip(*moved)], total_score

def move_down(board):
    transposed = [list(col) for col in zip(*board)]
    moved, total_score = move_right(transposed)
    return [list(row) for row in zip(*moved)], total_score

# --- Game State Checks ---

def board_changed(old_board, new_board):
    """Return True if the board state has changed after a move."""
    return old_board != new_board

def has_won(board):
    """Return True if any tile has reached 2048."""
    return any(board[r][c] == 2048 for r in range(4) for c in range(4))

def has_moves_left(board):
    """Return True if there is at least one valid move remaining."""
    # Any empty cell means moves exist
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:
                return True
    # Check horizontal merges
    for r in range(4):
        for c in range(3):
            if board[r][c] == board[r][c + 1]:
                return True
    # Check vertical merges
    for r in range(3):
        for c in range(4):
            if board[r][c] == board[r + 1][c]:
                return True
    return False

def get_current_score(board):
    """Return the sum of all tile values (informational, not game score)."""
    return sum(board[r][c] for r in range(4) for c in range(4))
