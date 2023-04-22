from os import path
import pygame

# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
class DrawDice:
    """A Class that displays and updates all of the dice image assets onto the pygame window.
    """
    def __init__(self):
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
