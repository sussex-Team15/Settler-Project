import os
import pygame
import random
import math
import time
from colour import Color
from hexgrid import legal_tile_ids
from pprint import pprint
from pygame.locals import *
from tiles import GameTile, ResourceTile
from utils import ASSET_DIR, TILE_CARDS_DIR
from player import Player
from button import *



# Initialize pygame
pygame.init()

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1450, 800
NUM_FONT = pygame.font.SysFont('Palatino', 40)
WORD_FONT = pygame.font.SysFont('Palatino', 25)


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
bg_img = pygame.image.load(os.path.join(ASSET_DIR, "tile_order.png"))
bg_img.convert()
bg_rect = bg_img.get_rect()
num_players = 4
player_names = ['Eddie', 'Morgan', 'Ryan', 'Noah']
node_buttons = [] #list of ButtonHex objects for nodes
tile_buttons = [] #list of ButtonHex object for tiles



WHITE = (255,255,255)
colors = [(255,0,0), (25, 255,25) , (255,255,77), (255,153,51), (0,0,0), (35, 219, 222)] #colors r g y o b c


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
                      random.randint(1,12),
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


    players = []

    for i in range(num_players):
        player = Player(player_names[i], colors[i] )
        print(player.name)
        players.append(player)

    return tile_sprites, board, board_mapping, players


def main_game_loop(**kwargs):
    GAME_RUNNING = True
    player_turn_index= 0
    pprint(board)

    while GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                GAME_RUNNING = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_event(event, players[player_turn_index]) # handles clicking events
            elif event.type == pygame.MOUSEMOTION:
                mouse_motion_event() # function handles mouse motion events 
                
                
            
            
            
            
        
        
        draw()
        pygame.display.update()
    pygame.quit()
    # this is a comment)

def mouse_motion_event():
    mouse_pos = pygame.mouse.get_pos()
    for button in node_buttons:
        button.is_hovered_over(mouse_pos)

    for button in tile_buttons:
        button.is_hovered_over(mouse_pos)
    build_road_button.is_hovered_over(mouse_pos)
    build_city_button.is_hovered_over(mouse_pos)
    build_settlement_button.is_hovered_over(mouse_pos)

    

        
    
def click_event(event, player):
    mouse_pos = pygame.mouse.get_pos()

    for button in node_buttons:
        if button.is_clicked(mouse_pos):
            print(f'{button.x}, {button.y} clicked!')
            break
    
    if build_road_button.is_clicked(mouse_pos):
            # do something
        print('Raod Build!')
    elif build_settlement_button.is_clicked(mouse_pos):
            # do something
        print("settlement build!")
    elif build_city_button.is_clicked(mouse_pos):
        print('city build')


    pygame.display.update()
    

def popup():
    '''
    popup window that gives options for player when node is clicked
    '''
    
    popup_width = 630
    popup_height = 160

    popup_rect = pygame.Rect(810, 620, popup_width, popup_height)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)

    build_road_button = ButtonRect(830, 640, 190, 40,
                              'Build Road', WORD_FONT, WHITE, (17, 104, 245), WHITE)
    build_road_button.draw(screen)
    build_settlement_button = ButtonRect(830, 700, 190, 40,
                              'Build Settlement', WORD_FONT, WHITE,  (38, 140, 31), WHITE)
    build_settlement_button.draw(screen)
    build_city_button = ButtonRect(1030, 640, 190, 40,
                              'Build City', WORD_FONT, WHITE, (181, 186, 43) , WHITE)
    build_city_button.draw(screen)

    
    return build_road_button, build_settlement_button, build_city_button

build_road_button, build_settlement_button, build_city_button = popup()
    
def calc_mouse_node(mouse_pos):
    '''
    calculates and returns the node mouse is hovering over

    Args:
        mouse_pos: x, y coordinates of the mouse click

    Returns:
        Node_id
    '''
    for node_id, node_point in board_mapping['nodes'].items():
                if ((node_point[0] - mouse_pos[0])**2 + (node_point[1] - mouse_pos[1])**2)**0.5 < 10 :
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return node_id
    else:
         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



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

    #draws the catan board
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
        
    for tile_number, coordinates in board_mapping['tiles'].items():
        # Create text surface
        text_surface = NUM_FONT.render(str(board[tile_number-1].real_number), True, WHITE)
    
        # Get size of text surface
        text_width, text_height = text_surface.get_size()
    
        # Calculate position to center text on tile
        x = coordinates[0] - text_width // 2
        y = coordinates[1] - text_height // 2
    
        # Draw text on screen
        screen.blit(text_surface, (x, y))

    
    draw_scoreboard()
    draw_buttons()
    popup()



    

def draw_buttons():
    button_radius = [10, 22]
    GRAY = (158, 153, 134)
    RED = (255,0,0)
    for node_id, node_point in board_mapping['nodes'].items(): #draw node buttons
        button  = ButtonHex(node_point[0], node_point[1], button_radius[0], GRAY)
        button.draw(screen)
        node_buttons.append(button)
    
    for node_id, node_point in board_mapping['tiles'].items():
        button = ButtonHex(node_point[0], node_point[1], button_radius[1], WHITE, isFilled=False)
        button.draw(screen)
        tile_buttons.append(button)


        
def draw_scoreboard():
    """
    Draws the scoreboard as a seperate pygame surface
    """
    rect_width = DISPLAY_WIDTH-800
    rect_height = DISPLAY_HEIGHT

    rect_x = DISPLAY_WIDTH - rect_width
    rect_y = 0
    # create the rectangular surface
    rect_surf = pygame.Surface((rect_width, rect_height))
    rect_surf.fill((0, 120, 255))  # fill with blue color

    screen.blit(rect_surf, (rect_x, rect_y))

    rect_outline_width = 6
    scoreboard_width = rect_width-20
    scoreboard_outline = pygame.Rect(10, 10, scoreboard_width, 600)
    
    

    pygame.draw.rect(rect_surf, WHITE, scoreboard_outline, rect_outline_width)
    pygame.draw.line(rect_surf, WHITE, (10,80), (rect_width-10, 80), 6)

    player_width = scoreboard_width//num_players
    font_size = 20 if len(players)==6 else 30 if len(players)==5 else 40
    player_font = pygame.font.SysFont('Palatino',font_size)

    for i in range(num_players):
        x = 10 + i * player_width
        pygame.draw.line(rect_surf, WHITE, (x, 10), (x, 610), rect_outline_width)
        name =  player_font.render(players[i].name, True, WHITE)
        name_rect = name.get_rect(center=(x + player_width // 2, 40))
        rect_surf.blit(name, name_rect)
    screen.blit(rect_surf,(rect_x, rect_y))

if __name__ == "__main__":
    tile_sprites, board, board_mapping, players = setup()
    main_game_loop(
        tile_sprites=tile_sprites,
        board=board,
        board_mapping=board_mapping,
        players=players
    )
