import pygame

class Door:
    def __init__(self, x, y, width, height, name): 
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.locked = False

    def toggle(self):
        self.locked = not self.locked

    def draw(self, surface):
        color = (255, 0, 0) if self.locked else (0, 0, 0)
        pygame.draw.rect(surface, color, self.rect, )
