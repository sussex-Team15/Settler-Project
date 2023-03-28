import os
import pygame
import random
import math
from colour import Color
from hexgrid import legal_tile_ids
from pprint import pprint
from pygame.locals import *
from Tiles import GameTile, ResourceTile
from utils import ASSET_DIR, TILE_CARDS_DIR


# Initialize pygame
pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1450, 800


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
bg_img = pygame.image.load(os.path.join(ASSET_DIR, "tile_order.png"))
bg_img.convert()
bg_rect = bg_img.get_rect()


def setup():
    """
    Sets up the initial catan board positions and the ids for each tile

    Returns:
        board: List of tile objects
        tile_sprites: list of images for each tile
        board_mapping: dictionary that maps the tile object to an id and nodes to respective coordinates.
    """
    # maps the tile_id to the x, y, coordinates for the screen
    board_mapping = {'tiles': {
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
    }, 'nodes': {


        1011: (621, 318),
        1013: (699, 187),
        105: (392, 714),
        107: (472, 589),
        109: (546, 450),
        1110: (622, 410),
        1112: (700, 279),
        116: (468, 671),
        118: (547, 542),
        1211: (696, 450),
        1213: (774, 318),
        127: (546, 719),
        129: (619, 586),
        1310: (699, 540),
        1312: (775, 408),
        138: (625, 675),
        23: (10, 320),
        25: (82, 186),
        27: (163, 55),
        32: (7, 408),
        34: (86, 274),
        36: (162, 140),
        38: (235, 10),
        43: (83, 451),
        45: (160, 316),
        47: (237, 183),
        49: (311, 53),
        510: (389, 11),
        52: (84, 539),
        54: (161, 408),
        56: (236, 276),
        58: (312, 142),
        611: (469, 56),
        63: (161, 579),
        65: (236, 448),
        67: (314, 318),
        69: (391, 185),
        710: (467, 140),
        712: (542, 9),
        72: (159, 672),
        74: (239, 539),
        78: (389, 274),
        811: (546, 185),
        813: (618, 52),
        83: (235, 717),
        85: (314, 589),
        910: (548, 274),
        912: (623, 144),
        94: (318, 673),
        96: (392, 538),
        76: (315, 407),
        87: (393, 449),
        98: (468, 408),
        89: (467, 317),

    }}
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
        rect.center = board_mapping['tiles'][gametile.tile_id]
        tile_sprites.append((image, rect))

    return tile_sprites, board, board_mapping


def main_game_loop(**kwargs):
    GAME_RUNNING = True

    pprint(board)

    while GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                GAME_RUNNING = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                tile = calc_mouse_pos_tile(mouse_pos)
                

        draw()
        pygame.display.update()
    pygame.quit()
    # this is a comment

def calc_mouse_pos_tile(mouse_pos):
    """
    returns the tile that the mouse has clicked in

    Args:
        mouse_pos: x, y coordinates of the mouse click

    Returns:
        tile object from the Tiles class
    """
    x, y = mouse_pos
    hex_length = math.dist((621, 318), (699, 187))

    for tile_id in board_mapping['tiles']:
        coords = board_mapping['tiles'][tile_id]
        dist = math.sqrt((coords[0] - x)**2 + (coords[1] - y)**2) # dist between mouse click and center of tile
        radius = hex_length * math.sqrt(3) / 2
    
         # if the distance is less than or equal to the radius, the mouse click falls within the tile
        if dist <= radius:
            return board[tile_id-1]
            
            

def draw():
    """
    Draws the pygame display
    """
    screen.fill(Color("grey"))

    for img, rect in tile_sprites:
            screen.blit(img, rect)
        # screen.blit(bg_img, bg_rect)

    for index in range(len(board)):
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_N], board_mapping['nodes'][board[index].node_coord_NW], 5)
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_N], board_mapping['nodes'][board[index].node_coord_NE], 5)
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_NW], board_mapping['nodes'][board[index].node_coord_SW], 5)

        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_SW], board_mapping['nodes'][board[index].node_coord_S], 5)

        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_S], board_mapping['nodes'][board[index].node_coord_SE], 5)
        
        pygame.draw.line(screen, 'white', board_mapping['nodes']
                            [board[index].node_coord_SE], board_mapping['nodes'][board[index].node_coord_NE], 5)
        
        draw_scoreboard()
        
def draw_scoreboard():
    """
    Draws the scoreboard as a seperate pygame surface
    """
    rect_width = 600
    rect_height = DISPLAY_HEIGHT
    rect_x = DISPLAY_WIDTH - rect_width
    rect_y = 0

    # create the rectangular surface
    rect_surf = pygame.Surface((rect_width, rect_height))
    rect_surf.fill((0, 0, 255))  # fill with blue color

    # draw the rectangular surface onto the window
    screen.blit(rect_surf, (rect_x, rect_y))
    
    rect_outline_width = 3
    rect_outline_rect = pygame.Rect(rect_x+50, rect_y-100, 300, 300)
    pygame.draw.rect(rect_surf, (255, 255, 255), rect_outline_rect, rect_outline_width)


if __name__ == "__main__":
    tile_sprites, board, board_mapping = setup()
    main_game_loop(
        tile_sprites=tile_sprites,
        board=board,
        board_mapping=board_mapping
    )
