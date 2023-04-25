import math
import os
import random
import sys
from pprint import pprint
import pygame
from pygame.locals import *  # pylint: disable=unused-wildcard-import wildcard-import # nopep8 E501
from hexgrid import legal_tile_ids
from src.button import ButtonHex, ButtonRect
from src.bank import Bank
from src.development_cards import DevelopmentCards
import webbrowser
from src.player import Player


from src.tiles import GameTile, ResourceTile
from src.utils import ASSET_DIR

from pdf2image import convert_from_path

# pylint: disable=redefined-outer-name

# Initialize pygame
pygame.init()  # pylint: disable=no-member

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1450, 800
NUM_FONT = pygame.font.SysFont('Palatino', 40)
WORD_FONT = pygame.font.SysFont('Palatino', 25)
GAME_LOG_FONT = pygame.font.SysFont('calibri', 25)


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.DOUBLEBUF)
bg_img = pygame.image.load(os.path.join(ASSET_DIR, "tile_order.png"))
bg_img.convert()
bg_rect = bg_img.get_rect()


NUM_PLAYERS = 6
players = []
bank = Bank()
current_turn_number = 0
node_buttons = []  # list of ButtonHex objects for nodes
tile_buttons = []  # list of ButtonHex object for tiles
built_roads = []  # list of roads built (s_node, e_node, player_owner)
built_settlements = []  # list of settlements built (node, player_owner)
built_cities = []  # list of cities built(node, player_owner)
game_log = []  # list for storing game events as strings
dice_rolled = []


settlement_img_path = os.path.join(
    'src', 'assets', 'buildings', 'settlement.png')
settlement_img = pygame.image.load(settlement_img_path)
settlement_img = pygame.transform.scale(settlement_img, (50, 50))
city_img_path = os.path.join('src', 'assets', 'buildings', 'city.png')
city_img = pygame.image.load(city_img_path)
city_img = pygame.transform.scale(city_img, (50, 50))

GRAY = (158, 153, 134)
BACKGROUND = (235, 235, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)
GREEN = (0, 204, 0)
colors = [(255, 0, 0), (25, 255, 25), (255, 255, 77), (255, 153, 51),
          (0, 0, 0), (35, 219, 222)]  # colors r g y o b c


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


def setup():
    """
    Sets up the initial catan board positions and the ids for each tile

    Returns:
        board: List of tile objects
        tile_sprites: list of images for each tile
        board_mapping: dictionary that maps the tile
        object to an id and nodes to respective coordinates.
    """
    # maps the tile_id to the x, y, coordinates for the screen

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


    


def mouse_motion_event():
    mouse_pos = pygame.mouse.get_pos()
    global mouse_hovering
    mouse_hovering = False
    for button in node_buttons:
        if button.is_hovered_over(mouse_pos):
            mouse_hovering = True
            break
    for button in tile_buttons:
        if button.is_hovered_over(mouse_pos):
            mouse_hovering = True
            break

    if build_road_btn.is_hovered_over(mouse_pos):
        mouse_hovering = True
    elif build_city_btn.is_hovered_over(mouse_pos):
        mouse_hovering = True
    elif build_settlement_btn.is_hovered_over(mouse_pos):
        mouse_hovering = True
    elif make_trade_btn.is_hovered_over(mouse_pos):
        mouse_hovering = True
    elif dev_card_btn.is_hovered_over(mouse_pos):
        mouse_hovering  = True
    elif bank_inventory_btn.is_hovered_over(mouse_pos):
        mouse_hovering = True


    pygame.display.flip()


def click_event(_event, player, special_round=False):  # _ as not used yet
    
    mouse_pos = pygame.mouse.get_pos()

    for button in tile_buttons:
        if button.is_clicked(mouse_pos):
            print(print(f'{button.x_pos}, {button.y_pos} clicked!'))
            break

    if build_road_btn.is_clicked(mouse_pos):
        road_cost = {ResourceTile.HILLS.generate_resource():1,
                    ResourceTile.FOREST.generate_resource():1}
        
        for resource, quantity in road_cost.items(): # check to see if player has enough resources

            if resource not in player.resources or player.resources[resource] < quantity:
                game_log.append("Not enough resources!")
                return None
        start_node = build_road()
        end_node = build_road()
        if is_adjacent(start_node, end_node):
            # check to see if nodes selected are adjacent
            built_roads.append((start_node, end_node, player))

            player.build_road(start_node, end_node)
            pygame.display.update()
            game_log.append((f'{player.name} built road!'))

    elif build_settlement_btn.is_clicked(mouse_pos):
        settlement_cost = {ResourceTile.HILLS.generate_resource(): 1, 
                            ResourceTile.PASTURE.generate_resource(): 1,
                            ResourceTile.FOREST.generate_resource(): 1,
                            ResourceTile.FIELDS.generate_resource(): 1
                            }
        for resource, quantity in settlement_cost.items():
                
            if resource not in player.resources or player.resources[resource] < quantity:
                game_log.append("Not enough resources!")
                return None
        node = build_settlement(player)
        player.build_settlement(node)
        built_settlements.append(((node.x_pos - 20, node.y_pos - 30), player))
        game_log.append(f'{player.name} built settlement!')

    elif build_city_btn.is_clicked(mouse_pos):
        city_cost = {ResourceTile.MOUNTAIN.generate_resource(): 3, 
                    ResourceTile.PASTURE.generate_resource(): 2}
        for resource, quantity in city_cost.items():
                
            if resource not in player.resources or player.resources[resource] < quantity:
                game_log.append("Not enough resources!")
                return None

        if build_settlement(player, city=True) == None:
            game_log.append("Node needs a settlement before a city can be placed")
            return None
        else:
            node = build_settlement(player, city=True)
            player.build_city(node)
            built_cities.append(((node.x_pos - 20, node.y_pos - 30), player))
            game_log.append(f'{player.name} built city!')
    elif make_trade_btn.is_clicked(mouse_pos):
        trade_open = True
        player_buttons, trade_surface = draw_trade_screen(player)
        while trade_open:
        
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mouse_pos = pygame.mouse.get_pos()
                    if not trade_surface.get_rect().collidepoint(event.pos):
                        return
                    else:
                        for button, player in player_buttons:
                            mouse_pos = pygame.mouse.get_pos()
                            if button.is_clicked(mouse_pos):
                                offered_player = player
                                offered_player_text = WORD_FONT.render(f"{offered_player.name}'s Resources", True, BLACK)
                                offered_player_rect = offered_player_text.get_rect(topleft = (450, 100))
                                trade_surface.blit(offered_player_text, offered_player_rect)
                                

                                resource_y = 150
                                for resource, quantity in offered_player.resources.items():
                                    resource_text = WORD_FONT.render(f'{resource}: {quantity}', True, BLACK)
                                    resource_rect = resource_text.get_rect(topleft = (400, resource_y))
                                    trade_surface.blit(resource_text, resource_rect)
                                    resource_y+=30

                                pygame.display.flip()
                elif event.type == pygame.MOUSEMOTION:
                    print(event.pos)
                    mouse_hovering = False
                    for button, player in player_buttons:
                    
                        mouse_pos = pygame.mouse.get_pos()
                        if button.is_hovered_over(mouse_pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                pygame.display.flip()
            
    elif dev_card_btn.is_clicked(mouse_pos):
        print('other button 1 clicked')
    
    
    
    elif bank_inventory_btn.is_clicked(mouse_pos):
        bank_surface, resource_buttons = draw_bank_inventory(player) # opens new screen where it shows inventory of player
        bank_open = True

        while bank_open:
        
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not bank_surface.get_rect().collidepoint(event.pos):
                        bank_open = False
                    else:
                        for button in resource_buttons:
                            pass

                elif event.type == pygame.MOUSEMOTION:
                    mouse_motion_event()
                pygame.display.flip()
            

            

            

        pygame.display.flip()

# pylint: disable=too-many-nested-blocks
def build_settlement(player, city=False):
    """places a settlement at the 

    :param player: _description_
    :type player: _type_
    :param city: _description_, defaults to False
    :type city: bool, optional
    :return: _description_
    :rtype: _type_
    """
    while True:
        for event in pygame.event.get():  # pylint: disable=no-member
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member # nopep8 E501
                mouse_pos = pygame.mouse.get_pos()
                for button in node_buttons:
                    if button.is_clicked(mouse_pos):
                        if city and not button.has_settlement:
                            return None
                        # give player vp 
                        if city:
                            player.victory_points += 2
                            # add 2 vp if player builds a city
                        else:
                            player.victory_points += 1
                            button.has_settlement = True
                        return button


def build_road():
    """handles the logic after the player clicks the build road button

    :return: node that the player clicked
    :rtype: ButtonHex
    """
    while True:
        for event in pygame.event.get():  # pylint: disable=no-member
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member # nopep8 E501
                mouse_pos = pygame.mouse.get_pos()
                for button in node_buttons:
                    if button.is_clicked(mouse_pos):
                        return button


def check_player_won(player):
    """checks to see if current player has enough vp to win game 

    Method is called at the end of the current players turn

    :return: True if player vp value is equal or above 10, else False
    :rtype: boolean
    """
    
    if player.victory_points >= 10:
        return True

    return False




# pylint: disable=inconsistent-return-statements
def calc_mouse_node(mouse_pos):
    '''
    calculates and returns the node mouse is hovering over

    Args:
        mouse_pos: x, y coordinates of the mouse click

    Returns:
        Node_id
    '''
    for node_id, node_point in board_mapping['nodes'].items():
        pos_1 = node_point[0] - mouse_pos[0]
        pos_2 = node_point[1] - mouse_pos[1]
        if (pos_1**2 + pos_2**2)**0.5 < 10:
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND)  # pylint: disable=no-member
            return node_id

    pygame.mouse.set_cursor(
        pygame.SYSTEM_CURSOR_ARROW)  # pylint: disable=no-member

# pylint: disable=inconsistent-return-statements
def calc_mouse_pos_tile(mouse_pos):
    """
    returns the tile that the mouse has clicked in

    Args:
        mouse_pos: x, y coordinates of the mouse click

    Returns:
        tile object from the tiles class
    """
    x_pos, y_pos = mouse_pos
    hex_length = math.dist((621, 318), (699, 187))

    for tile_id in board_mapping['tiles']:
        coords = board_mapping['tiles'][tile_id]
        # dist between mouse click and center of tile
        dist = math.sqrt((coords[0] - x_pos)**2 + (coords[1] - y_pos)**2)
        radius = hex_length * math.sqrt(3) / 2

        # if the distance is less than or equal to the radius
        # the mouse click falls within the tile
        if dist <= radius:
            return board[tile_id - 1]


def convert_to_nodeid(x_pos, y_pos):
    # converts the x, y coords of the
    # node button to the nodeid stored in board_mapping
    for node_id, node_points in board_mapping['nodes'].items():
        if node_points[0] == x_pos and node_points[1] == y_pos:
            return node_id

    return None


def calc_longest_road():
    for road in built_roads:
        road[2].total_road_num += 1
    # calculate who has highest total_road_num value
    highest = 0
    for player in players:
        if player.total_road_num > highest:
            highest = player.total_road_num
    for player in players:
        if player.total_road_num == highest:
            player.has_longest_road = True

    return player




# pylint: disable=redefined-argument-from-local
def draw_buildings(city=False):
    if city:
        for settlement in built_settlements:

            # Replace with the desired highlight color
            highlight_color = settlement[1].color
            # Replace with the desired highlight opacity (0 to 255)
            highlight_alpha = 0
            # Create a transparent surface
            highlight_overlay = pygame.Surface(settlement_img.get_size(),
                                               pygame.SRCALPHA)  # pylint: disable=no-member # nopep8 E501
            # Fill the surface with the highlight color and opacity
            highlight_overlay.fill(
                (highlight_color[0],
                 highlight_color[1],
                 highlight_color[2],
                 highlight_alpha
                 ))
            screen.blit(settlement_img, settlement[0])
            screen.blit(highlight_overlay, settlement[0])
    else:
        for city in built_cities:

            # Replace with the desired highlight color
            highlight_color = city[1].color
            # Replace with the desired highlight opacity (0 to 255)
            highlight_alpha = 0
            # Create a transparent surface
            highlight_overlay = pygame.Surface(city_img.get_size(),
                                               pygame.SRCALPHA)  # pylint: disable=no-member # nopep8 E501
            # Fill the surface with the highlight color and opacity
            highlight_overlay.fill(
                (highlight_color[0],
                 highlight_color[1],
                 highlight_color[2],
                 highlight_alpha
                 ))
            screen.blit(city_img, city[0])
            screen.blit(highlight_overlay, city[0])

def draw_dice(screen, roll_1, roll_2): 

    dice_size = 80

    side_1_p = os.path.join('src','assets','dice','1_sided.jpg')
    side_2_p = os.path.join('src','assets','dice','2_sided.jpg')
    side_3_p = os.path.join('src','assets','dice','3_sided.jpg')
    side_4_p = os.path.join('src','assets','dice','4_sided.jpg')
    side_5_p = os.path.join('src','assets','dice','5_sided.jpg')
    side_6_p = os.path.join('src','assets','dice','6_sided.jpg')
    side_1 = pygame.image.load(side_1_p)
    side_2 = pygame.image.load(side_2_p)
    side_3 = pygame.image.load(side_3_p)
    side_4 = pygame.image.load(side_4_p)
    side_5 = pygame.image.load(side_5_p)
    side_6 = pygame.image.load(side_6_p)

    # scaling all to the same size
    side_1 = pygame.transform.scale(side_1, (dice_size, dice_size))
    side_2 = pygame.transform.scale(side_2, (dice_size, dice_size))
    side_3 = pygame.transform.scale(side_3, (dice_size, dice_size))
    side_4 = pygame.transform.scale(side_4, (dice_size, dice_size))
    side_5 = pygame.transform.scale(side_5, (dice_size, dice_size))
    side_6 = pygame.transform.scale(side_6, (dice_size, dice_size))

    if roll_1 == 1:
        screen.blit(side_1, (10, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_1 == 2:
        screen.blit(side_2, (10, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_1 == 3:
        screen.blit(side_3, (10, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_1 == 4:
        screen.blit(side_4, (10, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_1 == 5:
        screen.blit(side_5, (10, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_1 == 6:
        screen.blit(side_6, (10, DISPLAY_HEIGHT - 90))
        pygame.display.update()

    if roll_2 == 1:
        screen.blit(side_1, (130, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_2 == 2:
        screen.blit(side_2, (130, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_2 == 3:
        screen.blit(side_3, (130, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_2 == 4:
        screen.blit(side_4, (130, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_2 == 5:
        screen.blit(side_5, (130, DISPLAY_HEIGHT - 90))
        pygame.display.update()
    elif roll_2 == 6:
        screen.blit(side_6, (130, DISPLAY_HEIGHT - 90))
        pygame.display.update()

    pygame.display.update()



def draw_trade_screen(current_player):
    """draws a trading display over the window

    Method is called if the current player has clicked the make tradebutton

    :return: None
    :rtype: None
    """

    
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    trade_surface = pygame.Surface((800, 600))
    trade_surface.fill((WHITE))
    offered_player = None

    prompt_text = WORD_FONT.render("Pick a player to trade with", True, BLACK)
    prompt_rect = prompt_text.get_rect(center = (400,450))
    trade_surface.blit(prompt_text, prompt_rect)

    
    player_name_x = 50
    player_buttons = []
    for player in players:
        if player.name != current_player.name:
            player_name_btn = ButtonRect((player_name_x, 500),
                                         (70, 40),
                                         (player.name, WORD_FONT, WHITE), 
                                         (player.color, WHITE))
            player_name_btn.draw(trade_surface)
            player_buttons.append((player_name_btn, player))
            player_name_x+=150

    
    title_text = WORD_FONT.render("Trade with another player", True, BLACK)
    title_rect = title_text.get_rect(center=(400, 50))
    trade_surface.blit(title_text, title_rect)

    player_text = WORD_FONT.render("Your resources", True, BLACK)
    player_rect = player_text.get_rect(topleft = (100,100))
    trade_surface.blit(player_text, player_rect)

    # create resource labels for current players resources
    resource_y = 150
    for resource, quantity in current_player.resources.items():
        resource_text = WORD_FONT.render(f'{resource}: {quantity}', True, BLACK)
        resource_rect = resource_text.get_rect(topleft = (150, resource_y))
        trade_surface.blit(resource_text, resource_rect)
        resource_y+=30
    
    resource_y = 150
    
    screen.blit(trade_surface, (50,50))
    return player_buttons, trade_surface


def draw_bank_inventory(player):
    """draws a inventory display over the window

    Method is called if the current player has clicked the check inventory button
    will show the inventory of the current player only

    :return: None
    :rtype: None
    """

    bank_surface = pygame.Surface((800, 600))
    bank_surface.fill((WHITE))
    resource_buttons =[]

    title_text = WORD_FONT.render("Bank Inventory", True, BLACK)
    title_rect = title_text.get_rect(center=(400, 50))
    bank_surface.blit(title_text, title_rect)


    for index, (resource, quantity) in enumerate(bank.resources.items()):
        text_x = 350
        text_y = 100 +(index*30)
        button = ButtonRect((text_x, text_y),
                                           (50,20),
                                           (f'{resource.name()}: {quantity}', WORD_FONT, BLACK),
                                           (WHITE, WHITE))
    
        resource_buttons.append(button)
        button.draw(bank_surface)

    screen.blit(bank_surface, (0,0))
    



    return bank_surface, resource_buttons

def popup():
    '''
    screen that contains the buttons for functionality
    '''

    popup_width = 630
    popup_height = 160

    popup_rect = pygame.Rect(810, 620, popup_width, popup_height)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect)

    build_road_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (830, 640),
        (190, 40),
        ('Build Road', WORD_FONT, WHITE),
        ((17, 104, 245), WHITE))
    build_road_btn.draw(screen)
    build_settlement_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (830, 700),
        (190, 40),
        ('Build Settlement', WORD_FONT, WHITE),
        ((38, 140, 31), WHITE))
    build_settlement_btn.draw(screen)
    build_city_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (1030, 640),
        (190, 40),
        ('Build City', WORD_FONT, WHITE),
        ((181, 186, 43), WHITE))
    build_city_btn.draw(screen)

    make_trade_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (1030, 700),
        (190, 40),
        ('Make Trade', WORD_FONT, WHITE),
        ((255, 51, 153), WHITE))
    make_trade_btn.draw(screen)

    dev_card_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (1230, 640),
        (190, 40),
        ('Development Card', WORD_FONT, WHITE),
        ((51, 153, 255), WHITE))
    dev_card_btn.draw(screen)

    bank_inventory_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (1230, 700),
        (190, 40),
        ('Bank', WORD_FONT, WHITE),
        ((255, 153, 51), WHITE))
    bank_inventory_btn.draw(screen)
    

    return (build_road_btn,
            build_settlement_btn,
            build_city_btn,
            make_trade_btn,
            dev_card_btn,
            bank_inventory_btn)

(build_road_btn,
 build_settlement_btn,
 build_city_btn,
 make_trade_btn,
 dev_card_btn,
 bank_inventory_btn) = popup()



class StartMenu:
    def __init__(self, current_state):
        self.start_button_rect = pygame.Rect(200,600, 200, 100)
        self.start_button_text = WORD_FONT.render("Start Game", True, BLACK)
        self.rule_book_button_rect = pygame.Rect(500, 600, 200, 100 )
        self.rule_book_button_text = WORD_FONT.render("Rules", True, BLACK)
        self.input_box = pygame.Rect(DISPLAY_WIDTH//2-200, DISPLAY_HEIGHT//2+50, 400, 50)
        self.current_state = current_state
        self.text = ''
        self.type_active = False # flag to see if player clicked on input box
    
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    print("clicked!")
                    self.current_state = MainGameState(players[0])
                    
                if self.rule_book_button_rect.collidepoint(event.pos):
                    webbrowser.open('https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf')
                if self.input_box.collidepoint(event.pos):
                    self.type_active = True
                else:
                    self.type_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.text:
                        player = Player(self.text, colors[len(players)])
                        players.append(player)
                        self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
    
    def draw(self, screen):
        
        WELCOME_FONT = pygame.font.SysFont("Algerian", 100, True)
        WORD_FONT = pygame.font.SysFont('Palatino', 40)

        background_img = pygame.image.load('src\\assets\\images\\start-menu-background.jpg')
        background_img  = pygame.transform.scale(background_img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        screen.blit(background_img, (0,0))

        welcome_text_surface = WELCOME_FONT.render("Welcome to disabled Catan!", True, BLACK)
        welcome_text_rect = pygame.Rect(100, 20, 500, 300)
        screen.blit(welcome_text_surface, welcome_text_rect)

        input_text_surface = WORD_FONT.render(self.text, True, BLACK)
        pygame.draw.rect(screen, WHITE, self.input_box, 2)
        screen.blit(input_text_surface, (self.input_box.x+5, self.input_box.y+5))

        for i, player in enumerate(players):
            player_text = f'Player {i+1}: {player.name}'
            text_surface = WORD_FONT.render(player_text, True, WHITE, player.color)
            text_rect = text_surface.get_rect(center=(DISPLAY_WIDTH-150, 500+i*50))
            screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0,255,0), self.start_button_rect)
        screen.blit(self.start_button_text, (self.start_button_rect.x, self.start_button_rect.y))

        pygame.draw.rect(screen, WHITE, self.rule_book_button_rect)
        screen.blit(self.rule_book_button_text, (self.rule_book_button_rect.x, self.rule_book_button_rect.y))

        pygame.display.flip()

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        if isinstance(self.current_state, MainGameState):
            return MainGameState(players[0])
        
        
        

class MainGameState:
    def __init__(self, player):
        # TODO check if restart is true. if so re-initialize all values to there start values, else maintain.
        self.current_turn_number = 0
        self.current_player = player
        self.bank = Bank()
        self.players = players
        self.current_state = None
        self.build_road_btn = ButtonRect(  # pylint: disable=redefined-outer-name
        (830, 640),
        (190, 40),
        ('Build Road', WORD_FONT, WHITE),
        ((17, 104, 245), WHITE))
        
        self.build_settlement_btn = ButtonRect(  # pylint: disable=redefined-outer-name
            (830, 700),
            (190, 40),
            ('Build Settlement', WORD_FONT, WHITE),
            ((38, 140, 31), WHITE))
        
        self.build_city_btn = ButtonRect(  # pylint: disable=redefined-outer-name
            (1030, 640),
            (190, 40),
            ('Build City', WORD_FONT, WHITE),
            ((181, 186, 43), WHITE))
        

        self.make_trade_btn = ButtonRect(  # pylint: disable=redefined-outer-name
            (1030, 700),
            (190, 40),
            ('Make Trade', WORD_FONT, WHITE),
            ((255, 51, 153), WHITE))
        

        self.dev_card_btn = ButtonRect(  # pylint: disable=redefined-outer-name
            (1230, 640),
            (190, 40),
            ('Development Card', WORD_FONT, WHITE),
            ((51, 153, 255), WHITE))
    

        self.bank_inventory_btn = ButtonRect(  # pylint: disable=redefined-outer-name
            (1230, 700),
            (190, 40),
            ('Bank', WORD_FONT, WHITE),
            ((255, 153, 51), WHITE))
        
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.make_trade_btn.is_clicked(event.pos):
                    self.current_state = ChooseTradePartner(self.current_player)
                if self.build_settlement_btn.is_clicked(event.pos):
                    self.current_state = Build(self.current_player, is_city=False)
                if self.dev_card_btn.is_clicked(event.pos):
                    
                    self.current_state = DevelopmentCardState(self.current_player)
                if self.bank_inventory_btn.is_clicked(event.pos):
                    
                    self.current_state = BankTrade(self.player, self.current_state)
                if self.build_city_btn.is_clicked(event.pos):
                    
                    self.current_state = Build(self.current_player,is_city=True)
                if self.build_road_btn.is_clicked(event.pos):
                    self.current_state = RoadBuildState(self.current_player)
                for node_button in node_buttons:
                    if node_button.is_clicked(event.pos):
                        pass
                for tile_button in tile_buttons:
                    if tile_button.is_clicked(event.pos):
                        pass
            elif event.type == pygame.K_SPACE:
                # TODO new turn logic
                pass
                
                
                
    
    def draw(self, screen):
        """
        Draws the pygame display
        """
        print("drawing")
        
        screen.fill(BACKGROUND)

        for img, rect in tile_sprites:
            screen.blit(img, rect)
            # screen.blit(bg_img, bg_rect)

        for tile_number, coordinates in board_mapping['tiles'].items():
            # Create text surface
            text_surface = NUM_FONT.render(
                str(board[tile_number - 1].real_number), True, WHITE)

            # Get size of text surface
            text_width, text_height = text_surface.get_size()

            # Calculate position to center text on tile
            x_pos = coordinates[0] - text_width // 2
            y_pos = coordinates[1] - text_height // 2

            # Draw text on screen
            screen.blit(text_surface, (x_pos, y_pos))

        self.draw_lines()
        self.draw_scoreboard(self.current_player )
        self.draw_buttons()
        self.draw_dice(1,1)

        self.bank_inventory_btn.draw(screen)
        self.build_city_btn.draw(screen)
        self.build_road_btn.draw(screen)
        self.build_settlement_btn.draw(screen)
        self.dev_card_btn.draw(screen)
        self.make_trade_btn.draw(screen)


    def draw_lines(self):
        for tile in board:
            pygame.draw.line(screen,
                            'white',
                            board_mapping['nodes'][tile.node_coord_n],
                            board_mapping['nodes'][tile.node_coord_nw], 5)

            pygame.draw.line(screen,
                            'white',
                            board_mapping['nodes'][tile.node_coord_n],
                            board_mapping['nodes'][tile.node_coord_ne], 5)

            pygame.draw.line(screen,
                            'white',
                            board_mapping['nodes'][tile.node_coord_nw],
                            board_mapping['nodes'][tile.node_coord_sw], 5)

            pygame.draw.line(screen,
                            'white',
                            board_mapping['nodes'][tile.node_coord_sw],
                            board_mapping['nodes'][tile.node_coord_s], 5)

            pygame.draw.line(screen,
                            'white',
                            board_mapping['nodes'][tile.node_coord_s],
                            board_mapping['nodes'][tile.node_coord_se], 5)

            pygame.draw.line(screen,
                            'white',
                            board_mapping['nodes'][tile.node_coord_se],
                            board_mapping['nodes'][tile.node_coord_ne], 5)
            
    def draw_scoreboard(self, player_turn):
        rect_width = DISPLAY_WIDTH - 800
        rect_height = DISPLAY_HEIGHT

        rect_x = DISPLAY_WIDTH - rect_width
        rect_y = 0
        # create the rectangular surface
        rect_surf = pygame.Surface((rect_width, rect_height))
        rect_surf.fill((0, 120, 255))  # fill with blue color

        screen.blit(rect_surf, (rect_x, rect_y))

        rect_outline_width = 6
        scoreboard_width = rect_width - 20
        scoreboard_outline = pygame.Rect(10, 10, scoreboard_width, 600)

        pygame.draw.rect(rect_surf, WHITE, scoreboard_outline, rect_outline_width)
        pygame.draw.line(rect_surf, WHITE, (10, 80), (rect_width - 10, 80), 6)
        pygame.draw.line(rect_surf, WHITE, (10, 160), (rect_width - 10, 160), 6)
        pygame.draw.line(rect_surf, WHITE, (10, 430),
                        (rect_width - 10, 430), 6)  # space for gamelog

        player_width = scoreboard_width // NUM_PLAYERS
        font_size = 20 if len(players) == 6 else 30 if len(players) == 5 else 40
        player_font = pygame.font.SysFont('Palatino', font_size)

        for i in range(len(players)):  # draw player names at top of scoreboard
            x_pos = 10 + i * player_width
            pygame.draw.line(rect_surf, WHITE, (x_pos, 10),
                            (x_pos, 430), rect_outline_width)
            name = player_font.render(players[i].name, True, WHITE)
            name_rect = name.get_rect(center=(x_pos + player_width // 2, 40))
            rect_surf.blit(name, name_rect)

        for i in range(len(players)):  # draw victory points
            x_pos = 10 + i * player_width  # in each cell below player names
            pygame.draw.line(rect_surf, WHITE, (10, 510),
                            (rect_width - 10, 510), 6)
            name = player_font.render(
                f'VP: {players[i].victory_points}',
                True, WHITE)
            name_rect = name.get_rect(center=(x_pos + player_width // 2, 120))
            rect_surf.blit(name, name_rect)

        for i in range(len(game_log)):  # draws game log text
            game_log_text = game_log[-1]  # most recent event
            game_log_text = WORD_FONT.render(game_log_text, True, WHITE)
            rect_surf.blit(game_log_text, (50, 460))
            screen.blit(rect_surf, (rect_x, rect_y))

        # player turn text being drawn
        player_turn_text = WORD_FONT.render(f'Current turn: {player_turn.name}',
                                            True, WHITE)
        rect_surf.blit(player_turn_text, (250, 540))
        screen.blit(rect_surf, (rect_x, rect_y))
    
    def draw_buttons(self):
        button_radius = [10, 22]
        # draw node buttons
        for _node_id, node_point in board_mapping['nodes'].items():
            button = ButtonHex(
                (node_point[0], node_point[1]),
                button_radius[0],
                GRAY)
            button.draw(screen)
            node_buttons.append(button)

        for _node_id, node_point in board_mapping['tiles'].items():
            button = ButtonHex(
                (node_point[0], node_point[1]),
                button_radius[1],
                WHITE, False)
            tile_buttons.append(button)
            # invisible buttons at center of tiles
    
    def draw_dice(self, roll_1, roll_2): # TODO add to MainGame state

        dice_size = 80

        side_1_p = os.path.join('src','assets','dice','1_sided.jpg')
        side_2_p = os.path.join('src','assets','dice','2_sided.jpg')
        side_3_p = os.path.join('src','assets','dice','3_sided.jpg')
        side_4_p = os.path.join('src','assets','dice','4_sided.jpg')
        side_5_p = os.path.join('src','assets','dice','5_sided.jpg')
        side_6_p = os.path.join('src','assets','dice','6_sided.jpg')
        side_1 = pygame.image.load(side_1_p)
        side_2 = pygame.image.load(side_2_p)
        side_3 = pygame.image.load(side_3_p)
        side_4 = pygame.image.load(side_4_p)
        side_5 = pygame.image.load(side_5_p)
        side_6 = pygame.image.load(side_6_p)

        # scaling all to the same size
        side_1 = pygame.transform.scale(side_1, (dice_size, dice_size))
        side_2 = pygame.transform.scale(side_2, (dice_size, dice_size))
        side_3 = pygame.transform.scale(side_3, (dice_size, dice_size))
        side_4 = pygame.transform.scale(side_4, (dice_size, dice_size))
        side_5 = pygame.transform.scale(side_5, (dice_size, dice_size))
        side_6 = pygame.transform.scale(side_6, (dice_size, dice_size))

        if roll_1 == 1:
            screen.blit(side_1, (10, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_1 == 2:
            screen.blit(side_2, (10, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_1 == 3:
            screen.blit(side_3, (10, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_1 == 4:
            screen.blit(side_4, (10, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_1 == 5:
            screen.blit(side_5, (10, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_1 == 6:
            screen.blit(side_6, (10, DISPLAY_HEIGHT - 90))
            pygame.display.update()

        if roll_2 == 1:
            screen.blit(side_1, (130, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_2 == 2:
            screen.blit(side_2, (130, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_2 == 3:
            screen.blit(side_3, (130, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_2 == 4:
            screen.blit(side_4, (130, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_2 == 5:
            screen.blit(side_5, (130, DISPLAY_HEIGHT - 90))
            pygame.display.update()
        elif roll_2 == 6:
            screen.blit(side_6, (130, DISPLAY_HEIGHT - 90))
            pygame.display.update()

        pygame.display.update()

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
            

class DevelopmentCardState:
    def __init__(self, player):
        self.player = player
        self.card_bought = False
        self.card_image = False
        self.current_state = None
        self.card_images = {DevelopmentCards.KNIGHT: (pygame.image.load('src\\assets\\Development\\knight.jpg'), pygame.Rect(300, 50, 100, 150)),
                            DevelopmentCards.VP: (pygame.image.load('src\\assets\\Development\\palace.jpg'), pygame.Rect(700, 50, 100, 150))}                                                            
        
    
    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for card, (image, rect) in self.card_images.items():
                    if rect.collidepoint(mouse_pos):
                        self.player.buy_dev_card(card.name())
                        print(f'{card.name()} bought')
                        self.current_state = MainGameState(self.player)

    def draw(self, screen):
        screen.fill(WHITE)
        
        for card, (image, rect) in self.card_images.items():
            image = pygame.transform.scale(image, (300, 300))
            rect = pygame.Rect(rect.x, rect.y, image.get_width(), image.get_height())
            screen.blit(image, rect)

            cost_text = WORD_FONT.render(f'cost', True, BLACK)
            cost_rect = cost_text.get_rect(center=(rect.x+50, 370))
            screen.blit(cost_text, cost_rect)

            y_offset = 400
            for resource, quantity in card.cost().items():
                text = WORD_FONT.render(f'{resource} : {quantity}', True, BLACK)
                text_rect = text.get_rect(center=(rect.x+50, y_offset))
                screen.blit(text, text_rect)
                y_offset += 50

        back_button_rect = pygame.Rect(1100, 600, 400, 200)

        font_size = min(100, int(back_button_rect.height * 0.8)) # sets font size to be 80% size of recatngle
        font = pygame.font.SysFont('Palatino', font_size)

        back_button_text = font.render("Back", True, BLACK, RED)
        screen.blit(back_button_text, back_button_rect)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state

    
class Build:
    def __init__(self, player, is_city):
        self.player = player
        self.is_city = is_city
        self.node = None
        self.current_state = None

    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node_button in node_buttons:
                    if node_button.is_clicked(event.pos):
                        self.node = node_button
                        if self.has_enough_resources():
                            if self.is_city:
                                self.player.build_city(self.node)
                                screen.blit(city_img, (self.node.x_pos, self.node.y_pos))
                                self.current_state = MainGameState(self.player)
                            else:
                                self.player.build_settlement(self.node)
                                screen.blit(settlement_img, (self.node.x_pos, self.node.y_pos))
                                self.current_state =  MainGameState(self.player)
                        else:
                            self.current_state = MainGameState(self.player)
        

    def has_enough_resources(self):
        if self.is_city:
            city_cost = {ResourceTile.MOUNTAIN.generate_resource(): 3, 
                                    ResourceTile.PASTURE.generate_resource(): 2}
            
            for resource, quantity in city_cost.items():
                
                if resource not in self.player.resources or self.player.resources[resource] < quantity:
                    return
                else: 
                    self.player.build_city(self.node)
                
        else: 
            settlement_cost = {ResourceTile.HILLS.generate_resource(): 1, 
                            ResourceTile.PASTURE.generate_resource(): 1,
                            ResourceTile.FOREST.generate_resource(): 1,
                            ResourceTile.FIELDS.generate_resource(): 1
                            }
            for resource, quantity in settlement_cost.items():
                    
                if resource not in self.player.resources or self.player.resources[resource] < quantity:
                    game_log.append("Not enough resources!")
                    return MainGameState(self.player)
                else:
                    self.player.build_settlement(self.node)
    
    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state

class RoadBuildState:
    def __init__(self, player):
        self.player = player
        self.cost = {ResourceTile.HILLS.generate_resource():1,
                    ResourceTile.FOREST.generate_resource():1}
        self.node_buttons = []
        self.node1 = None
        self.node2 = None
        self.current_state = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('clicked')
                mouse_pos = pygame.mouse.get_pos()
                for node_button in self.node_buttons:
                    
                    if node_button.collidepoint(mouse_pos):
                        print('node clicked')
                        if self.node1 == None:
                            self.node1 = node_button
                            print(f'{self.node1} clicked!')
                        else:
                            if self.is_adjacent(self.node1, node_button):

                                print('road built')
                                self.node2 = node_button
                                
                                self.player.build_road(self.node1, self.node2)
                                
                                self.draw(screen)
                                game_log.append(f'{self.player.name} built road!')
                                pygame.display.flip()
                            else:
                                self.current_state = MainGameState(self.player)
    
    def has_enough_resources(self):
        for resource, quantity in self.road_cost.items(): # check to see if player has enough resources

            if resource not in self.player.resources or self.player.resources[resource] < quantity:
                game_log.append("Not enough resources!")
                return MainGameState(self.player)
            else:
                self.player.build_road(self.node1, self.node2)
                return MainGameState(self.player)
            
    def is_adjacent(self, node1, node2):

        x1_pos, y1_pos = node1.x, node1.y
        x2_pos, y2_pos = node2.x, node2.y

        x_diff = abs(x1_pos - x2_pos)
        y_diff = abs(y1_pos - y2_pos)
        max_road_len = 100  # road lens are diff so this is maximum road len

        print(f'x_diff: {x_diff}')
        print(f'y_diff: {y_diff}')

        # return true if x_diff and y_diff is less than radius of tiles
        return (x_diff <= max_road_len) and (y_diff <= max_road_len)
    
    def draw(self, screen):
        if self.node1 is not None and self.node2 is not None:
            pygame.draw.line(
                    screen,
                    self.player.color,
                    (self.node1.x, self.node1.y),
                    (self.node2.x, self.node2.y),
                    5)
        for button in node_buttons:
            rect = pygame.Rect((button.x_pos, button.y_pos), (button.radius,  button.radius))
            self.node_buttons.append(rect)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
        

class ChooseTradePartner:
    def __init__(self, player):
        self.player = player
        self.current_state = None
        self.trade_partner = None
        self.available_players = []
        self.screen_width, self.screen_height = 800, 800
        
        self.back_button_text = WORD_FONT.render('Back Button', True, WHITE, BLACK)
        self.back_button_rect = self.back_button_text.get_rect()
        self.back_button_rect.center = (300,300)


    def draw(self, screen):
        screen.fill(WHITE)
        self.draw_player_resources(screen)
        self.draw_available_partners(screen)
        screen.blit(self.back_button_text, self.back_button_rect)
        

    def draw_player_resources(self, screen):
        resources = self.player.resources
        y_offset = 60

        for resource, quantity in resources.items():
            button_text = WORD_FONT.render(f'{resource} : {quantity}', True, WHITE, BLACK)
            button_rect = button_text.get_rect(center = (400, y_offset))
            screen.blit(button_text, button_rect)
            y_offset += 50

    
    def draw_available_partners(self, screen):
        y_offset = 60
        for player in players:
            if player.name != self.player.name:
                
                player_name_text = WORD_FONT.render(player.name, True, WHITE, player.color)
                player_rect = player_name_text.get_rect(center=(600, y_offset))
                self.available_players.append((player_rect, player))
                screen.blit(player_name_text, player_rect)
                y_offset +=50


    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if self.back_button_rect.collidepoint(mouse_pos):
                    self.current_state = MainGameState(self.player)
            
            for player in self.available_players:
                if player[0].collidepoint(mouse_pos):
                    self.trade_partner = player[1]
                    self.current_state = ChooseTradeResources(self.player, self.trade_partner)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state  

class ChooseTradeResources:

    def __init__(self, player, trade_partner):
        self.player = player
        self.trade_partner = trade_partner
        self.current_state = None
        self.partner_resources_buttons = []
        self.back_button = None


    def draw(self, screen):
        screen.fill(WHITE)
        self.draw_player_resources(screen)
        self.draw_partner_resources(screen)
        

        back_button_text = WORD_FONT.render("Back", True, WHITE, BLACK)
        back_button_rect = back_button_text.get_rect(center=(700, 700))
        self.back_button = back_button_rect
        screen.blit(back_button_text, back_button_rect)


    def draw_player_resources(self, screen):
        resources = self.player.resources
        y_offset = 100

        player_name_text = WORD_FONT.render(f'Your Resources', True, BLACK)
        player_name_rect = player_name_text.get_rect(center = (DISPLAY_WIDTH//3, 100))
        screen.blit(player_name_text, player_name_rect)

        for resource, quantity in resources.items():
            button_text = WORD_FONT.render(f'{resource} : {quantity}', True, BLACK)
            button_rect = button_text.get_rect(center = (DISPLAY_WIDTH//3, y_offset))
            screen.blit(button_text, button_rect)
            self.partner_resources_buttons.append((button_rect, resource))
            
            y_offset+=50

    def draw_partner_resources(self, screen):
        if self.trade_partner is None:
            return
        resources = self.trade_partner.resources
        y_offset = 100

        for resource, quantity in resources.items():
            button_text = WORD_FONT.render(f'{resource} : {quantity}', True, BLACK)
            button_rect = button_text.get_rect(center = (DISPLAY_WIDTH//2, y_offset))
            screen.blit(button_text, button_rect)
            self.partner_resources_buttons.append((button_rect, resource))
            
            y_offset+=50

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type==pygame.MOUSEBUTTONDOWN:
                for resource_button in self.partner_resources_buttons:
                    if resource_button[0].collidepoint(mouse_pos):
                        self.current_state = ResourceAmountSelection(self.player, self.trade_partner)
                if self.back_button.collidepoint(mouse_pos):
                    self.current_state = ChooseTradePartner(self.player)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
                
class ResourceAmountSelection:
    def __init__(self, player, trade_partner):
        self.player = player
        self.trade_partner = trade_partner
        self.current_state = None
        self.quantity = 0
        self.font = WORD_FONT
        self.text_surface = self.font.render("Choose Amount:", True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=(400,200))
        self.increment_rect = None
        self.decrement_rect = None
        self.back_button_rect = pygame.Rect(10,10,50,50)
        self.back_button_text = WORD_FONT.render("Back", True, WHITE, BLACK)
        self.submit_button_text = WORD_FONT.render("Submit", True, WHITE, GREEN)
        self.submit_button_rect = self.submit_button_text.get_rect(center=(700,700))

        self.submit_button_text = pygame.transform.scale(self.submit_button_text, (self.submit_button_rect.width *5, self.submit_button_rect.height*5))

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.text_surface, self.text_rect)

        quantity_surface = self.font.render(str(self.quantity), True, (0, 0, 0))
        quantity_rect = quantity_surface.get_rect(center=(400, 250))
        screen.blit(quantity_surface, quantity_rect)

        increment_surface = self.font.render("+", True, (0, 0, 0))
        self.increment_rect = increment_surface.get_rect(center=(500, 250))
        decrement_surface = self.font.render("-", True, (0, 0, 0))
        self.decrement_rect = decrement_surface.get_rect(center=(300, 250))
        screen.blit(increment_surface, self.increment_rect)
        screen.blit(decrement_surface, self.decrement_rect)

        pygame.draw.rect(screen, BLACK, self.back_button_rect)
        screen.blit(self.back_button_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 10))

        pygame.draw.rect(screen, BLACK, self.submit_button_rect)
        screen.blit(self.submit_button_text, (self.submit_button_rect.x + 10, self.submit_button_rect.y + 10))
    
    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.increment_rect.collidepoint(mouse_pos):
                    self.quantity +=1
                elif self.decrement_rect.collidepoint(mouse_pos):
                    self.quantity-=1
                if self.back_button_rect.collidepoint(mouse_pos):
                    self.current_state =  ChooseTradeResources(self.player, self.trade_partner)
                if self.submit_button_rect.collidepoint(mouse_pos):
                    self.current_state =  AcceptTradeState(self.player, self.current_state)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
                
class AcceptTradeState:
    def __init__(self, player, trade_partner, quantity):
        self.player = player
        self.trade_partner = trade_partner
        self.current_state = None
        self.trade_accepted = False
        self.quantity = quantity
        
        self.accept_rect = pygame.Rect(10, 10, 50, 50)
        self.accept_text = WORD_FONT.render("Accept?", True, GREEN)

        self.decline_rect = pygame.Rect(30, 30, 80, 80)
        self.decline_text = WORD_FONT.render("Decline?", True, RED)

    def draw(self, screen):
        screen.fill(WHITE)
         
        pygame.draw.rect(screen, BLACK, self.accept_rect)
        screen.blit(self.accept_text, (self.accept_rect.x + 10, self.accept_rect.y + 10))

        pygame.draw.rect(screen, BLACK, self.decline_rect)
        screen.blit(self.decline_text, (self.decline_rect.x + 10, self.decline_rect.y + 10))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.accept_rect.collidepoint(event.pos):
                    
                    self.current_state =  MainGameState(self.player)
                else:
                    self.current_state = ChooseTradePartner(self.player)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state


class BuildState:
    def __init__(self, is_city, player):
        self.is_city = is_city
        self.player = player
        self.current_state = None
        self.settlement_cost = {ResourceTile.HILLS.generate_resource(): 1, 
                            ResourceTile.PASTURE.generate_resource(): 1,
                            ResourceTile.FOREST.generate_resource(): 1,
                            ResourceTile.FIELDS.generate_resource(): 1
                            }
        self.city_cost = {ResourceTile.MOUNTAIN.generate_resource(): 3, 
                          ResourceTile.PASTURE.generate_resource(): 2}
        self.has_enough_resources = False

    def has_enough_resources(self):
        if self.is_city:
            for resource, quantity in self.city_cost.items():
                    
                if resource not in self.player.resources or self.player.resources[resource] < quantity:
                    game_log.append("Not enough resources!")
                    return None
                else:
                    self.has_enough_resources = True
        else:
            for resource, quantity in self.settlement_cost.items():
                    
                if resource not in self.player.resources or self.player.resources[resource] < quantity:
                    game_log.append("Not enough resources!")
                    return None
                else:
                    self.has_enough_resources = True

    def handle_events(self, events):

        for event in events:
            for node_button in node_buttons:
                if node_button.is_clicked(event.pos):
                    if self.has_enough_resources:
                        built_settlements.append(((node_button.x_pos - 20, node_button.y_pos - 30), self.player))
                        game_log.append(f'{self.player.name} built settlement!')
                        self.current_state = MainGameState(self.player, self.current_state)
                    else:
                        game_log.append('Not enough Resources')
                        self.current_state =  MainGameState(self.player, self.current_state)
    
    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state

class EndMenu:
    def __init__(self, players, current_state):
        self.players = players
        self.current_state = current_state
        self.players.sort(key=lambda p:p.victory_points, reverse=True)
        self.main_menu_button_text = WORD_FONT.render("Main Menu", True, BLACK)
        self.main_menu_button_rect = pygame.Rect(400, 600, 200, 200)

    def draw(self, screen):
        screen.fill(WHITE)

        y = 50
        for player in self.players:
            text_surface = WORD_FONT.render(f'{player.name}: {player.victory_points} VP', True, BLACK)
            screen.blit(text_surface, (400, y))
            y+=30
        
        winner_text_surface = WORD_FONT.render(f'Congrats Nerd! {self.players[0].name}')
        screen.blit(winner_text_surface, (400, 700))


        pygame.draw.rect(screen, BLACK, self.main_menu_button_rect)
        screen.blit(self.main_menu_button_rect, self.main_menu_button_text)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_menu_button_rect.collidepoint(event.pos):
                    self.current_state = StartMenu()

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
                



def main_game_loop(**kwargs):  # pylint: disable=unused-argument
    game_running = True
    player_turn_index = 0
    current_turn_number = 0
    
    current_state = None
    while game_running:
        
        events = pygame.event.get()
    
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False
        
        if current_state is not None and current_state.should_transition():
            current_state = current_state.transition()
        
        if current_state is None:
            print("yesse")
            current_state = StartMenu(current_state)

        current_state.handle_events(events)
        current_state.draw(screen)
        #print(current_state)
        
        pygame.display.update()



if __name__ == "__main__":
    tile_sprites, board, board_mapping = setup()
    main_game_loop(
        tile_sprites=tile_sprites,
        board=board,
        board_mapping=board_mapping,
        
    )