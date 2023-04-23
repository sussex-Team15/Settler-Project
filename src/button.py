import pygame

RED = (255, 0, 0)
GRAY = (158, 153, 134)


class ButtonRect:
    """
    A class representing a rectangular button.

    :param x_y_pos: A tuple representing the x and y coordinates of the top-left corner of the button.
    :type x_y_pos: Tuple[int, int]
    :param width_height: A tuple representing the width and height of the button.
    :type width_height: Tuple[int, int]
    :param text: The text displayed on the button.
    :type text: str
    :param colors: A tuple containing the colors of the button and its highlight when hovered over.
    :type colors: Tuple[Tuple[int, int, int], Tuple[int, int, int]]
    """
    def __init__(self,
                 x_y_pos,
                 width_height,
                 text,
                 colors):
        """
        Initializes a ButtonRect object with the given properties.

        :param x_y_pos: A tuple containing the (x, y) position of the button.
        :type x_y_pos: tuple
        :param width_height: A tuple containing the width and height of the button.
        :type width_height: tuple
        :param text: The text displayed on the button.
        :type text: str
        :param colors: A tuple containing the colors of the button and its highlight state.
        :type colors: tuple
        """
        x_pos, y_pos = x_y_pos
        width, height = width_height
        text, font, text_color = text
        button_color, highlight_color = colors

        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.highlight_color = highlight_color
        self.cursor_set = False  # boolean flag

    def draw(self, surface):
        """
        Draw the button onto the specified surface.

        :param surface: The surface to draw the button onto.
        :type surface: pygame.Surface
        """
        pygame.draw.rect(surface, self.button_color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        """
        Check if the button was clicked.

        :param mouse_pos: The current mouse position.
        :type mouse_pos: Tuple[int, int]
        :return: True if the button was clicked, False otherwise.
        :rtype: bool
        """
        return self.rect.collidepoint(mouse_pos)

    # returns true if mouse hovers over button
    def is_hovered_over(self, mouse_pos):
        """
        Check if the mouse is currently hovering over the button.

        :param mouse_pos: The current mouse position.
        :type mouse_pos: Tuple[int, int]
        :return: True if the mouse is hovering over the button, False otherwise.
        :rtype: bool
        """
        if self.rect.collidepoint(mouse_pos) and not self.cursor_set:
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND)  # pylint: disable=no-member
            self.cursor_set = True
            return True

        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_ARROW)  # pylint: disable=no-member
        self.cursor_set = False
        return False


class ButtonHex:
    """A class for creating and drawing hexagonal buttons.

    :param x_y_pos: A tuple of the x and y coordinates of the center of the button.
    :type x_y_pos: tuple
    :param radius: The radius of the button.
    :type radius: int
    :param color: The color of the button.
    :type color: tuple
    :param is_filled: Whether or not the button should be filled in. Defaults to True.
    :type is_filled: bool
    """
    def __init__(self,
                 x_y_pos,
                 radius,
                 color,
                 is_filled=True):
        """Create a hexagonal button with a specified position, radius, color, and fill.

        :param x_y_pos: The x and y coordinates of the center of the button.
        :type x_y_pos: Tuple[int, int]
        :param radius: The radius of the button.
        :type radius: int
        :param color: The color of the button.
        :type color: Tuple[int, int, int]
        :param is_filled: Whether the button should be filled in or not. Defaults to True.
        :type is_filled: bool
        """
        self.x_pos, self.y_pos = x_y_pos
        self.radius = radius
        self.color = color
        self.cursor_set = False
        self.is_filled = is_filled

    def draw(self, surface):
        """Draws the hexagonal button onto the specified pygame surface.

        :param surface: The pygame surface to draw the button onto.
        :type surface: pygame.Surface
        """
        if self.is_filled:
            pygame.draw.polygon(surface, self.color, [
                (self.x_pos + self.radius, self.y_pos),
                (self.x_pos + self.radius / 2, self.y_pos + self.radius),
                (self.x_pos - self.radius / 2, self.y_pos + self.radius),
                (self.x_pos - self.radius, self.y_pos),
                (self.x_pos - self.radius / 2, self.y_pos - self.radius),
                (self.x_pos + self.radius / 2, self.y_pos - self.radius)
            ])

    def is_hovered_over(self, mouse_pos):
        """Returns True if the mouse is currently hovering over the button, False otherwise.

        :param mouse_pos: The current x and y position of the mouse.
        :type mouse_pos: tuple
        :return: Whether or not the mouse is currently hovering over the button.
        :rtype: bool
        """
        # returns true if mouse hovers over button

        x_pos = (self.x_pos - mouse_pos[0])**2
        y_pos = (self.y_pos - mouse_pos[1])**2
        if (x_pos + y_pos)**0.5 < self.radius and not self.cursor_set:
            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND)  # pylint: disable=no-member
            self.cursor_set = True

            return True

        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_ARROW)  # pylint: disable=no-member
        self.cursor_set = False

        return False

    def is_clicked(self, mouse_pos):
        """Returns True if the button is currently being clicked, False otherwise.

        :param mouse_pos: The current x and y position of the mouse.
        :type mouse_pos: tuple
        :return: Whether or not the button is currently being clicked.
        :rtype: bool
        """
        x_pos = (self.x_pos - mouse_pos[0])**2
        y_pos = (self.y_pos - mouse_pos[1])**2

        return bool((x_pos + y_pos)**0.5 < self.radius)
