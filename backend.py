# BACKEND GOES HERE

from defs import Tile, Board

# handler function for when the user left clicks a tile
def left_click_tile(tile: Tile, board: Board):
    # if the tile is flagged, ignore the click
    # if the tile is already revealed, ignore the click
    if (tile.is_flagged or tile.is_revealed):
        return

    # set the tile as revealed
    tile.is_revealed = True

    # increase the number of revealed tiles
    board.num_revealed += 1

    # if the tile is a mine, set the game lost parameter to true
    if (tile.is_mine):
        board.is_game_lost = True
        return

    # if the tile has no surrounding mines, recursively click the surrounding tiles
    if (tile.value == 0):
        surrounding_tiles = get_surrounding_tiles(tile, board); 

        for nearby_tiles in surrounding_tiles:
            # left click all tiles surrounding the tile
            left_click(nearby_tiles, board)

    # check to see if the win conditions are true
    check_win(board)

# function to check if all non-mine tiles have been revealed
def check_win(board: Board):
    if (board.num_revealed == (100 - board.mines)):
        board.is_game_won = True

# obtains the valid tiles surrounding the input tile on the board
def get_surrounding_tiles(tile: Tile, board: Board):
    surrounding_tiles = []

    # iterate from -1 to 1 offset row from the tile's row
    for row in range(-1, 2):
        # iterate from -1 to 1 offset column from the tile's column
        for col in range(-1, 2):
            offset_row = tile.row + row
            offset_col = tile.col + col 
            if offset_row < 0 or offset_row > 10:
                continue
            if offset_col < 0 or offset_col > 10:
                continue
            # add the surrounding tile if the iteration was not skipped
            surrounding_tiles.append(board.tiles[offset_row][offset_col])

    return surrounding_tiles

def right_click_tile(tile: Tile, board: Board):
    if not tile.is_revealed:
        tile.is_flagged = not tile.is_flagged
        if tile.is_flagged:
            board.flags_remaining -= 1
        else:
            board.flags_remaining += 1
