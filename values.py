from typing import Dict, Tuple


# Basics
SQUARE_NAMES = [
    [f"{letter}{number}" for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]]
    for number in range(8, 0, -1)
]
BOARD_WIDTH = len(SQUARE_NAMES)
POSITION_TYPE = Tuple[int, int]


# Piece movements
BISHOP_MOVES = [  # Any combination of positive and negative, when the xy diff is the same.
    (n, n) for n in range(1, BOARD_WIDTH)
] + [(n, -n) for n in range(1, BOARD_WIDTH)] + [(-n, n) for n in range(1, BOARD_WIDTH)] + [
    (-n, -n) for n in range(1, BOARD_WIDTH)
]
ROOK_MOVES = [  # Any straight line.
    (0, n) for n in range(1, BOARD_WIDTH)
] + [(0, -n) for n in range(1, BOARD_WIDTH)] + [(n, 0) for n in range(1, BOARD_WIDTH)] + [
    (-n, 0) for n in range(1, BOARD_WIDTH)
]
KNIGHT_MOVES = [(-1, 2), (1, 2), (-1, -2), (1, -2), (-2, 1), (2, 1), (-2, -1), (2, -1)]
QUEEN_MOVES = BISHOP_MOVES + ROOK_MOVES  # Can go in any direction
KING_MOVES = [move for move in QUEEN_MOVES if (abs(move[0]) <= 1) and (abs(move[1]) <= 1)]  # Queen with a 1 radius


# Sqaure name - idx mappings
idx_name_mapping = lambda position: SQUARE_NAMES[position[1]][position[0]]
name_to_idx_mapping: Dict[str, POSITION_TYPE] = {}
for x, _list in enumerate(SQUARE_NAMES):
    for y, _ in enumerate(_list):
        name = idx_name_mapping((x, y))
        name_to_idx_mapping[name] = (x, y)


# What to raise for game end
class GameOver(BaseException):
    pass
