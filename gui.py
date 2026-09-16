# Example file showing a basic pygame "game loop"
import pygame as pg
from enum import Enum


SCALE = 6
SCREEN_WIDTH = 192 # ten 16px tiles + four 8px tiles = 192
SCREEN_HEIGHT = 232 # ten 16px tiles + nine 8px tiles = 232

sprites = {}
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
    COVERED = 9
    FLAG = 10
    MINE = 11
    CLICKED_MINE = 12
    VERITY_SMILE = 13
    VERITY_SUNGLASSES = 14
    VERITY_SURPRISED = 15
    VERITY_DEAD = 16
    BACKGROUND = 17

# return a pg surface scaled by SCALE
def scale_surface(surface):
    return pg.transform.scale_by(surface, SCALE)

# blit a given surface to screen
# should only be used to draw the tile sprites
def draw_to_tile(screen, surface, tile_coords):
    # determine upper left corner coords of the tile at tile_coords

    # top left tile's top left coord is (16, 56)
    pixel_coords = [16 + tile_coords[0] * 16, 56 + tile_coords[1] * 16]

    # scale
    pixel_coords[0] *= SCALE
    pixel_coords[1] *= SCALE

    screen.blit(surface, pixel_coords)

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
    name_locations = [(Sprite.COVERED, (0, 0)),
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

# helper to save sheets given the name and relative position of the sprites on the sheet
# name is sprite enum
# absolute_position is the coordinate of the top left pixel of the top left sprite in the set
# spacing is the coordinate representing the horizontal and vertical distance between sprites
# size is the coordinate representing the size of the sprite
def save_sprites_from_sheet(name, absolute_position, relative_position, spacing, size, sprite_sheet):
        surf = pg.Surface((16, 16))

        # top left sprite starts at (2, 2), have 1 pixel spacing, and are 16x16
        # use this to find top left of each sprite, 16,16 is the size
        sprite_sheet_location = (absolute_position[0] + relative_position[1] * spacing[0],
                                 absolute_position[1] + relative_position[0] * spacing[1],
                                 size[0], size[1])
        surf.blit(sprite_sheet, (0,0), area=sprite_sheet_location)
        surf = scale_surface(surf)

        sprites[name.value] = surf

def main():
    # pygame setup
    pg.init()

    screen = pg.display.set_mode((SCALE * SCREEN_WIDTH, SCALE * SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True

    init_sprites()

    i = 0
    while running:
        i += 1
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # draw background 
        screen.blit(sprites[Sprite.BACKGROUND], (0,0))

        # test
        for r in range(10):
            for c in range(10):
                draw_to_tile(screen, sprites[(10 * r + c) % 17], (c,r))
        
        # flip() the display to put your work on screen
        pg.display.flip()
        
        clock.tick(5)  # limits FPS to 60

    pg.quit()

if __name__ == "__main__":
    main()
