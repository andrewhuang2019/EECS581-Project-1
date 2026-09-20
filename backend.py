# BACKEND GOES HERE

from defs import Tile, Board
import random

#handler function for when the user clicks a tile for the first time
def first_click(tile: Tile, board: Board):
    first_click_tiles = get_surrounding_tiles(tile, board) #get first click tile along with adjacent tiles
    block_mine = {(t.row, t.col) for t in first_click_tiles} #create set of tuples to hold tiles that cannot contain mines

    make_mines(board, block_mine) # randomly place mines in available board spaces

    #iterate through all tiles on the board
    for row in range(10):
        for col in range(10):
            if board.tiles[row][col].is_mine == False: #if tile is not a mine
                mines_nearby(board.tiles[row][col], board) #set value to number of adjacent mines
    
    left_click_tile(tile, board) #run left click behavior on the first clicked tile

#randomly places user-specified number of mines on a board (no mines placed on first click or its adjacent tiles)
def make_mines(board: Board, blocked_mines: set):
    mine_count = 0 #numbers of mines placed on board so far
    while mine_count < board.mines: #while mine count less than user mine input
        #generate random integer for row and column 
        rand_row = random.randint(0,9) 
        rand_col = random.randint(0,9)

        #if random tile is not in blocked mines set and has not already been made a mine
        if ((rand_row, rand_col) not in blocked_mines) and (not board.tiles[rand_row][rand_col].is_mine):
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

# Function written by Sina Asheghalishahi
# reveals all mines on the board (used when the user clicks on a mine)
def reveal_all_mines(board: Board):
    for row in range(10):
        for col in range(10):
            if board.tiles[row][col].is_mine:
                board.tiles[row][col].is_revealed = True

# handler function for when the user left clicks a tile
def left_click_tile(tile: Tile, board: Board):

    if board.is_game_lost or board.is_game_won:
        return

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
        board.clicked_mine = tile
        reveal_all_mines(board)
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
            if offset_row < 0 or offset_row >= 10:
                continue
            if offset_col < 0 or offset_col >= 10:
                continue
            if(row == 0 and col == 0):
                continue
            # add the surrounding tile if the iteration was not skipped
            surrounding_tiles.append(board.tiles[offset_row][offset_col])

    return surrounding_tiles

# ignore clicks if game is lost
# ignore tile if revealed
# flag an unflagged tile if there are flags left
# unflag a flagged tile
# update values accordingly
def right_click_tile(tile: Tile, board: Board):

    # ignore revealed tiles
    if tile.is_revealed or board.is_game_lost or board.is_game_won:
        return

    # try to flag
    if not tile.is_flagged and board.flags_remaining > 0:
        board.flags_remaining -= 1
        tile.is_flagged = True
        return
    
    # unflag
    if tile.is_flagged:
        board.flags_remaining += 1
        tile.is_flagged = False
        return

