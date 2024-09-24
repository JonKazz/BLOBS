import pygame
a = pygame.font.get_fonts()
for i in a:
    if i[0] == "l":
        print(i)