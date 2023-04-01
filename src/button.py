import pygame

class ButtonRect:
    def __init__(self, x, y, width, height, text, font, text_color, button_color, highlight_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.highlight_color = highlight_color
        self.cursor_set = False #boolean flag

    
    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def is_hovered_over(self, mouse_pos): # returns true if mouse hovers over button
        if self.rect.collidepoint(mouse_pos):
            if not self.cursor_set:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.cursor_set = True
                return True
        else: 
            if self.cursor_set:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.cursor_set = False
            return False




class ButtonHex:
    def __init__(self, x, y, radius, color, isFilled=True):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.cursor_set = False
        self.isFilled = isFilled
    
    def draw(self, surface):
        if self.isFilled:
            pygame.draw.polygon(surface, self.color, [
                (self.x + self.radius, self.y),
                (self.x + self.radius / 2, self.y + self.radius),
                (self.x - self.radius / 2, self.y + self.radius),
                (self.x - self.radius, self.y),
                (self.x - self.radius / 2, self.y - self.radius),
                (self.x + self.radius / 2, self.y - self.radius)
            ])
        else:
            pygame.draw.polygon(surface, self.color, [
                (self.x + self.radius, self.y),
                (self.x + self.radius / 2, self.y + self.radius),
                (self.x - self.radius / 2, self.y + self.radius),
                (self.x - self.radius, self.y),
                (self.x - self.radius / 2, self.y - self.radius),
                (self.x + self.radius / 2, self.y - self.radius)
            ], width=4) # same as above but with width so its not filled hex

    
    def is_hovered_over(self, mouse_pos): # returns true if mouse hovers over button

        if ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5 < self.radius:
            if not self.cursor_set:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.cursor_set = True
                return True
        else:
            if self.cursor_set:

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.cursor_set = False

            return False
    
    def is_clicked(self, mouse_pos):
        if ((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)**0.5 < self.radius:
            return True
        else: 
            return False
    
        
class TileButton:
    pass # button for the center of a board tile