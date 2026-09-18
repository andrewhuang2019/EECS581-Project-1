# BACKEND GOES HERE

from defs import Tile, Board
import random

#handler function for when the user clicks a tile for the first time
def first_click(tile: Tile, board: Board):
    block_mine = {} #create dictionary to hold tiles that cannot contain mines
    first_click_tiles = get_surrounding_tiles(tile, board) #get first click tile along with adjacent tiles

    for t in first_click_tiles:
        block_mine[t.row] = t.col #add first click tiles to dictionary 

    make_mines(board, block_mine) # randomly place mines in available board spaces

    #iterate through all tiles on the board
    for row in range(10):
        for col in range(10):
            if board.tiles[row][col].is_mine == False: #if tile is not a mine
                mines_nearby(board.tiles[row][col], board) #set value to number of adjacent mines
    
    left_click_tile(tile, board) #run left click behavior on the first clicked tile

#randomly places user-specified number of mines on a board (no mines placed on first click or its adjacent tiles)
def make_mines(board: Board, blocked_mines: dict):
    mine_count = 0 #numbers of mines placed on board so far
    while mine_count < board.mines: #while mine count less than user mine input
        #generate random integer for row and column 
        rand_row = random.randint(0,9) 
        rand_col = random.randint(0,9)

        if rand_row not in blocked_mines or blocked_mines[rand_row] != rand_col: #if random tile is not in blocked mines dictionary
            board.tiles[rand_row][rand_col].is_mine = True #place mine 

            mine_count += 1 #increment mine count

#changes the "value" member variable of a passed Tile object to the number of adjacent mines
def mines_nearby(tile: Tile, board: Board):
    tile.value = 0 #set tile value to 0
    surrounding_tiles = get_surrounding_tiles(tile, board) #get list of the tiles adjacent to current tile
    
    for t in surrounding_tiles: #iterate through the surrounding tiles
        if t.is_mine == True: #if this surrounding tile is a mine
            tile.value += 1 #increment current tile's value
    
def get_tile_at_coords(coords, board: Board):
    return board.tiles[coords[0]][coords[1]]

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
            left_click_tile(nearby_tiles, board)

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
