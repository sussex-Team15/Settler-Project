# pylint: disable=missing-module-docstring
from os import path
import pygame

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class DrawDice:
    """
    A class that displays and updates all of the dice image assets onto the pygame window.

    This class provides functionality for drawing and updating the two dice images on the
    pygame window, based on the current roll values of the dice.

    :param DISPLAY_HEIGHT: The height of the pygame display window.
    :type DISPLAY_HEIGHT: int
    :param dice_size: The size of the dice images to display.
    :type dice_size: int
    """
    def __init__(self):
        """
        Initializes a new DrawDice object with the specified display height and dice size.

        The constructor also loads all of the dice images from the asset files and scales them
        to the specified size.

        :param DISPLAY_HEIGHT: The height of the pygame display window.
        :type DISPLAY_HEIGHT: int
        :param dice_size: The size of the dice images to display.
        :type dice_size: int
        """
        # loading dice images
        self.DISPLAY_HEIGHT = 800
        self.dice_size = 80
        side_1_p = path.join('src', 'assets', 'dice', '1_sided.jpg')
        side_2_p = path.join('src', 'assets', 'dice', '2_sided.jpg')
        side_3_p = path.join('src', 'assets', 'dice', '3_sided.jpg')
        side_4_p = path.join('src', 'assets', 'dice', '4_sided.jpg')
        side_5_p = path.join('src', 'assets', 'dice', '5_sided.jpg')
        side_6_p = path.join('src', 'assets', 'dice', '6_sided.jpg')
        self.side_1 = pygame.image.load(side_1_p)
        self.side_2 = pygame.image.load(side_2_p)
        self.side_3 = pygame.image.load(side_3_p)
        self.side_4 = pygame.image.load(side_4_p)
        self.side_5 = pygame.image.load(side_5_p)
        self.side_6 = pygame.image.load(side_6_p)

        # scaling all to the same size
        self.side_1 = pygame.transform.scale(self.side_1, (self.dice_size,
                                                        self.dice_size))
        self.side_2 = pygame.transform.scale(self.side_2, (self.dice_size,
                                                        self.dice_size))
        self.side_3 = pygame.transform.scale(self.side_3, (self.dice_size,
                                                        self.dice_size))
        self.side_4 = pygame.transform.scale(self.side_4, (self.dice_size,
                                                        self.dice_size))
        self.side_5 = pygame.transform.scale(self.side_5, (self.dice_size,
                                                        self.dice_size))
        self.side_6 = pygame.transform.scale(self.side_6, (self.dice_size,
                                                        self.dice_size))

    def draw(self, screen, roll_1, roll_2):
        """
        Draws the dice images onto the specified pygame screen, based on the current roll values.

        This method displays the two dice images at the specified locations on the screen,
        based on the current values of `roll_1` and `roll_2`.

        :param screen: The pygame screen to display the dice images on.
        :type screen: pygame.Surface
        :param roll_1: The current roll value of the first die.
        :type roll_1: int
        :param roll_2: The current roll value of the second die
        :type roll_2: int
        """
        if roll_1 == 1:
            screen.blit(self.side_1, (10, self.DISPLAY_HEIGHT - 90))
        elif roll_1 == 2:
            screen.blit(self.side_2, (10, self.DISPLAY_HEIGHT - 90))
        elif roll_1 == 3:
            screen.blit(self.side_3, (10, self.DISPLAY_HEIGHT - 90))
        elif roll_1 == 4:
            screen.blit(self.side_4, (10, self.DISPLAY_HEIGHT - 90))
        elif roll_1 == 5:
            screen.blit(self.side_5, (10, self.DISPLAY_HEIGHT - 90))
        elif roll_1 == 6:
            screen.blit(self.side_6, (10, self.DISPLAY_HEIGHT - 90))

        if roll_2 == 1:
            screen.blit(self.side_1, (130, self.DISPLAY_HEIGHT - 90))
        elif roll_2 == 2:
            screen.blit(self.side_2, (130, self.DISPLAY_HEIGHT - 90))
        elif roll_2 == 3:
            screen.blit(self.side_3, (130, self.DISPLAY_HEIGHT - 90))
        elif roll_2 == 4:
            screen.blit(self.side_4, (130, self.DISPLAY_HEIGHT - 90))
        elif roll_2 == 5:
            screen.blit(self.side_5, (130, self.DISPLAY_HEIGHT - 90))
        elif roll_2 == 6:
            screen.blit(self.side_6, (130, self.DISPLAY_HEIGHT - 90))

        pygame.display.update()
