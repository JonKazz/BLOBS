from random import randint

# Velocity Constants
MIN_S_VEL = 4
MAX_S_VEL = 8
MIN_M_VEL = 3
MAX_M_VEL = 6 # 6
MIN_L_VEL = 2 # 2
MAX_L_VEL = 4 # 4

''' PLAYER TYPE CONSTANTS '''
TINY_TYPE = 14 # Score 0 - 4
SMALL_TYPE = 20 # Score 4 - 10
MEDIUM_TYPE = 30 # Score 10 - 20
LARGE_TYPE = 40 # Score 20-30
XL_TYPE = 60 # Score 30-50


''' SPAWN RATE CONSTANTS '''
MIN_SPAWN_RATE = 15
MAX_SPAWN_RATE = 20


''' Testing Mode '''
easy_mode = False
if easy_mode:
    MAX_S_VEL = 3
    MAX_M_VEL = 3
    MAX_L_VEL = 3
    
def player_size_type(player_size: int) -> str:
    if player_size < TINY_TYPE:
        return "T"
    elif player_size < SMALL_TYPE:
        return "S"
    elif player_size < MEDIUM_TYPE:
        return "M"
    elif player_size < LARGE_TYPE:
        return "L"
    elif player_size < XL_TYPE:  
        return "XL"
    else:
        return "W"
      
def blob_size_speed(player_size: int) -> tuple:
    size_type = randint(1,10)
    
    if size_type < 3:
        return (small_size(player_size), randint(MIN_S_VEL, MAX_S_VEL))
    
    elif size_type < 5:
        return (med_size(player_size), randint(MIN_M_VEL, MAX_M_VEL))
    
    else:
        return (large_size(player_size), randint(MIN_L_VEL, MAX_L_VEL))


# Linearly grows spawn speed with player size
def blob_spawn_speed(player_size: int) -> int:
    return int((1/6)*(player_size-10) + 15)


def large_size(player_size: int) -> int:
    player_type = player_size_type(player_size)
    if player_type == "T":
        return randint(30, 60)
    elif player_type == "S":
        return randint(player_size*2, (player_size+8)*3)
    elif player_type == "M":
        return randint(player_size*2, (player_size+5)*3)
    elif player_type == "L":
        return randint(player_size*2, player_size*3)
    elif player_type == "XL":
        return randint(player_size, player_size+4)
    else:
        return player_type//2


def med_size(player_size: int) -> int:
    player_type = player_size_type(player_size)
    if player_type == "T":
        return randint(player_size, player_size*4)
    elif player_type == "S":
        return randint(player_size, player_size*3)
    elif player_type == "M":
        return randint(player_size, (player_size+5)*2)
    elif player_type == "L":
        return randint(player_size, player_size*2)
    elif player_type == "XL":
        return randint(player_size - 10, player_size + 6)
    return player_type//5

def small_size(player_size: int) -> int:
    player_type = player_size_type(player_size)
    print(player_type)
    if player_type == "T" or player_type == "S":
        return randint(player_size//2, player_size)
    elif player_type == "M" or player_type == "H":
        return randint(player_size//3, player_size-3)
    elif player_type == "XL":
        return(randint(player_size//5, player_size))
    else:
        return player_type//10