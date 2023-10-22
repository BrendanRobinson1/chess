from typing import List, Optional, Tuple
from IPython.display import clear_output
import time

from chess.enums import Team
from chess.pieces import Piece, PlaceHolder, Pawn, Rook, Knight, Queen, Bishop, King
from chess.values import (
    BOARD_WIDTH,
    ROOK_MOVES,
    KNIGHT_MOVES,
    BISHOP_MOVES,
    QUEEN_MOVES,
    KING_MOVES,
    POSITION_TYPE,
    name_to_idx_mapping,
    GameOver,
)
    
    

class ChessBoard:
    board: List[List[Piece]]  # All spots will always be occupied by a Piece type

    def __init__(self):
        """Class representing the core board component of the game."""
        self.set_board()

    def __repr__(self) -> str:
        return f"\n{'_' * 133}\n".join(['|\t'+'|\t'.join([piece.display_piece() for piece in row])+'|' for row in self.board])
    
    def __repr_str__(self) -> str:
        return self.__repr__()

    def set_board(self):
        """Set the board for a new game."""
        empty_row = lambda row: [PlaceHolder(starting_position=(n, row), moves=[]) for n in range(BOARD_WIDTH)]
        pawns = lambda team, row: [Pawn(starting_position=(n, row), team=team, moves=[]) for n in range(BOARD_WIDTH)]
        back_row = lambda team, row: [
            Rook(starting_position=(0, row), team=team, moves=ROOK_MOVES),
            Knight(starting_position=(1, row), team=team, moves=KNIGHT_MOVES),
            Bishop(starting_position=(2, row), team=team, moves=BISHOP_MOVES),
            Queen(starting_position=(3, row), team=team, moves=QUEEN_MOVES),
            King(starting_position=(4, row), team=team, moves=KING_MOVES),
            Bishop(starting_position=(5, row), team=team, moves=BISHOP_MOVES),
            Knight(starting_position=(6, row), team=team, moves=KNIGHT_MOVES),
            Rook(starting_position=(7, row), team=team, moves=ROOK_MOVES),
        ]
        self.board = [
            back_row(Team.black, 0),
            pawns(Team.black, 1),
            empty_row(2),
            empty_row(3),
            empty_row(4),
            empty_row(5),
            pawns(Team.white, 6),
            back_row(Team.white, 7),            
        ]
        
    def _get_piece(self, location: POSITION_TYPE) -> Piece:
        """Return the piece at location."""
        return self.board[location[1]][location[0]]
    
    def _place_piece(self, piece: Piece, location: POSITION_TYPE):
        """Place `piece` on the board at `location`."""
        self.board[location[1]][location[0]] = piece

    def _same_team(self, team: Team, location: POSITION_TYPE) -> bool:
        """Returns bool if current team is occupying location."""
        return self._get_piece(location).team == team
    
    def _move_overrides(self, piece: Piece, from_idx: POSITION_TYPE, to_idx: POSITION_TYPE) -> bool:
        """Sometimes a typically legal move is illegal.
        
        Uses:
        - Pawn cannot move forwards when that space is occupied by opposite team
        - When you're in check (not implemented yet idk how)
        """
        if isinstance(piece, Pawn) and (from_idx[0] - to_idx[0] == 0):  # If a pawn is regularly moving forwards
            # Return `True` if the piece we're moving to is on the opposite team
            # Return `False` if the team is NA (placeholder), or same (already checked and disallowed)
            return self._get_piece(to_idx).team == piece.team.change()
        return False
    
    def _allowable_move(self, from_idx: POSITION_TYPE, to_idx: POSITION_TYPE) -> bool:
        """Returns bool if piece at `from_idx` can legally move to `to_idx`."""
        taking = not isinstance(self._get_piece(to_idx), PlaceHolder)  # Take anything other than a placeholder
        piece = self._get_piece(from_idx)
        if self._move_overrides(piece, from_idx, to_idx):
            return False  # I.e. a pawn cannot move forward if the other team's piece is there
        return piece.allowable_move(to_idx, taking=taking)
    
    def _check_path(self, from_idx: POSITION_TYPE, to_idx: POSITION_TYPE) -> bool:
        """Returns False is the path is empty, True if there is an obstacle."""
        piece = self._get_piece(from_idx)  # The piece to move
        if piece.name == "Knight":
            return False  # Knights can just jump over pieces
        path = get_path(from_idx, to_idx)  # List of all points to traverse (not incl. to_idx)
        if len(path) == 1:
            return False  # Moving to adjacent square, not necessary to check
        path = path[1:]  # Remove from_idx, own piece would be a false positive
        return any(  # False if any of the points contain a non-PlaceHolder, True if all are PlaceHolders
            [not isinstance(self._get_piece(point), PlaceHolder) for point in path]
        )
    
    def can_x_move_to_y(self, team: Team, from_idx: POSITION_TYPE, to_idx: POSITION_TYPE) -> Tuple[bool, str]:
        """Checks:
        1. Your team isn't occupying the space
        2. The piece can legally move to that space
        3. No pieces are blocking the movement
        4. Making sure if avoid check if necessary TODO
        """
        if self._same_team(team, to_idx):
            return False, "Try again, your piece is there! "
        elif not self._allowable_move(from_idx, to_idx):
            return False, "Try again, that move wasn't legal! "
        elif self._check_path(from_idx, to_idx):
            return False, "Try again, there is another piece in the way! "
        else:
            return True, ""
        
    @staticmethod
    def _request_square(req_str: str) -> Optional[POSITION_TYPE]:
        requested = input(req_str).lower()
        try:
            return name_to_idx_mapping[requested]
        except KeyError:
            if requested in ["poo", "exit", "cancel", "escape", "quit"]:
                raise GameOver("Game over man, game over!")
            return None
        
    def get_move(self, team: Team) -> Tuple[POSITION_TYPE, POSITION_TYPE]:
        """Asks the player for a move, and returns from_cell_idx, to_cell_idx."""
        msg = ''
        while True:  # input loop for picking the piece to move
            from_idx = self._request_square(f"{msg}{team.name}'s turn! Pick a piece to move")
            if from_idx is None:
                msg = "Invalid square name! "
                continue
            if not self._same_team(team, from_idx):
                msg = "Try again, that wasn't your piece! "
            elif not any([self.can_x_move_to_y(team, from_idx, _to_idx)[0] for _to_idx in name_to_idx_mapping.values()]):
                msg = "Try again, no possible moves for that piece! "
            else:
                break  # If you own the piece, and there is a possible move, accept this input
            # Make a way to get back here, if you want to change

        msg = ''
        while True:  # input loop for picking where to move
            to_idx = self._request_square(f"{msg}{team.name}'s turn! Pick a square to move to")
            if to_idx is None:
                msg = "Invalid square name! "
                continue
            legal_move, msg = self.can_x_move_to_y(team, from_idx, to_idx)
            if legal_move:
                break  # Target cell needs to NOT have your piece
            
        return from_idx, to_idx
    
    def move_a_piece(self, from_idx: POSITION_TYPE, to_idx: POSITION_TYPE):
        """Moves a piece from position, to new position, updates piece's position, and initialises a new PlaceHolder."""
        piece_to_move = self._get_piece(from_idx)
        piece_to_move.position = to_idx  # Update the position of it
        self._place_piece(piece_to_move, to_idx)  # Place the piece in it's new spot (overwriting whatever was there).
        self._place_piece(PlaceHolder(starting_position=to_idx, moves=[]), location=from_idx)  # Place a new placeholder

    def play(self):
        """Start playing!"""
        team = Team.pick()
        while True:  # Turn loop
            print(self)
            time.sleep(1)
            move_from, move_to = self.get_move(team)
            # TODO check for checks that would void this move, check if a piece is in the way (these need to be done in get_move)
            # The things are flipped, i.e. a1 references black, when it should reference white, not a6
            self.move_a_piece(from_idx=move_from, to_idx=move_to)
            clear_output(wait=True)
            # End of turn, change team
            team = team.change()


def get_path(from_idx: POSITION_TYPE, to_idx: POSITION_TYPE) -> List[POSITION_TYPE]:
    """Returns a list of all points along the path of `from_idx` to `to_idx`."""
    # Straight lines
    if from_idx[0] == to_idx[0]:
        step = 1 if from_idx[1] < to_idx[1] else -1
        return [(from_idx[0], y) for y in range(from_idx[1], to_idx[1], step)]
    elif from_idx[1] == to_idx[1]:
        step = 1 if from_idx[0] < to_idx[0] else -1
        return [(x, from_idx[1]) for x in range(from_idx[0], to_idx[0], step)]
    # Diagonal lines
    raise NotImplementedError()
