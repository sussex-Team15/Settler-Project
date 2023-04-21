import pygame

RED = (255, 0, 0)
GRAY = (158, 153, 134)


class ButtonRect:

    def __init__(self,
                 x_y_pos,
                 width_height,
                 text,
                 colors):
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
        pygame.draw.rect(surface, self.button_color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    # returns true if mouse hovers over button
    def is_hovered_over(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and not self.cursor_set:
            return True
        return False


class ButtonHex:
    def __init__(self,
                 x_y_pos,
                 radius,
                 color,
                 is_filled=True):
        self.x_pos, self.y_pos = x_y_pos
        self.radius = radius
        self.color = color
        self.cursor_set = False
        self.is_filled = is_filled
        self.has_settlement = False
        self.has_city = False

    def draw(self, surface):
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
        # returns true if mouse hovers over button

        x_pos = (self.x_pos - mouse_pos[0])**2
        y_pos = (self.y_pos - mouse_pos[1])**2
        if (x_pos + y_pos)**0.5 < self.radius and not self.cursor_set:
            return True
        return False

    def is_clicked(self, mouse_pos):
        x_pos = (self.x_pos - mouse_pos[0])**2
        y_pos = (self.y_pos - mouse_pos[1])**2

        return bool((x_pos + y_pos)**0.5 < self.radius)
