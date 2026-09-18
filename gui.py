#gui.py

import pygame as pg
from defs import *


SCALE = 4
SCREEN_WIDTH = 192 # ten 16px tiles + four 8px tiles = 192
SCREEN_HEIGHT = 232 # ten 16px tiles + nine 8px tiles = 232

sprites = {}
screen = pg.display.set_mode((SCALE * SCREEN_WIDTH, SCALE * SCREEN_HEIGHT))

# Function written by John Rader
# return a pg surface scaled by SCALE
def scale_surface(surface):
    return pg.transform.scale_by(surface, SCALE)

# Function written by John Rader
# blit a given surface to screen
# should only be used to draw the tile sprites
def draw_to_tile(surface, tile_coords):
    # determine upper left corner coords of the tile at tile_coords

    # top left tile's top left coord is (16, 56)
    pixel_coords = [16 + tile_coords[0] * 16, 56 + tile_coords[1] * 16]

    # scale
    pixel_coords[0] *= SCALE
    pixel_coords[1] *= SCALE

    screen.blit(surface, pixel_coords)


# helper that returns tile coords for a given mouse position on click
def get_clicked_tile(mouse_pos):

    # convert mouse pos to tile coords
    x, y = mouse_pos

    # scale down to original size
    x //= SCALE
    y //= SCALE

    # adjust for the offset of the top left tile
    x -= 16
    y -= 56

    # if the click is outside of the board, return None
    if (x < 0 or y < 0 or x >= 160 or y >=160):
        return None

    # convert to tile coords
    x //= 16
    y //= 16

    # return (col, row) as a tuple
    col = x
    row = y

    return (col, row)


# load all sprites into memory (sprites dict), then scale
# TODO: add the rest of the needed sprites
def init_sprites():
    # all images drawn to sprites are done so at (0,0), so they fill the entire surface
    dest = (0,0)

    # load entire sprite sheet
    sprite_sheet = pg.image.load("./assets/minesweeper_sheet.png")

    # special sized sprites
    # background is 192x232px
    # get sprite by making a surface of the same size as the sprite, then drawing the image to it
    bg_surf = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_sheet_location = (1, 77, SCREEN_WIDTH, SCREEN_HEIGHT)
    bg_surf.blit(sprite_sheet, dest, area=bg_sheet_location)

    bg_surf = scale_surface(bg_surf)

    sprites[Sprite.BACKGROUND] = bg_surf

    # load 16x16 sprites
    # track sprite type and position on sprite sheet
    # (name, pos(r, c))
    name_locations = [(Sprite.UNREVEALED, (0, 0)),
                      (Sprite.REVEALED, (0, 1)),
                      (Sprite.FLAG, (0, 2)),
                      (Sprite.MINE, (0, 3)),
                      (Sprite.CLICKED_MINE, (1, 0)),
                      (Sprite.ONE, (1, 1)),
                      (Sprite.TWO, (1, 2)),
                      (Sprite.THREE, (1, 3)),
                      (Sprite.FOUR, (2, 0)),
                      (Sprite.FIVE, (2, 1)),
                      (Sprite.SIX, (2, 2)),
                      (Sprite.SEVEN, (2, 3)),
                      (Sprite.EIGHT, (3, 0))]

    abs_pos = (2, 2)
    offset = (17, 17)
    size = (16, 16)
    for name, pos in name_locations:
        save_sprites_from_sheet(name, abs_pos, pos, offset, size, sprite_sheet)

    # load 16x16 verities
    name_locations = [(Sprite.VERITY_SMILE, (0,0)),
                      (Sprite.VERITY_SUNGLASSES, (0, 1)),
                      (Sprite.VERITY_SURPRISED, (1, 0)),
                      (Sprite.VERITY_DEAD, (1,1))]

    abs_pos = (133, 2)
    for name, pos in name_locations:
        save_sprites_from_sheet(name, abs_pos, pos, offset, size, sprite_sheet)

    # load 8x8 cursor arrow
    abs_pos = (79, 11)
    offset = (9, 9)
    size = (8, 8)
    save_sprites_from_sheet(Sprite.CURSOR, abs_pos, (0,0), offset, size, sprite_sheet)

    # load 8x8 red texts
    abs_pos = (97, 11)
    name_locations = [(Sprite.RED_ZERO, (0, 0)),
                      (Sprite.RED_ONE, (0, 1)),
                      (Sprite.RED_TWO, (0, 2)),
                      (Sprite.RED_THREE, (0, 3)),
                      (Sprite.RED_FOUR, (1, 0)),
                      (Sprite.RED_FIVE, (1, 1)),
                      (Sprite.RED_SIX, (1, 2)),
                      (Sprite.RED_SEVEN, (1, 3)),
                      (Sprite.RED_EIGHT, (2, 0)),
                      (Sprite.RED_NINE, (2, 1)),]

    for name, pos in name_locations:
        save_sprites_from_sheet(name, abs_pos, pos, offset, size, sprite_sheet)

    abs_pos = (97, 47)
    offset = (33, 9)
    size = (32, 8)
    # load 32x8 status texts
    name_locations = [(Sprite.TEXT_LOST, (0, 0)),
                      (Sprite.TEXT_WON, (1, 0)),
                      (Sprite.TEXT_PLAYING, (2, 0))]

    for name, pos in name_locations:
        save_sprites_from_sheet(name, abs_pos, pos, offset, size, sprite_sheet)

# draw that 20 to 0 for flags remaining
def draw_flags_left_numbers(board):
    flags = board.flags_remaining
    tens_digit = flags // 10
    ones_digit = flags % 10
    # the sprites are 20 to 29, for zero to nine respectively
    tens_sprite = sprites[tens_digit + 20]
    ones_sprite = sprites[ones_digit + 20]
    # tens_sprite = sprites[Sprite.RED_ZERO]
    # ones_sprite = sprites[Sprite.RED_ZERO]
    
    # screen starts at (1,77) on the sprite sheet so subtract that offset
    locations = [(tens_sprite, [144 - 1, 109 - 77]), (ones_sprite, [152 - 1, 109 - 77])]
    for surf, tile_coord in locations:
        # scale
        tile_coord[0] *= SCALE
        tile_coord[1] *= SCALE

        screen.blit(surf, tile_coord)

# draw the playing status text
def draw_status(board):
    surf = None

    if board.is_game_won:
        surf = Sprite.TEXT_WON.value
    elif board.is_game_lost:
        surf = Sprite.TEXT_LOST.value
    else:
        surf = Sprite.TEXT_PLAYING.value
    
    surf = sprites[surf]

    # screen starts at (1,77) on the sprite sheet so subtract that offset
    tile_coord = [32 - 1, 109 - 77]

    tile_coord[0] *= SCALE
    tile_coord[1] *= SCALE

    screen.blit(surf, tile_coord)

 
# draw from given board
def draw_board(board):
    for r in range(10):
        for c in range(10):
            tile = board.tiles[r][c]

            sprite_to_draw = Sprite.VERITY_DEAD # if this gets drawn then check for error
            pass_value = False

            # if the tile is flagged, then draw the flag
            if (tile.is_flagged):
                sprite_to_draw = Sprite.FLAG
            # if the tile isn't revealed, then just draw the unrevealed tile
            elif (not tile.is_revealed):
                sprite_to_draw = Sprite.UNREVEALED
            # if it is revealed, then check the value to see if it is [0, 8]
            else:
                if (tile.value >= 0 and tile.value <= 8):
                    sprite_to_draw = tile.value
                    pass_value = True
                # if it is revealed and also a mine, draw the revealed mine tile
                elif (tile.is_mine):
                    sprite_to_draw = Sprite.CLICKED_MINE
                else:
                    sprite_to_draw = Sprite.REVEALED

            # get surface to draw
            surf = None

            # use this if passing in an integer instead of sprite enum
            if(pass_value):
                surf = sprites[sprite_to_draw]
            else:
                surf = sprites[sprite_to_draw.value]

            # use (c,r) for (x,y) matching
            draw_to_tile(surf, (c, r))

# Function written by John Rader
# helper to save sheets given the name and relative position of the sprites on the sheet
# name is sprite enum
# absolute_position is the coordinate of the top left pixel of the top left sprite in the set
# spacing is the coordinate representing the horizontal and vertical distance between sprites
# size is the coordinate representing the size of the sprite
# if pass_value is set, lookup with name, not name.value
def save_sprites_from_sheet(name, absolute_position, relative_position, spacing, size, sprite_sheet):
        surf = pg.Surface(size)

        # top left sprite starts at (2, 2), have 1 pixel spacing, and are 16x16
        # use this to find top left of each sprite, 16,16 is the size
        sprite_sheet_location = (absolute_position[0] + relative_position[1] * spacing[0],
                                 absolute_position[1] + relative_position[0] * spacing[1],
                                 size[0], size[1])
        surf.blit(sprite_sheet, (0,0), area=sprite_sheet_location)
        surf = scale_surface(surf)

        sprites[name.value] = surf

# Function outline sourced from pygame tutorial
# core drawing loop
def main():
    # pygame setup
    pg.init()

    clock = pg.time.Clock()
    running = True

    init_sprites()

    # test
    board = Board(10)
    board.tiles[0][0].is_revealed = True
    board.tiles[0][1].is_flagged = True
    board.tiles[0][2].is_mine = True
    board.tiles[0][2].is_flagged = True
    board.tiles[0][3].is_mine = True
    board.tiles[0][3].is_revealed = True
    for i in range(8):
        board.tiles[1][i].value = i + 1
        board.tiles[1][i].is_revealed = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # on click, get the coords of the tile that was clicked
            elif event.type == pg.MOUSEBUTTONDOWN:
                if (event.button == 1): # left click
                    mouse_pos = pg.mouse.get_pos()
                    tile_coords = get_clicked_tile(mouse_pos)
                    if (tile_coords is not None):
                        col, row = tile_coords
                

        # draw background 
        screen.blit(sprites[Sprite.BACKGROUND], (0,0))

        draw_board(board)
        
        draw_cursor(board)

        draw_flags_left_numbers(board)

        draw_status(board)

        # flip() the display to put your work on screen
        pg.display.flip()
        
        clock.tick(10)  # limits FPS to 60

    pg.quit()

# draw cursor below an unrevealed tile
def draw_cursor(board):
    # test drawing cursor
    mouse_pos = pg.mouse.get_pos()
    tile_coords = get_clicked_tile(mouse_pos)

    if (tile_coords is None):
        return

    if (board.tiles[tile_coords[1]][tile_coords[0]].is_revealed):
        return

    one_below = (tile_coords[0], tile_coords[1] + 1)
    draw_to_tile(sprites[Sprite.CURSOR.value], one_below)

if __name__ == "__main__":
    main()
