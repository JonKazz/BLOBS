import pygame
from constants import PLAYER_COLOR, WIN_HEIGHT, WIN_WIDTH

DEBUG_FONT_SIZE = 15
debug_font = pygame.font.SysFont("arialblack", DEBUG_FONT_SIZE)

class Player():
    def __init__(self):
        self.x = WIN_WIDTH/2
        self.y = WIN_HEIGHT/2
        self.color = PLAYER_COLOR
        self.radius = 10
    
    def show_size(self, WIN, show_level) -> None: # Returns either blob radius or level based on show_level
        size = self.radius
        if show_level:
            size = int(0.5*size - 5)
        
        img = debug_font.render(str(size), True, "black")
        WIN.blit(img, (self.x - DEBUG_FONT_SIZE/2, self.y - DEBUG_FONT_SIZE/2))
        
    
    
    