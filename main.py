import pygame
from blob import Blob
from player import Player
from constants import WIN_WIDTH, WIN_HEIGHT, PLAYER_COLOR
from spawn_algorithm_2 import blob_spawn_speed

pygame.init()
pygame.mouse.set_visible(False) # Sets mouse invisible

# Window Constants
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BACKGROUND_COLOR = (170, 180, 190)

# Blob Constants
FPS = 60
SPAWN_SPEED = 20

# Fonts
text_font = pygame.font.SysFont("arialblack", 50)
score_font = pygame.font.SysFont("arialblack", 35)
debug_font = pygame.font.SysFont("arialblack", 20)

blob_group = pygame.sprite.Group()




    
''' MAIN LOOP '''
def main_loop():
    clock = pygame.time.Clock()
    player = Player()
    
    # Game state variables
    run = True
    game_over = True
    has_won = False
    start_animation = False
    
    # Debug variables
    is_paused = False
    is_show_size = False
    is_show_vel = False
    is_show_dist = False
    
    # Spawn frequency variables
    spawn_speed = 20
    blob_loop = 0
    
    score = 0
    high_score = 0
    start_animation_num = 50
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get(): # Gets all keyboard inputs
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Debug mode if press 'space'
                    is_paused = not is_paused
                
                if is_paused: # Debug Mode
                    if event.key == pygame.K_s: # Shows size if press 's'
                        is_show_vel = False
                        is_show_dist = False
                        is_show_size = not is_show_size
                    
                    if event.key == pygame.K_v: # Shows velocity if press 'v'
                        is_show_size = False
                        is_show_dist = False
                        is_show_vel = not is_show_vel

                    if event.key == pygame.K_d: # Shows distance between blob and player if press 'd'
                        is_show_size = False
                        is_show_vel = False
                        is_show_dist = not is_show_dist
                    
                    if event.key == pygame.K_c: # Removes all blobs if press 'c'
                        kill_blob_group()
                                           
                    if event.key == pygame.K_UP: # Increases player radius if press 'up'
                        player.radius += 2
                    
                    if event.key == pygame.K_DOWN: # Decreases player radius if press 'down'
                        player.radius -= 2
                 
                    
            if event.type == pygame.MOUSEBUTTONDOWN and game_over: # Starting screen
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # For 'press to start' in starting screen
                if mouse_x > 425 and mouse_x < 475 and mouse_y > 225 and mouse_y < 275:
                    start_animation = True
                    score = 0


        if start_animation: # Grows\h'press to start' circle until it fills screen, it will then start the game
            pygame.draw.circle(WIN, BACKGROUND_COLOR, [WIN_WIDTH/2, WIN_HEIGHT/2], start_animation_num)
            draw_player(player)
            if start_animation_num < 700:
                start_animation_num += 5
            else:
                start_animation = False
                game_over = False
                is_paused = False
                start_animation_num = 50
        
        
        elif game_over:
            death_screen(score_font, score, high_score)
            kill_blob_group()
        
        elif has_won:
            win_screen(text_font)
            kill_blob_group()
        
        else:
            if is_paused:
                debug_mode(WIN, player, is_show_size, is_show_vel, is_show_dist)
            
            else:
                if blob_loop % spawn_speed == 0:
                    Blob(blob_group, player.radius)
                blob_loop += 1
                
                dt = clock.tick() / 1000
                game_screen(dt, player)
                
            # Blob eating player/player eating blob logic
            for blob in blob_group:
                if blob.is_touching(player):
                    if blob.can_eat(player):
                        player.radius = 10 # Resets player size
                        game_over = True
                        if score > high_score:
                            high_score = score
                    if blob.can_be_eaten(player):
                        blob.kill()
                        score += 1
                        player.radius += 2
                        spawn_speed = blob_spawn_speed(player.radius) # Updates spawn speed
                        if player.radius > WIN_HEIGHT:
                            has_won = True

            
            # Score (top left)
            img = score_font.render(str(score), True, "black")
            WIN.blit(img, (50, 50))
            
        pygame.display.update()





''' DRAWING SPRITES '''
def draw_player(player):
    player.x, player.y = pygame.mouse.get_pos()
    pygame.draw.circle(WIN, player.color, [player.x, player.y], player.radius) # Draws player

def draw_blobs(WIN, dt):
    blob_group.draw(WIN)
    blob_group.update(dt)
    
def game_screen(dt, player):
    WIN.fill(BACKGROUND_COLOR)
    draw_player(player)
    draw_blobs(WIN, dt)
    
    
    
''' REMOVING SPRITES'''
def kill_blob_group():
    if len(blob_group) > 0:
        for blob in blob_group:
            blob.kill()




''' GAME OVER SCREEN '''
def death_screen(font, score: int, high_score: int):
    player = Player() # Resets player
          
    image = pygame.image.load("blobs_main_screen.png") # Main screen image
    WIN.blit(image, (0, 0))
    
    score_text = font.render(str(score), True, "black") # Score
    WIN.blit(score_text, (165, 29))
    
    high_score_text = font.render(str(high_score), True, "black") # Highscore
    WIN.blit(high_score_text, (240, 87))
    
    pygame.draw.circle(WIN, BACKGROUND_COLOR, [WIN_WIDTH/2, WIN_HEIGHT/2], 50)
    
    draw_player(player)
            

''' WIN SCREEN '''
def win_screen(font):
    player = Player() # Resets player
       
    WIN.fill(PLAYER_COLOR)
    img = font.render(f"You won!", True, "white") # Score UI
    WIN.blit(img, (335, 150))
    pygame.draw.rect(WIN, "white", pygame.Rect(425, 225, 50, 50)) # Box for retry
    
    draw_player(player) 


''' DEBUG MODE SCREEN '''
def debug_mode(WIN, player, is_show_size, is_show_vel, is_show_dist):
    WIN.fill(BACKGROUND_COLOR)
    draw_player(player)
    
    blob_group.draw(WIN)
    
    if is_show_size:
        show_level = False
        for blob in blob_group:
            blob.show_size(WIN, show_level)
        player.show_size(WIN, show_level)
    
    if is_show_vel:
        for blob in blob_group:
            blob.show_velocity(WIN)
    
    if is_show_dist:
        for blob in blob_group:
            blob.show_distance(WIN, player)

    
    
    
if __name__ == "__main__":
    main_loop()


