import os
import pygame
import random

from colour import Color
from hexgrid import legal_tile_ids
from pprint import pprint
from pygame.locals import *
from Tiles import GameTile, ResourceTile
from utils import ASSET_DIR, TILE_CARDS_DIR


# Initialize pygame
pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 785, 724


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
bg_img = pygame.image.load(os.path.join(ASSET_DIR, "tile_order.png"))
bg_img.convert()
bg_rect = bg_img.get_rect()


def setup():
    # maps the tile_id to the x, y, coordinates for the screen
    board_mapping = {
        1: (236, 98),
        2: (162, 233),
        3: (81, 364),
        4: (162, 494),
        5: (239, 630),
        6: (393, 629),
        7: (545, 631),
        8: (622, 496),
        9: (703, 362),
        10: (623, 229),
        11: (547, 96),
        12: (391, 95),
        13: (314, 229),
        14: (236, 363),
        15: (317, 495),
        16: (469, 496),
        17: (545, 363),
        18: (468, 230),
        19: (392, 362)
    }
    # Create the board as a list of GameTile Objects
    board = [GameTile(random.randint(0, 12),
                      random.choice(list(ResourceTile)), 4,
                      tile_id) for tile_id in legal_tile_ids()]

    # fill the tile_sprites list with the correct Gametile assets
    tile_sprites = []
    for gametile in board:
        image = pygame.image.load(gametile.tile.asset())
        image = pygame.transform.scale(image, (image.get_rect().width / 2.5,
                                               image.get_rect().height / 2.5))

        image.convert()
        rect = image.get_rect()
        rect.center = board_mapping[gametile.tile_id]
        tile_sprites.append((image, rect))

    return tile_sprites


def main_game_loop(**kwargs):
    GAME_RUNNING = True

    pprint(board)

    while GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                GAME_RUNNING = False
            elif event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        screen.fill(Color("grey"))

        for img, rect in tile_sprites:
            screen.blit(img, rect)
        # screen.blit(bg_img, bg_rect)

        pygame.display.update()
    pygame.quit()
    # this is a comment


if __name__ == "__main__":
    tile_sprites = setup()
    main_game_loop(
        tile_sprites=tile_sprites
    )
