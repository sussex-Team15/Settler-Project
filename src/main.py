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
from src.resource_ import Resource


from src.tiles import GameTile, ResourceTile
from src.utils import ASSET_DIR
from src.ai_player import AIPlayer

# pylint: disable=redefined-outer-name

# Initialize pygame
pygame.init()  # pylint: disable=no-member

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1450, 800
NUM_FONT = pygame.font.SysFont('arial', 40)
WORD_FONT = pygame.font.SysFont('arial', 25)
GAME_LOG_FONT = pygame.font.SysFont('arial', 25)
BIG_FONT = pygame.font.SysFont("arial", 100, True)


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
player_colors = {} 
game_log = []  # list for storing game events as strings
dice_rolled = []
adjacent_nodes = [] #list of all adjacent nodes


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

def create_adjacent_nodes(nodes_dict, adjacent_nodes):
        for node1_id, node1_pos in nodes_dict.items():
            for node2_id, node2_pos in nodes_dict.items():
                if node1_id != node2_id:  # Skip comparison of a node with itself
                    if is_adjacent(node1_id, node2_id):
                        adjacent_nodes.append((node1_id, node2_id))

def is_adjacent(node1, node2):
    x1_pos, y1_pos = board_mapping['nodes'][node1]
    x2_pos, y2_pos = board_mapping['nodes'][node2]
    x_diff = abs(x1_pos - x2_pos)
    y_diff = abs(y1_pos - y2_pos)
    max_road_len = 100  # road lens are diff so this is maximum road len
    print(f'x_diff: {x_diff}')
    print(f'y_diff: {y_diff}')
    # return true if x_diff and y_diff is less than radius of tiles
    return (x_diff <= max_road_len) and (y_diff <= max_road_len)

create_adjacent_nodes(board_mapping['nodes'], adjacent_nodes)

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

    
    board = [GameTile(random.randint(1, 12),
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



class StartMenu:
    def __init__(self):
        self.start_button_rect = pygame.Rect(200,600, 200, 100)
        self.start_button_text = WORD_FONT.render("Start Game", True, BLACK)
        self.rule_book_button_rect = pygame.Rect(500, 600, 200, 100 )
        self.rule_book_button_text = WORD_FONT.render("Rules", True, BLACK)
        self.input_box = pygame.Rect(DISPLAY_WIDTH//2-200, DISPLAY_HEIGHT//2+50, 400, 50)
        self.current_state = None
        self.text = ''
        self.type_active = False # flag to see if player clicked on input box
        self.checkbox_rect = pygame.Rect(1000, DISPLAY_HEIGHT//2+50, 30, 30)
        self.checked = False

    
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    if len(players)<2:
                        self.current_state = StartMenu()
                    else:
                    
                        self.current_state = SpecialRoundGameState(players[0])
                    
                if self.rule_book_button_rect.collidepoint(event.pos):
                    webbrowser.open('https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf')
                if self.input_box.collidepoint(event.pos):
                    self.type_active = True
                else:
                    self.type_active = False
                if self.checkbox_rect.collidepoint(event.pos):
                    self.checked = not self.checked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.text and not self.checked:
                        try:
                            player = Player(self.text, colors[len(players)])
                            players.append(player)
                            self.text = ''
                        except IndexError:
                            continue
                    elif self.text and self.checked:
                        try:
                            player = AIPlayer(self.text, colors[len(players)])
                            players.append(player)
                            self.text = ''
                        except IndexError:
                            continue
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
    
    def draw(self, screen):
        
        WELCOME_FONT = pygame.font.SysFont("Algerian", 100, True)
        WORD_FONT = pygame.font.SysFont('Palatino', 40)

        background_img = pygame.image.load(os.path.join('src','assets','images','start-menu-background.jpg'))
        background_img  = pygame.transform.scale(background_img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        screen.blit(background_img, (0,0))

        welcome_text_surface = WELCOME_FONT.render("Welcome to ugly Catan!", True, BLACK)
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

        # draw checkbox for AI player

        checkbox_prompt_text = WORD_FONT.render("Check box to set as AI player", True, BLACK)
        checkbox_prompt_rect = checkbox_prompt_text.get_rect(center=(700,  DISPLAY_HEIGHT//2+150))
        screen.blit(checkbox_prompt_text, checkbox_prompt_rect)

        input_prompt_text = WORD_FONT.render("Enter name hear: ", True, BLACK)
        input_prompt_rect = input_prompt_text.get_rect(center=(DISPLAY_WIDTH//2-320, DISPLAY_HEIGHT//2+70))
        screen.blit(input_prompt_text, input_prompt_rect)


        pygame.draw.rect(screen, BLACK, self.checkbox_rect, 4)
        if self.checked:
            pygame.draw.line(screen, BLACK, (self.checkbox_rect.left+5, self.checkbox_rect.centery), 
                         (self.checkbox_rect.left+10, self.checkbox_rect.bottom-5), 4)
            pygame.draw.line(screen, BLACK, (self.checkbox_rect.left+10, self.checkbox_rect.bottom-5), 
                            (self.checkbox_rect.right-5, self.checkbox_rect.top+5), 4)        



        pygame.display.flip()

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
        
class SpecialRoundGameState: # gamestate for the first 2 turns of the game (players can build 1 road and settlement free)
    def __init__(self, player):
        self.current_player = player
        self.players = players
        self.current_turn_number = 0 # when this hits len(players)*2 it means everyone has had 2 free rounds - move to maingamestate
        self.player_turn_index = 0
        self.current_state = None
        self.node_buttons = []
        self.settlement_node1 = None
        self.settlement_node2 = None
        self.road_1 = [None, None] # (road_node1, road_node2)
        self.road_2 = [None, None]
        self.settlement_img = pygame.image.load(os.path.join('src','assets','buildings','settlement.png'))
        

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node_button in self.node_buttons:
                    if node_button.is_clicked(mouse_pos):
                        if self.settlement_node1 == None:
                            self.settlement_node1 = node_button
                            self.current_player.build_settlement(self.settlement_node1, is_special_round=True)
                            built_settlements.append((self.settlement_node1, self.current_player))
                            return
                        elif self.settlement_node2 == None:
                            self.settlement_node2 = node_button
                            self.current_player.build_settlement(self.settlement_node2, is_special_round=True)
                            built_settlements.append((self.settlement_node2, self.current_player))
                            return
                        else:
                            if self.road_1[0] is None:
                                self.road_1[0] = node_button
                            elif self.road_1[1] is None and self.is_adjacent(self.road_1[0], node_button):
                                self.road_1[1] = node_button
                                self.current_player.build_road(self.road_1[0], self.road_1[1], is_special_round=True)
                                built_roads.append(((self.road_1[0], self.road_1[1], self.current_player)))
                            elif self.road_2[0] is None:
                                self.road_2[0] = node_button
                            elif self.road_2[1] is None:
                                self.road_2[1] = node_button
                                self.current_player.build_road(self.road_2[0], self.road_2[1], is_special_round=True)
                                built_roads.append(((self.road_2[0], self.road_2[1], self.current_player)))
                        return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.current_turn_number == len(players)-1:
                        self.current_state = MainGameState(self.current_player)
                    if self.player_turn_index == len(self.players) - 1:
                        self.player_turn_index = 0
                        self.current_player = self.players[self.player_turn_index]
                        self.current_turn_number +=1
                    else:
                        self.player_turn_index += 1
                        self.current_player = self.players[self.player_turn_index]
                        self.current_turn_number +=1
                
                    self.current_player.settlements.append(self.settlement_node1)
                    self.current_player.settlements.append(self.settlement_node2)
                    self.current_player.roads.append(self.road_1)
                    self.current_player.roads.append(self.road_2)
                            
                    self.settlement_node1 = None
                    self.settlement_node2 = None
                    self.road_1 = [None, None]
                    self.road_2 = [None, None]
                


    def draw(self, screen):
        screen.fill(self.current_player.color)
        WORD_FONT = pygame.font.SysFont('arial', 40)
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
        button_radius = [10, 22]

        for _node_id, node_point in board_mapping['nodes'].items():
            button = ButtonHex(
                (node_point[0], node_point[1]),
                button_radius[0],
                GRAY)
            button.draw(screen)
            self.node_buttons.append(button)

        prompt_text = WORD_FONT.render(f'{self.current_player.name}: Pick a node to build a Settlement', True, BLACK)
        prompt_rect = pygame.Rect(800, 200, 100, 100)
        screen.blit(prompt_text, prompt_rect)

        for settlement in built_settlements:
            # Create a transparent surface
            highlighted_img = pygame.Surface(settlement_img.get_size(), pygame.SRCALPHA)
            highlighted_img.fill(settlement[1].color)
            highlighted_img.blit(settlement_img, (0, 0), None, pygame.BLEND_RGBA_MULT)

            
            screen.blit(highlighted_img, (settlement[0].x_pos-25, settlement[0].y_pos-25))
            

        for line in built_roads:
            pygame.draw.line(
                screen,
                line[2].color,
                (line[0].x_pos, line[0].y_pos),
                (line[1].x_pos, line[1].y_pos),
                5)

    def is_adjacent(self, node1, node2):

        x1_pos, y1_pos = node1.x_pos, node1.y_pos
        x2_pos, y2_pos = node2.x_pos, node2.y_pos

        x_diff = abs(x1_pos - x2_pos)
        y_diff = abs(y1_pos - y2_pos)
        max_road_len = 100  # road lens are diff so this is maximum road len



        # return true if x_diff and y_diff is less than radius of tiles
        return (x_diff <= max_road_len) and (y_diff <= max_road_len)
    
    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
    
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
        

class MainGameState:
    def __init__(self, player, robber_coords = None):
        # TODO check if restart is true. if so re-initialize all values to there start values, else maintain.
        self.current_turn_number = current_turn_number
        self.player_turn_index = 0
        self.current_player = player
        self.bank = Bank()
        self.players = players
        self.current_state = None
        self.build_road_rect = pygame.Rect(830, 640, 190, 40)
        self.build_settlement_rect = pygame.Rect(830, 700, 190, 40)
        self.build_city_rect = pygame.Rect(1030, 640, 190, 40)
        self.make_trade_rect = pygame.Rect(1030, 700, 190, 40)
        self.dev_card_rect = pygame.Rect(1230, 640, 190, 40)
        self.bank_inventory_rect = pygame.Rect(1230, 700, 190, 40)
        self.dice_rolled = [1,1]
        self.robber_coords = robber_coords
        self.invent_button_rect = pygame.Rect(1030, 760, 190, 40)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.make_trade_rect.collidepoint(event.pos):
                    self.current_state = ChooseTradePartner(self.current_player)
                if self.build_settlement_rect.collidepoint(event.pos):
                    self.current_state = Build(self.current_player, is_city=False)
                if self.dev_card_rect.collidepoint(event.pos):
                    
                    self.current_state = DevelopmentCardState(self.current_player)
                if self.bank_inventory_rect.collidepoint(event.pos):
                    
                    self.current_state = ChooseResources(self.current_player, None)
                if self.build_city_rect.collidepoint(event.pos):
                    
                    self.current_state = Build(self.current_player,is_city=True)
                if self.build_road_rect.collidepoint(event.pos):

                    self.current_state = RoadBuildState(self.current_player)
                if self.invent_button_rect.collidepoint(event.pos):
                    self.current_state = InventoryGameState(self.current_player)
                for node_button in node_buttons:
                    if node_button.is_clicked(event.pos):
                        pass
                for tile_button in tile_buttons:
                    if tile_button.is_clicked(event.pos):
                        pass
            elif event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_SPACE:

                    for player in players:
                        if player.victory_points >9:
                            self.current_state = EndMenu(players, )
                    if self.player_turn_index == len(self.players) - 1:
                        self.player_turn_index = 0
                        self.current_player = self.players[self.player_turn_index]
                        self.current_turn_number +=1
                    else:
                        self.player_turn_index += 1
                        self.current_player = self.players[self.player_turn_index]
                        self.current_turn_number +=1
                
                    dice_roll1, dice_roll2 = self.current_player.roll_dice(2)
                    self.dice_rolled[0]= dice_roll1
                    self.dice_rolled[1] = dice_roll2
                    for game_tile in board:
                        if dice_roll1 + dice_roll2 == game_tile.real_number:
                                
                            self.current_player.add_resource(game_tile.tile.generate_resource().name())
                            
                            card = game_tile.tile.generate_resource().name()
                           
                            game_log_txt = ''.join(
                                    f'{self.current_player.name} just rolled a '
                                    f'{dice_roll1+dice_roll2}. Added '
                                    f'{card} to inventory'
                                )
                            game_log.append(game_log_txt)
                    if dice_roll1+dice_roll2 == 7: # player can add robber to tile
                        card = game_tile.tile.generate_resource().name()
                        game_log_txt = ''.join(
                                    f'{self.current_player.name} just rolled a '
                                    f'{dice_roll1+dice_roll2}. Added '
                                    f'{card} to inventory'
                                )
                        game_log.append(game_log_txt)
                        self.current_state = PlaceRobberState(self.current_player)
    def draw(self, screen):
        """
        Draws the pygame display
        """
       
        
        screen.fill(BACKGROUND)
        robber_img = pygame.image.load(os.path.join('src','assets','Tiles','robber.jpg'))
        robber_img = pygame.transform.scale(robber_img, (robber_img.get_width()*0.05, robber_img.get_height()*0.05))

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

        for gametile in board:
            if gametile.has_robber and not self.robber_coords is None:
                screen.blit(robber_img, (self.robber_coords[0]+70, self.robber_coords[1]+65))

        self.draw_lines()
        for line in built_roads:
            pygame.draw.line(
                screen,
                line[2].color,
                (line[0].x_pos, line[0].y_pos),
                (line[1].x_pos, line[1].y_pos),
                5)
        self.draw_scoreboard(self.current_player)
        self.draw_buttons()
        self.draw_dice(self.dice_rolled[0],self.dice_rolled[1])


        
        for player in self.players:
            highlighted_img = pygame.Surface(settlement_img.get_size(), pygame.SRCALPHA)
            highlighted_img.fill(player.color)
            highlighted_img.blit(settlement_img, (0, 0), None, pygame.BLEND_RGBA_MULT)
            player_colors[player] = highlighted_img
        
        for settlement in built_settlements:
            screen.blit(player_colors[settlement[1]], (settlement[0].x_pos-25, settlement[0].y_pos-25))
    
        for settlement in built_settlements:
            screen.blit(player_colors[settlement[1]], (settlement[0].x_pos-25, settlement[0].y_pos-25))





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
            
    def draw_roads(self):
        for road in built_roads:
            pygame.draw.line(screen,
                            road[2].color, # player who build roads color
                            road[0], # start coord
                            road[1], # end coord
                            5)
            
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
       
        build_road_text = WORD_FONT.render('Build Road', True, WHITE, (17, 104, 245))
        screen.blit(build_road_text, self.build_road_rect)

        build_settlement_text = WORD_FONT.render('Build Settlement', True, WHITE, (38, 140, 31))
        screen.blit(build_settlement_text, self.build_settlement_rect)
         
        build_city_text = WORD_FONT.render('Build City', True, WHITE, (181, 186, 43))
        screen.blit(build_city_text, self.build_city_rect)

        make_trade_text = WORD_FONT.render('Trade', True, WHITE, (255, 51, 153))
        screen.blit(make_trade_text, self.make_trade_rect)
        
        dev_card_text = WORD_FONT.render('Development Card', True, WHITE, (51, 153, 255))
        screen.blit(dev_card_text, self.dev_card_rect)
        
        bank_inventory_text = WORD_FONT.render('Bank', True, WHITE, (255, 153, 51))
        screen.blit(bank_inventory_text, self.bank_inventory_rect)

        invent_button_text = WORD_FONT.render("Inventory", True, WHITE, GREEN)
        screen.blit(invent_button_text, self.invent_button_rect)

    
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
            
class InventoryGameState:
    def __init__(self, player):
        self.player = player
        self.current_state = None
        self.back_button = pygame.Rect(20, 700, 300, 200)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.current_state = MainGameState(self.player)

    def draw(self, screen):
        screen.fill(BACKGROUND)
        images = []
        images.append(pygame.image.load(os.path.join('src','assets','resource','lumber.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','wool.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','Grain.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','brick.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','ore.jpg')))
        
        x_offset_image = 20
        x_offset__text = 50
        for i , (resource, quantity) in enumerate(self.player.resources.items()):
            if resource is None:
                continue 

            screen.blit(images[i], (x_offset_image, 200))
            

            resource_info_text = WORD_FONT.render(f'{resource} : {quantity}', True, BLACK)
            resource_info_rect = resource_info_text.get_rect(center=(x_offset__text, 650))
            screen.blit(resource_info_text, resource_info_rect)
            x_offset__text+=280
            x_offset_image+=280

        
        screen.blit(BIG_FONT.render('Your Current Resources', True, BLACK), (200, 50))
        screen.blit(BIG_FONT.render('Back', True, BLACK, RED), self.back_button)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state

class PlaceRobberState:
    def __init__(self, player):
        self.player = player
        self.current_state = None
        self.robber_img = pygame.image.load(os.path.join('src','assets','Tiles','robber.jpg'))

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for id, coord in board_mapping['tiles'].items():
                    target_rect = pygame.Rect(coord[0], coord[1], 350, 350)
                    if target_rect.collidepoint(mouse_pos):
                        for game_tile in board:
                            if game_tile.get_tile_info()['Tile id'] == id:
                                game_tile.has_robber = True
                                self.current_state = MainGameState(self.player, (mouse_pos[0]-60, mouse_pos[1]-50))
                            
    

    def draw(self, screen):
        prompt_text = WORD_FONT.render(f'Place the robber on a tile', True, BLACK, RED)
        prompt_rect = prompt_text.get_rect(center=(500, 750))
        screen.blit(prompt_text, prompt_rect)
    
    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state

class ChooseResources:
    def __init__(self, player, trade_partner):
        self.player = player
        self.trade_partner = trade_partner
        self.current_state = None
        self.submit_button = pygame.Rect(300, 680, 400, 200)
        self.resource_buttons = []
        self.back_button = pygame.Rect(20, 680, 200, 200)
        
        self.offered_resources = [0,0,0,0,0]
        self.plus_buttons = []
        self.minus_buttons = []
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(len(self.plus_buttons))
                print(len(self.offered_resources))
                for i, plus_button in enumerate(self.plus_buttons):
                    if plus_button.collidepoint(event.pos):
                        self.offered_resources[i] +=1
                for i, minus_button in enumerate(self.minus_buttons):
                    if minus_button.collidepoint(event.pos) and self.offered_resources[i]>0:
                        self.offered_resources[i]-=1
                if self.back_button.collidepoint(event.pos):
                    self.current_state = MainGameState(self.player)
                elif self.submit_button.collidepoint(event.pos):
                    if self.trade_partner is None: # submit for bank trade
                        resource_names = [Resource.WOOD.name(), Resource.WOOL.name(), Resource.GRAIN.name(), Resource.BRICK.name(), Resource.ORE.name()]
                        resources_trade= dict(zip(resource_names, self.offered_resources))
                        if self.has_enough_resources(self.player.resources, resources_trade) and sum(resources_trade.values()) == 4:
                            self.current_state = BankTrade(self.player, bank, resources_trade)
                        else:
                            self.current_state = NotEnoughResources(self.player)
                    else:
                        resource_names = [Resource.WOOD.name(), Resource.WOOL.name(), Resource.GRAIN.name(), Resource.BRICK.name(), Resource.ORE.name()]
                        resources_trade= dict(zip(resource_names, self.offered_resources))
                        if self.has_enough_resources(self.player.resources, resources_trade):
                            self.current_state = ChooseDesiredResources(self.player, self.trade_partner, resources_trade)
                        else:
                            self.current_state = NotEnoughResources(self.player)
                        
                

    def draw(self, screen):
        screen.fill(BACKGROUND)

        images = []
        images.append(pygame.image.load(os.path.join('src','assets','resource','lumber.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','wool.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','Grain.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','brick.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','ore.jpg')))
        
        x_offset_image = 20
        x_offset__button = 50
        button_width = 30  
        button_height = 30

        self.plus_buttons.clear()
        self.minus_buttons.clear()

        for i in range(len(images)):
            screen.blit(images[i], (x_offset_image, 200))
            
            plus_button = pygame.Surface((button_width, button_height))
            plus_button.fill(GREEN)
            plus_button_rect = plus_button.get_rect()
            plus_button_rect.centerx = x_offset_image + images[i].get_width() / 2
            plus_button_rect.y = 120
            screen.blit(plus_button, plus_button_rect)
            screen.blit(WORD_FONT.render("+", True, WHITE), plus_button_rect)

            # Draw the '-' button
            minus_button = pygame.Surface((button_width, button_height))
            minus_button.fill(RED)
            minus_button_rect = minus_button.get_rect()
            minus_button_rect.centerx = x_offset_image + images[i].get_width() / 2
            minus_button_rect.y = 170
            screen.blit(minus_button, minus_button_rect)
            screen.blit(WORD_FONT.render("-", True, WHITE), minus_button_rect)

            self.plus_buttons.append(plus_button_rect)
            self.minus_buttons.append(minus_button_rect)

            # Draw resource quantity next to the + and - minus buttons
            quantity_text = WORD_FONT.render(str(self.offered_resources[i]), True, BLACK)
            quantity_rect = quantity_text.get_rect()
            quantity_rect.centerx = x_offset_image + images[i].get_width() / 2 + 25
            quantity_rect.y = 160
            screen.blit(quantity_text, quantity_rect)

            x_offset__button+=280
            x_offset_image+=280

            self.resource_buttons.append(images[i].get_rect())

    
        x_offset = 150
        for resource, quantity in self.player.resources.items():
            if resource == None:
                continue
            else:
                trade_quantity_text = WORD_FONT.render(f'amount owned: {quantity}', True, BLACK)
                trade_quantity_rect = trade_quantity_text.get_rect(center=(x_offset, 650))
                
                screen.blit(trade_quantity_text, trade_quantity_rect)
                x_offset +=270


        
        screen.blit(BIG_FONT.render('Your Current Resources', True, BLACK), (200, 30))
        screen.blit(BIG_FONT.render('Back', True, BLACK, RED), self.back_button)
        screen.blit(BIG_FONT.render('Submit Resources', True, BLACK), self.submit_button)

    
    def has_enough_resources(self, player_resources, offered_resources):
        for resource, quantity in offered_resources.items(): # check to see if player has enough resources

            if resource not in player_resources or player_resources[resource] < quantity:
                return False
        return True
            

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
    
class ChooseDesiredResources:
    def __init__(self, player, trade_partner, offered_resources):
        self.player = player
        self.trade_partner = trade_partner
        self.offered_resources = offered_resources
        self.current_state = None
        self.submit_button = pygame.Rect(300, 680, 200, 200)
        self.resource_buttons = [] # The resource buttons of the trade partner the player desires
        self.back_button = pygame.Rect(20, 680, 200, 200)
        self.desired_resources = [0,0,0,0,0]
        self.plus_buttons = []
        self.minus_buttons = []
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for i, plus_button in enumerate(self.plus_buttons):
                    if plus_button.collidepoint(event.pos):
                        self.desired_resources[i] +=1
                for i, minus_button in enumerate(self.minus_buttons):
                    if minus_button.collidepoint(event.pos) and self.desired_resources[i]>0:
                        self.desired_resources[i]-=1
                if self.back_button.collidepoint(event.pos):
                    self.current_state = MainGameState(self.player)
                elif self.submit_button.collidepoint(event.pos):
                    if self.trade_partner is None: # submit for bank trade
                        resource_names = [Resource.WOOD.name(), Resource.WOOL.name(), Resource.GRAIN.name(), Resource.BRICK.name(), Resource.ORE.name()]
                        resources_trade= dict(zip(resource_names, self.desired_resources))
                        if self.has_enough_resources(self.trade_partner.resources, resources_trade):
                            self.current_state = BankTrade(self.player, bank, resources_trade)
                        else:
                            self.current_state = NotEnoughResources(self.player)
                    else:
                        resource_names = [Resource.WOOD.name(), Resource.WOOL.name(), Resource.GRAIN.name(), Resource.BRICK.name(), Resource.ORE.name()]
                        resources_trade= dict(zip(resource_names, self.desired_resources))
                        print(resources_trade)
                        self.current_state = AcceptTradeState(self.player, self.trade_partner, self.offered_resources, resources_trade)


    def draw(self, screen):
        screen.fill(BACKGROUND)

        images = []
        images.append(pygame.image.load(os.path.join('src','assets','resource','lumber.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','wool.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','Grain.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','brick.jpg')))
        images.append(pygame.image.load(os.path.join('src','assets','resource','ore.jpg')))
        
        x_offset_image = 20
        x_offset__button = 50
        button_width = 30  
        button_height = 30

        self.plus_buttons.clear()
        self.minus_buttons.clear()

        for i in range(len(images)):
            screen.blit(images[i], (x_offset_image, 200))
            
            plus_button = pygame.Surface((button_width, button_height))
            plus_button.fill(GREEN)
            plus_button_rect = plus_button.get_rect()
            plus_button_rect.centerx = x_offset_image + images[i].get_width() / 2
            plus_button_rect.y = 120
            screen.blit(plus_button, plus_button_rect)
            screen.blit(WORD_FONT.render("+", True, WHITE), plus_button_rect)

            # Draw the '-' button
            minus_button = pygame.Surface((button_width, button_height))
            minus_button.fill(RED)
            minus_button_rect = minus_button.get_rect()
            minus_button_rect.centerx = x_offset_image + images[i].get_width() / 2
            minus_button_rect.y = 170
            screen.blit(minus_button, minus_button_rect)
            screen.blit(WORD_FONT.render("-", True, WHITE), minus_button_rect)

            self.plus_buttons.append(plus_button_rect)
            self.minus_buttons.append(minus_button_rect)

            # Draw resource quantity next to the + and - minus buttons
            quantity_text = WORD_FONT.render(str(self.desired_resources[i]), True, BLACK)
            quantity_rect = quantity_text.get_rect()
            quantity_rect.centerx = x_offset_image + images[i].get_width() / 2 + 25
            quantity_rect.y = 160
            screen.blit(quantity_text, quantity_rect)

            x_offset__button+=280
            x_offset_image+=280

            self.desired_resources.append(images[i].get_rect())

        # draw the quantity of the resource the trade partner has
        x_offset = 150
        for resource, quantity in self.trade_partner.resources.items():
            if resource == None:
                continue
            else:
                trade_quantity_text = WORD_FONT.render(f'amount owned: {quantity}', True, BLACK)
                trade_quantity_rect = trade_quantity_text.get_rect(center=(x_offset, 650))
                
                screen.blit(trade_quantity_text, trade_quantity_rect)
                x_offset +=270

        
        screen.blit(BIG_FONT.render(f'{self.trade_partner.name}: Current Resources', True, BLACK), (200, 30))
        screen.blit(BIG_FONT.render('Back', True, BLACK, RED), self.back_button)
        screen.blit(BIG_FONT.render('Submit Resources', True, BLACK), self.submit_button)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state



class BankTrade:
    def __init__(self, player, bank, offered_resources):
        self.player = player
        self.bank = bank
        self.current_state = None
        self.resource_buttons = []
        self.back_button = pygame.Rect(1000, 700, 200, 200)
        self.offered_resources = offered_resources

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (button, resource) in enumerate(self.resource_buttons):
                    if button.collidepoint(mouse_pos):
                        if i == 0:
                           self.player.add_resource(Resource.BRICK.name())
                           self.bank.resources[Resource.BRICK.name()]-=1
                           self.player.remove_resources(self.offered_resources)
                           self.current_state = MainGameState(self.player)
                        elif i == 1:
                            self.player.add_resource(Resource.WOOD.name())
                            self.bank.resources[Resource.WOOD.name()]-=1
                            self.player.remove_resources(self.offered_resources)
                            self.current_state = MainGameState(self.player)
                        elif i == 2:
                            self.player.add_resource(Resource.WOOL.name())
                            self.bank.resources[Resource.WOOL.name()]-=1
                            self.player.remove_resources(self.offered_resources)
                            self.current_state = MainGameState(self.player)
                        elif i == 3:
                            self.player.add_resource(Resource.GRAIN.name())
                            self.bank.resources[Resource.GRAIN.name()]-=1
                            self.player.remove_resources(self.offered_resources)
                            self.current_state = MainGameState(self.player)
                        elif i == 4:
                            self.player.add_resource(Resource.ORE.name())
                            self.bank.resources[Resource.ORE.name()]-=1
                            self.player.remove_resources(self.offered_resources)
                            self.current_state = MainGameState(self.player)
                    elif self.back_button.collidepoint(mouse_pos):
                        self.current_state = MainGameState(self.player)
                        

    def draw(self, screen):
        screen.fill(BACKGROUND)

        resource_images = []
        resource_images.append((pygame.image.load(os.path.join('src','assets','resource','brick.jpg')),Resource.BRICK))
        resource_images.append((pygame.image.load(os.path.join('src','assets','resource','lumber.jpg')), Resource.WOOD))
        resource_images.append((pygame.image.load(os.path.join('src','assets','resource','wool.jpg')), Resource.WOOL))
        resource_images.append((pygame.image.load(os.path.join('src','assets','resource','Grain.jpg')), Resource.GRAIN))
        resource_images.append((pygame.image.load(os.path.join('src','assets','resource','ore.jpg')), Resource.ORE))

        x_offset = 5
        for image, resource in resource_images:
            screen.blit(image, (x_offset, 100))
            rect = pygame.Rect(x_offset, 100, image.get_width(), image.get_height())
            self.resource_buttons.append((rect, resource))
            x_offset+=290

        font = pygame.font.SysFont("arial", 100, True)
        bank_message_text = font.render("Trade with the Bank!", True, BLACK)
        bank_message_rect = pygame.Rect(20, 20, DISPLAY_WIDTH-2, 50)
        screen.blit(bank_message_text, bank_message_rect)
        
        x_offset = 100
        for resource, quantity in self.bank.resources.items():
            text = WORD_FONT.render(f'{resource} : {quantity}', True, BLACK)
            text_rect = pygame.Rect(x_offset, 600, 100, 100)
            screen.blit(text, text_rect)
            x_offset += 280

        font = pygame.font.SysFont("arial", 100, True)
        back_button_text = font.render(f'Back', True, BLACK, RED)
        
        screen.blit(back_button_text, self.back_button)

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
        self.card_images = {DevelopmentCards.KNIGHT: (pygame.image.load(os.path.join('src','assets','Development','knight.jpg')), pygame.Rect(300, 50, 100, 150)),
                            DevelopmentCards.VP: (pygame.image.load(os.path.join('src','assets','Development','palace.jpg')), pygame.Rect(700, 50, 100, 150))}                                                            
        self.back_button_rect = pygame.Rect(1100, 600, 400, 200)
    
    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for card, (image, rect) in self.card_images.items():
                    if rect.collidepoint(mouse_pos):
                        self.player.buy_dev_card(card.name())
                        print(f'{card.name()} bought')
                        self.current_state = MainGameState(self.player)
                if self.back_button_rect.collidepoint(mouse_pos):
                    self.current_state = MainGameState(self.player)

    def draw(self, screen):
        screen.fill(BACKGROUND)
        
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


        font_size = min(100, int(self.back_button_rect.height * 0.8)) # sets font size to be 80% size of recatngle
        font = pygame.font.SysFont('Palatino', font_size)

        back_button_text = font.render("Back", True, BLACK, RED)
        screen.blit(back_button_text, self.back_button_rect)

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
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node_button in node_buttons:
                    if node_button.is_clicked(mouse_pos):
                        self.node = node_button
                        if self.has_enough_resources():
                            if self.is_city:
                                self.player.build_city(self.node)
                                self.player.victory_points +=2
                                built_cities.append((self.node, self.player))
                                self.current_state = MainGameState(self.player)
                            else:
                                self.player.build_settlement(self.node, False)
                                self.player.victory_points +=1
                                built_settlements.append((self.node, self.player))
                                self.current_state =  MainGameState(self.player)
                        else:
                            self.current_state = NotEnoughResources(self.player)

    def draw(self, screen):
        pass
        

    def has_enough_resources(self):
        if self.is_city:
            city_cost = {ResourceTile.MOUNTAIN.generate_resource().name(): 3, 
                                    ResourceTile.PASTURE.generate_resource().name(): 2}
            
        
            for resource, amount in city_cost.items():
                if resource not in self.player.resources or self.player.resources[resource] < amount:
                    return False
            return True
        else: 
            settlement_cost = {ResourceTile.HILLS.generate_resource().name(): 1, 
                            ResourceTile.PASTURE.generate_resource().name(): 1,
                            ResourceTile.FOREST.generate_resource().name(): 1,
                            ResourceTile.FIELDS.generate_resource().name(): 1
                            }
            for resource, quantity in settlement_cost.items():
                    
                if resource not in self.player.resources or self.player.resources[resource] < quantity:
                    return False
            return True
    
    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state

class RoadBuildState:
    

    def __init__(self, player):
        self.player = player      
        self.node1 = None
        self.node2 = None
        self.cost = {Resource.BRICK.name(): 1, Resource.WOOD.name():1}
        self.current_state = None
        self.cancel_button = pygame.Rect(700, 700, 100, 100)
        self.building_road = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for node_button in node_buttons:
                    if node_button.is_clicked(mouse_pos):
                        if not self.building_road:
                            # player clicked on the first node
                            self.node1 = node_button
                            self.building_road = True
                            return
                        elif self.is_adjacent(self.node1, node_button):
                            # player clicked on the second adjacent node
                            self.node2 = node_button
                            if self.has_enough_resources():
                                self.player.build_road(self.node1, self.node2, is_special_round=False)
                                built_roads.append((self.node1, self.node2, self.player))
                                self.current_state = MainGameState(self.player)
                            else:
                                self.current_state = NotEnoughResources(self.player)
                            self.building_road = False
                            return
                        else:
                            # player clicked on a non-adjacent node
                            self.current_state = MainGameState(self.player)
                            self.building_road = False
                            return
                    if self.cancel_button.collidepoint(mouse_pos):
                        # player cancelled the road building action
                        self.current_state = MainGameState(self.player)
                        self.building_road = False
                        return
    
    def has_enough_resources(self):
        for resource, amount in self.cost.items():
            if resource not in self.player.resources or self.player.resources[resource] < amount:
                return False
        return True
    
    def is_adjacent(self, node1, node2):

        x1_pos, y1_pos = node1.x_pos, node1.y_pos
        x2_pos, y2_pos = node2.x_pos, node2.y_pos

        x_diff = abs(x1_pos - x2_pos)
        y_diff = abs(y1_pos - y2_pos)
        max_road_len = 100  # road lens are diff so this is maximum road len


        # return true if x_diff and y_diff is less than radius of tiles
        return (x_diff <= max_road_len) and (y_diff <= max_road_len)
    
    def draw(self, screen):
        prompt_text = WORD_FONT.render('click two adjacent nodes to build a road!', True, BLACK, RED)
        prompt_rect = pygame.Rect(300, 750, 100, 100)
        screen.blit(prompt_text, prompt_rect)

        cancel_text = WORD_FONT.render('Cancel', True, BLACK, RED)
        screen.blit(cancel_text, self.cancel_button)
    
    
    

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
        self.font = pygame.font.SysFont("arial", 70, True)
        self.back_button_text = self.font.render('Back Button', True, BLACK, RED)
        self.back_button_rect = self.back_button_text.get_rect(center=(1000, 700))



    def draw(self, screen):
        screen.fill(BACKGROUND)
        x_offset = 150

        for player in players:
            if player.name != self.player.name:
                
                player_name_text = self.font.render(player.name, True, WHITE, player.color)
                player_rect = player_name_text.get_rect(center=(x_offset, DISPLAY_HEIGHT//2))
                self.available_players.append((player_rect, player))
                screen.blit(player_name_text, player_rect)
                x_offset +=275

        prompt_text = self.font.render('Choose who to trade with', True, BLACK)
        prompt_rect = prompt_text.get_rect(center=(700,100))
        screen.blit(prompt_text, prompt_rect)
        screen.blit(self.back_button_text, self.back_button_rect)
    

    


    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if self.back_button_rect.collidepoint(mouse_pos):
                    self.current_state = MainGameState(self.player)
            
                for player in self.available_players:
                    if player[0].collidepoint(mouse_pos):
                        self.trade_partner = player[1]
                        self.current_state = ChooseResources(self.player, self.trade_partner)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state  

                

                
class AcceptTradeState:
    def __init__(self, player, trade_partner, player_resources, trade_partner_resources):
        self.player = player
        self.trade_partner = trade_partner
        self.current_state = None
        self.trade_accepted = False
        self.player_resources = player_resources
        self.trade_partner_resources = trade_partner_resources        
        self.accept_rect = pygame.Rect(100, 300, 50, 50)
        self.accept_text = WORD_FONT.render("Accept?", True, GREEN)

        self.decline_rect = pygame.Rect(400, 300, 80, 80)
        self.decline_text = WORD_FONT.render("Decline?", True, RED)

    def draw(self, screen):
        screen.fill(BACKGROUND)

        prompt_text = BIG_FONT.render(f'{self.trade_partner.name}: Accept or decline this offer', True, BLACK)
        prompt_rect = prompt_text.get_rect(center=(500, 100))
        screen.blit(prompt_text, prompt_rect)
         
        pygame.draw.rect(screen, BLACK, self.accept_rect)
        screen.blit(self.accept_text, (self.accept_rect.x + 10, self.accept_rect.y + 10))

        pygame.draw.rect(screen, BLACK, self.decline_rect)
        screen.blit(self.decline_text, (self.decline_rect.x + 10, self.decline_rect.y + 10))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.accept_rect.collidepoint(event.pos):
                    for resource in self.player_resources.keys():
                        print(f'before: {resource} : {self.player.resources[resource]}')
        
                        self.player.resources[resource]-=1
                        self.trade_partner.resources[resource]+=1

                        print(f'after: {resource} : {self.player.resources[resource]}')
                    for resource in self.trade_partner_resources:
                        self.player.resources[resource]+=1
                        self.trade_partner.resources[resource]-=1
                    self.current_state =  MainGameState(self.player)
                

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
    
class NotEnoughResources:
    def __init__(self, player):
        self.player = player
        self.current_state  = None
        self.font = pygame.font.SysFont("Algerian", 100, True)
        self.message_text = self.font.render('Not enough resources!', True, WHITE, RED)
        self.message_rect  = self.message_text.get_rect(center=(DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2))

    def handle_events(self, events):
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.message_rect.collidepoint(mouse_pos):
                    self.current_state = MainGameState(self.player)

    def draw(self, screen):
        screen.blit(self.message_text, self.message_rect)

    def should_transition(self):
        return self.current_state is not None
    def transition(self):
        return self.current_state
    

class EndMenu:
    def __init__(self, players):
        self.players = players
        self.current_state = None
        self.players.sort(key=lambda p:p.victory_points, reverse=True)
        self.main_menu_button_text = WORD_FONT.render("Main Menu", True, BLACK)
        self.main_menu_button_rect = pygame.Rect(400, 600, 200, 200)

    def draw(self, screen):
        screen.fill(BACKGROUND)

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
    """
    The main game loop that runs the game until the user quits.

    :param kwargs: Additional keyword arguments (unused).
    :type kwargs: dict

    :return: None
    :rtype: None
    """
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
            current_state = StartMenu()

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
