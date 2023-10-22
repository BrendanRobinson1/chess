from typing import List
from dataclasses import dataclass
from PIL import Image

from chess.enums import Team
from chess.values import POSITION_TYPE


PIECE_TYPES = ["PlaceHolder", "Pawn  ", "Rook  ", "Bishop", "Knight", "Queen ", "King  "]
PIECE_IMAGE_PATH = r"C:/Users/binda/Pictures/chess_png"


@dataclass
class Piece:
    starting_position: POSITION_TYPE
    moves: List[POSITION_TYPE]
    team: Team
    name: str
    
    def __post_init__(self):
        self.position = self.starting_position
        self.image = (
            Image.open(f'{PIECE_IMAGE_PATH}/{self.team.name}_{self.name.strip().lower()}.png')
            if self.team != Team.na
            else None
        )  # TODO How do I actually use these images?? Very cool though
        assert self.name in PIECE_TYPES
        
    def _check_deltas(
        self, new_position: POSITION_TYPE, allowable_combos: List[POSITION_TYPE]
    ) -> bool:
        white_team_bool = -1 if self.team == Team.white else 1  # white needs idx to go opposite way on y
        return any(
            ((new_position[0] - self.position[0]) == x) and ((new_position[1] - self.position[1]) == white_team_bool * y)
            for x, y in allowable_combos 
        )

    def allowable_move(self, new_position: POSITION_TYPE, taking: bool = False) -> bool:
        return self._check_deltas(new_position, self.moves)
    
    def display_piece(self) -> str:
        return f"{self.team.name}_{self.name}"
    
    
@dataclass
class PlaceHolder(Piece):
    team: Team = Team.na
    name: str = 'PlaceHolder'
    
    def display_piece(self) -> str:
        return "            "  # Blank...

   
@dataclass
class Pawn(Piece):
    name: str = "Pawn  "
    
    def allowable_move(self, new_position: POSITION_TYPE, taking: bool = False) -> bool:
        allowable_combos = [(0, 1)]  # You can always move up one, unless there's a piece there
        if self.starting_position == self.position:
            allowable_combos.append((0, 2))  # If at start you can move up two
        if taking:
            allowable_combos.extend([(-1, 1), (1, 1)])  # If you're taking, allowed to go diagonal up
        return self._check_deltas(new_position, allowable_combos)
        

@dataclass
class Knight(Piece):
    name: str = "Knight"


@dataclass
class Bishop(Piece):
    name: str = "Bishop"


@dataclass
class Rook(Piece):
    name: str = "Rook  "


@dataclass
class Queen(Piece):
    name: str = "Queen "


@dataclass
class King(Piece):
    name: str = "King  "
