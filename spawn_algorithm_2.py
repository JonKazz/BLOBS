from random import randint

''' VELOCITY CONSTANTS'''
MIN_S_VEL = 4
MAX_S_VEL = 8
MIN_M_VEL = 3
MAX_M_VEL = 6 
MIN_L_VEL = 2 
MAX_L_VEL = 4 

''' Takes radius, converts to level'''
def convert_level(player_radius: int) -> int:
    return int(0.5*player_radius - 5)

''' Takes level, converts to radius '''
def convert_radius(player_level : int) -> int:
    return 2*player_level + 10

def blob_size_speed(player_radius: int) -> tuple:
    size_type = randint(1,10)
    player_level = convert_level(player_radius)
    
    if player_level > 49: # Winning score
        return (randint(40, 80), MAX_S_VEL)
    
    elif size_type < 3:
        return (small_blob(player_level), randint(MIN_S_VEL, MAX_S_VEL))
    
    elif size_type < 6:
        return (medium_blob(player_level), randint(MIN_M_VEL, MAX_M_VEL))
    
    else:
        return (large_blob(player_level), randint(MIN_L_VEL, MAX_L_VEL))


# Linearly grows spawn speed with player size
def blob_spawn_speed(player_size: int) -> int:
    player_level = convert_level(player_size)
    if player_level > 50:
        return 1
    return int(0.1*player_level + 20)

def large_blob(player_level: int) -> int: # Returns radius
    max_size = 65
    min_size = int(0.5*player_level + 25)
    return convert_radius(randint(min_size, max_size))

def medium_blob(player_level: int) -> int: # Returns radius
    max_size = int(0.5*player_level + 30)
    min_size = int(0.5*player_level + 20)
    return convert_radius(randint(min_size, max_size))

def small_blob(player_level: int) -> int: # Returns radius
    max_size = int(0.5*player_level)
    min_size = int(0.5*player_level - 2)
    return convert_radius(randint(min_size, max_size))