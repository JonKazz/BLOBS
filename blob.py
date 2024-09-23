import pygame
import math
from spawn_algorithm_2 import blob_size_speed
from random import randint, uniform, choice
from constants import WIN_WIDTH, WIN_HEIGHT

pygame.init()

# Debug variables
DEBUG_FONT_SIZE = 15
debug_font = pygame.font.SysFont("arialblack", DEBUG_FONT_SIZE)

# Number of pixles blobs spawn offscreen
SPAWN_OFFSET = 150

class Blob(pygame.sprite.Sprite):
    
    ''' BLOB CREATION '''
    def __init__(self, 
                 groups: pygame.sprite.Group, 
                 player_rad: int):
        
        super().__init__(groups)
        rail = choice(("BOTTOM", "TOP", "LEFT", "RIGHT"))
        self.pos = self.rand_position(rail)
        self.direction = self.rand_direction(rail)
        
        self.color = choice(("red", "green", "blue"))
        self.radius, self.speed = blob_size_speed(player_rad)
    
        self.create_surf()
        
    def create_surf(self) -> None:
        self.image = pygame.Surface((self.radius*2, self.radius*2)).convert_alpha()
        self.image.set_colorkey("black") 
        pygame.draw.circle(surface=self.image, color=self.color, center=(self.radius, self.radius), radius=self.radius, width=0)
        self.rect = self.image.get_rect(center=self.pos)
        
        
        
        
        
        
        
        
        
        
    ''' BLOB MOVEMENT '''
    # Moves blob by direction * speed * dt
    def move(self, dt: float) -> None:
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
    
    # Updates blob position
    def update(self, dt) -> None:
        self.move(dt)
        self.check_offscreen()
        
    # Removes blob if offscreen
    def check_offscreen(self) -> None:
        self.pos += self.direction * self.speed
        if (
            self.pos[0] < -SPAWN_OFFSET or
            self.pos[0] > WIN_WIDTH + SPAWN_OFFSET or
            self.pos[1] < -SPAWN_OFFSET or
            self.pos[1] > WIN_HEIGHT + SPAWN_OFFSET
        ):
            self.kill()
    
    
    
    
    
    
    
    
    
    
    ''' PLAYER-BLOB CALCULATIONS'''
    
    # Returns distance between player and blob
    def distance(self, player) -> float:
        x, y = self.pos
        distance = math.sqrt((x - player.x)**2 + (y - player.y)**2)
        return round(distance, 2)
    
    # Returns True if player and blob are touching
    def is_touching(self, player) -> bool:
        if self.distance(player) < self.radius + player.radius:
            return True
        return False
        
    # Returns True if blob can eat player
    def can_eat(self, player) -> bool:
        dist = self.distance(player)
        if self.radius > player.radius and dist < self.radius - 0.4*player.radius:
            return True
        else:
            return False
    
    # Returns True if player can eat blob
    def can_be_eaten(self, player) -> bool:
        dist = self.distance(player)
        if self.radius < 0.9*player.radius and dist < player.radius + self.radius:
            return True
        else:
            return False
    
    
    
    
    
    
    
    
    
    
    ''' RANDOM POSITION/DIRECTION CALCULATIONS'''
    
    # Returns random position within rail
    def rand_position(self, rail) -> list[int]: # [x_position, y_position]
        if rail == "BOTTOM":
            return [randint(0, WIN_WIDTH), WIN_HEIGHT + SPAWN_OFFSET]
        elif rail == "TOP":
            return [randint(0, WIN_WIDTH), -SPAWN_OFFSET]
        elif rail == "LEFT":
            return [-SPAWN_OFFSET, randint(0, WIN_HEIGHT)]
        elif rail == "RIGHT":
            return [WIN_WIDTH + SPAWN_OFFSET, randint(0, WIN_HEIGHT)]  
        else:
            raise ValueError("Unknown rail value")
    
    # Returns random Vector based on rail position
    def rand_direction(self, rail) -> pygame.math.Vector2:
        if rail == "BOTTOM":
            vector = [uniform(-self.pos[0], WIN_WIDTH-self.pos[0]), -(WIN_HEIGHT//2)]
        elif rail == "TOP":
            vector = [uniform(-self.pos[0], WIN_WIDTH-self.pos[0]), WIN_HEIGHT//2]
        elif rail == "LEFT":
            vector = [WIN_HEIGHT//2, uniform(-self.pos[1], WIN_HEIGHT-self.pos[1])]
        elif rail == "RIGHT":
            vector = [-(WIN_HEIGHT//2), uniform(-self.pos[1], WIN_HEIGHT-self.pos[1])]
        return pygame.math.Vector2(vector[0], vector[1]).normalize()
    
    
    
    
    
    
    
    
    
    
    ''' DEBUG FUNCTIONS '''
    
    def show_size(self, WIN, show_level) -> None: # Returns either blob radius or level based on show_level
        size = self.radius
        if show_level:
            size = int(0.5*size - 5)
            
        velocity = debug_font.render(str(size), True, "black")
        WIN.blit(velocity, (self.pos[0], self.pos[1]))
    
    def show_velocity(self, WIN) -> None:
        velocity = debug_font.render(str(self.speed), True, "black")
        WIN.blit(velocity, (self.pos[0], self.pos[1]))
    
    def show_distance(self, WIN, player) -> None:
        distance = debug_font.render(str(self.distance(player)), True, "black")
        #func = debug_font.render(str(self.radius - 0.6*player.radius), True, "black")
        WIN.blit(distance, (self.pos[0], self.pos[1]))
        #WIN.blit(func, (self.pos[0], self.pos[1] + DEBUG_FONT_SIZE))
        
