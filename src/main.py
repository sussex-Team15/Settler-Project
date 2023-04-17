import math
import os
import pygame
import random
import sys
from pygame.locals import *  # pylint: disable=unused-wildcard-import wildcard-import # nopep8 E501
from hexgrid import legal_tile_ids
from pprint import pprint

from src.draw_dice import DrawDice
from src.button import ButtonHex, ButtonRect

from src.player import Player


from src.tiles import GameTile, ResourceTile
from src.utils import ASSET_DIR

# pylint: disable=redefined-outer-name

# Initialize pygame
pygame.init()  # pylint: disable=no-member

DISPLAY_WIDTH, DISPLAY_HEIGHT = 1450, 800
NUM_FONT = pygame.font.SysFont('Palatino', 40)
WORD_FONT = pygame.font.SysFont('Palatino', 25)
GAME_LOG_FONT = pygame.font.SysFont('calibri', 25)


screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
bg_img = pygame.image.load(os.path.join(ASSET_DIR, "tile_order.png"))
bg_img.convert()


bg_rect = bg_img.get_rect()


NUM_PLAYERS = 6
player_names = ['Eddie', 'Morgan', 'Ryan', 'Noah', 'Yash', 'Nelson']
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
colors = [(255, 0, 0), (25, 255, 25), (255, 255, 77), (255, 153, 51),
          (0, 0, 0), (35, 219, 222)]  # colors r g y o b c
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

    players = []

    for i in range(NUM_PLAYERS):
        player = Player(player_names[i], colors[i])
        print(player.name)
        players.append(player)

    return tile_sprites, board, board_mapping, players


def main_game_loop(**kwargs):  # pylint: disable=unused-argument
    game_running = True
    player_turn_index = 0
    current_player = players[player_turn_index]

    dice_rolled.append((current_player.roll_dice(2)))

    pprint(board)
    # GAME LOOP
    # 1 LOOP THROUGH PLAYERS AND INITIALISE STARTING POSITIONS.
    # 2 BEGIN MAIN TURN BASED LOOP.
    # 2.1 PLAYER HAS CHOICE OF BUILDING AND

    while game_running:
        for event in pygame.event.get():  # pylint: disable=no-member
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                game_running = False

            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.key.K_SPACE:
                    if player_turn_index == len(players) - 1:
                        player_turn_index = 0
                        current_player = players[player_turn_index]
                    else:
                        player_turn_index += 1
                        current_player = players[player_turn_index]

                    dice_roll1, dice_roll2 = current_player.roll_dice(2)
                    dice_rolled.append((dice_roll1, dice_roll2))
                    

                    for game_tile in board:
                        if dice_roll1 + dice_roll2 == game_tile.real_number:
                            current_player.add_resources(game_tile)

                            card = game_tile.tile.generate_resource().name()
                            game_log_txt = ''.join(
                                f'{current_player.name} just rolled a '
                                f'{dice_roll1+dice_roll2}. Added '
                                f'{card} to inventory'
                            )

                            game_log.append(game_log_txt)

            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member # nopep8 E501
                click_event(event, current_player)  # handles clicking events

            elif event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
                mouse_motion_event()  # function handles mouse motion events

        if check_player_won():
            # draw_end_screen() # TODO
            game_running = False

        draw(current_player)
        for line in built_roads:
            pygame.draw.line(
                screen,
                line[2].color,
                (line[0].x_pos, line[0].y_pos),
                (line[1].x_pos, line[1].y_pos),
                5)
        draw_buildings()  # draw_settlements
        draw_buildings(city=True)  # draw cities

        # count how many settlements
        # each player has and award vp accordingly

        # player_longest_road = calc_longest_road()
        # player_longest_road.victory_points +=1
        roll1, roll2 = dice_rolled[0]
        draw_dice = DrawDice()
        draw_dice.draw(screen, roll1, roll2)
        pygame.display.update()
        # this is a comment)


def mouse_motion_event():
    mouse_pos = pygame.mouse.get_pos()
    for button in node_buttons:
        button.is_hovered_over(mouse_pos)
    for button in tile_buttons:
        button.is_hovered_over(mouse_pos)

    build_road_btn.is_hovered_over(mouse_pos)
    build_city_btn.is_hovered_over(mouse_pos)
    build_settlement_btn.is_hovered_over(mouse_pos)
    make_trade_btn.is_hovered_over(mouse_pos)
    other_btn_1.is_hovered_over(mouse_pos)
    other_btn_2.is_hovered_over(mouse_pos)


def click_event(_event, player):  # _ as not used yet
    mouse_pos = pygame.mouse.get_pos()

    for button in tile_buttons:
        if button.is_clicked(mouse_pos):
            print(print(f'{button.x_pos}, {button.y_pos} clicked!'))
            break

    if build_road_btn.is_clicked(mouse_pos):

        start_node = build_road()
        end_node = build_road()
        if is_adjacent(start_node, end_node):
            # check to see if nodes selected are adjacent
            built_roads.append((start_node, end_node, player))

            pygame.display.update()
            game_log.append((f'{player.name} built road!'))

    elif build_settlement_btn.is_clicked(mouse_pos):
        x_pos, y_pos = build_settlement(player)
        built_settlements.append(((x_pos - 20, y_pos - 30), player))
        game_log.append(f'{player.name} built settlement!')

    elif build_city_btn.is_clicked(mouse_pos):
        x_pos, y_pos = build_settlement(player, city=True)
        built_cities.append(((x_pos - 20, y_pos - 30), player))
        game_log.append(f'{player.name} built city!')
    elif make_trade_btn.is_clicked(mouse_pos):
        print('Trade Clicked')
    elif other_btn_1.is_clicked(mouse_pos):
        print('other button 1 clicked')
    elif other_btn_2.is_clicked(mouse_pos):
        print('other button 2 clicked')

    pygame.display.flip()


def build_settlement(player, city=False):
    """_summary_

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
                        # give player vp
                        if city:
                            player.victory_points += 2
                            # add 2 vp if player builds a city
                        else:
                            player.victory_points += 1
                        return mouse_pos


def build_road():
    """_summary_

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
                        return button


def check_player_won():
    """_summary_

    :return: _description_
    :rtype: _type_
    """
    for player in players:
        if player.victory_points >= 10:
            return True

    return False


def is_adjacent(node1, node2):
    ''' Returns true if node1 and node2 are connected by a road

    Args:
        node1: first node to be checked
        node2: second node to be checked

    Returns:
        boolean

    '''

    x1_pos, y1_pos = node1.x_pos, node1.y_pos
    x2_pos, y2_pos = node2.x_pos, node2.y_pos

    x_diff = abs(x1_pos - x2_pos)
    y_diff = abs(y1_pos - y2_pos)
    max_road_len = 100  # road lens are diff so this is maximum road len

    print(f'x_diff: {x_diff}')
    print(f'y_diff: {y_diff}')

    # return true if x_diff and y_diff is less than radius of tiles
    return (x_diff <= max_road_len) and (y_diff <= max_road_len)


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


def draw(player_turn):
    """
    Draws the pygame display
    """
    screen.fill(BACKGROUND)

    for img, rect in tile_sprites:
        screen.blit(img, rect)
        # screen.blit(bg_img, bg_rect)

    draw_lines()  # draws game board lines

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

    draw_scoreboard(player_turn)
    draw_buttons()

    popup()


def draw_lines():
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


def draw_buttons():
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


def draw_scoreboard(player_turn):
    """
    Draws the scoreboard as a seperate pygame surface
    """
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

    for i in range(NUM_PLAYERS):  # draw player names at top of scoreboard
        x_pos = 10 + i * player_width
        pygame.draw.line(rect_surf, WHITE, (x_pos, 10),
                         (x_pos, 430), rect_outline_width)
        name = player_font.render(players[i].name, True, WHITE)
        name_rect = name.get_rect(center=(x_pos + player_width // 2, 40))
        rect_surf.blit(name, name_rect)

    for i in range(NUM_PLAYERS):  # draw victory points
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
        game_log_text = GAME_LOG_FONT.render(game_log_text, True, WHITE)
        rect_surf.blit(game_log_text, (50, 460))
        screen.blit(rect_surf, (rect_x, rect_y))

    # player turn text being drawn
    player_turn_text = WORD_FONT.render(f'Current turn: {player_turn.name}',
                                        True, WHITE)
    rect_surf.blit(player_turn_text, (250, 540))
    screen.blit(rect_surf, (rect_x, rect_y))


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


def popup():
    '''
    popup window that gives options for player when node is clicked
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

    other_btn_1 = ButtonRect(  # pylint: disable=redefined-outer-name
        (1230, 640),
        (190, 40),
        ('Other Button', WORD_FONT, WHITE),
        ((51, 153, 255), WHITE))
    other_btn_1.draw(screen)

    other_btn_2 = ButtonRect(  # pylint: disable=redefined-outer-name
        (1230, 700),
        (190, 40),
        ('Other Button', WORD_FONT, WHITE),
        ((255, 153, 51), WHITE))
    other_btn_2.draw(screen)
    make_trade_btn.draw(screen)

    return (build_road_btn,
            build_settlement_btn,
            build_city_btn,
            make_trade_btn,
            other_btn_1,
            other_btn_2)


(build_road_btn,
 build_settlement_btn,
 build_city_btn,
 make_trade_btn,
 other_btn_1,
 other_btn_2) = popup()

if __name__ == "__main__":
    tile_sprites, board, board_mapping, players = setup()
    main_game_loop(
        tile_sprites=tile_sprites,
        board=board,
        board_mapping=board_mapping,
        players=players
    )
