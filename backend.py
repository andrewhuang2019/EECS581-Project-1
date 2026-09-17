# BACKEND GOES HERE

from defs import Tile, Board

def left_click_tile(tile: Tile, board: Board):
    if (tile.is_flagged or tile.is_revealed):
        return

    tile.is_revealed = True
    board.num_revealed += 1

    if (tile.is_mine):
        board.is_game_lost = True
        return

    if (tile.value == 0):
        surrounding_tiles = get_surrounding_tiles(tile, board); 

        for nearby_tiles in surrounding_tiles:
            # left click all tiles surrounding the tile
            left_click(nearby_tiles, board)

    check_win(board)

def check_win(board: Board):
    if (board.num_revealed == (100 - board.mines)):
        board.is_game_won = True

def get_surrounding_tiles(tile: Tile, board: Board):
    surrounding_tiles = []

    for row in range(-1, 1):
        for col in range(-1, 1):
            offset_row = tile.row + row
            offset_col = tile.col + col 
            if offset_row < 0 or offset_row > 10:
                continue
            if offset_col < 0 or offset_col > 10:
                continue
            surrounding_tiles.append(board.tiles[offset_row][offset_col])

    return surrounding_tiles

def right_click_tile(tile: Tile, board: Board):
    if not tile.is_revealed:
        tile.is_flagged = not tile.is_flagged
        if tile.is_flagged:
            board.flags_remaining -= 1
        else:
            board.flags_remaining += 1