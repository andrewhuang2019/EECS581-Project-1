from enum import Enum

class Sprite(Enum):
    REVEALED = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    UNREVEALED = 9
    FLAG = 10
    MINE = 11
    CLICKED_MINE = 12
    VERITY_SMILE = 13
    VERITY_SUNGLASSES = 14
    VERITY_SURPRISED = 15
    VERITY_DEAD = 16
    BACKGROUND = 17

class Tile():

    def __init__(self, row, col):
        # for display purposes, the number doesn't matter until the tile is revealed
        # if revealed, any value 0 - 8 is considered to be valid, anything else is assumed to be 0 (blank, revealed space)
        self.value: int = -1
        # whether or not a tile is revealed
        self.is_revealed: bool = False
        # whether or not a tile is a mine
        # if is_revealed and is_mine true, then the user clicked on a mine and the clicked mine should be displayed
        self.is_mine: bool = False
        # whether or not a tile is flagged
        # shouldn't be able to flag a revealed tile
        self.is_flagged: bool = False
        # row of the tile
        self.row: int = row
        # column of the tile
        self.col: int = col

class Board():

    def __init__(self, mines):
        # 10x10 2d array of tiles
        # initialize with default tiles
        self.tiles = []
        for r in range(10):
            row = []
            for c in range(10):
                row.append(Tile(r,c))
            self.tiles.append(row)

        self.is_game_won = False
        self.is_game_lost = False
        self.flags_total = -1
        self.flags_remaining = mines 
        self.mines = mines
