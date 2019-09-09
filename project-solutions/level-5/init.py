"""General information on your module and what it does."""
import coda

# global data
WINDOW = coda.Vector2(800, 608)
SCREEN = coda.start(WINDOW, "Demo Project 4")

#load sprites
TILE_IMAGES = [None,                     # Sky
               coda.Image("assets/Ground.png"), # Ground
               coda.Image("assets/Hazard.png"), # Hazard
               coda.Image("assets/Exit.png"),   # Door
               None,                     # Player
               coda.Image("assets/Coin.png")]   # Coin

PLAYER_IMAGE = coda.Image("assets/player.png")

#constants
SKY = 0
GROUND = 1
HAZARD = 2
DOOR = 3
PLAYER_START = 4
COINS = 5

PLAYER_START_HEALTH = 10
PLAYER_ACCEL = 64
GRAVITY_ACCEL = 70
PLAYER_DECEL = 500
PLAYER_AIR_DECEL = 10
PLAYER_MAX_SPEED = 128
PLAYER_TERMINAL_VEL = 128

TILE_SIZE = 16

#modifiable data
class Data:
    """Place modifiable data here."""
    tilemap = []
    sky = []
    walls = []

    hazards = []
    doors = []
    coins = []
    player = coda.Object(PLAYER_IMAGE)
    player_health = PLAYER_START_HEALTH
    player_max_speed = 100
    player_start_position = coda.Vector2(0, 0)
    grounded = False
    can_fly = False
    level_num = 1
    window = coda.Vector2(0, 0)

MY = Data()

def health_bar(screen, health, max_health, max_size, location):
    """Creates a health bar at the given position."""
    if health > max_health - max_health * 0.25:
        bar_color = coda.GREEN
    elif health > max_health - max_health * 0.5:
        bar_color = coda.YELLOW
    else:
        bar_color = coda.RED

    width = max_size[0] * (health / max_health)
    coda.draw_rect(screen, bar_color, location, (width, max_size[1]))

def load_level(level_name_as_string):
    """Cleans up resources and loads a specified level. Can be used to reload the same level."""
    cleanup()
    MY.tilemap = coda.read_file("assets/"+level_name_as_string + ".txt")
    for row in range(len(MY.tilemap)):
        for column in range(len(MY.tilemap[row])):
            obj = coda.Object(TILE_IMAGES[int(MY.tilemap[row][column])])
            obj.location = coda.Vector2(column * TILE_SIZE + 8, row * TILE_SIZE + 8)
            if int(MY.tilemap[row][column]) == GROUND:
                MY.walls.append(obj)
            elif int(MY.tilemap[row][column]) == HAZARD:
                MY.hazards.append(obj)
            elif int(MY.tilemap[row][column]) == DOOR:
                MY.doors.append(obj)
            elif int(MY.tilemap[row][column]) == PLAYER_START:
                MY.player_start_position = obj.location
            elif int(MY.tilemap[row][column]) == COINS:
                MY.coins.append(obj)
    MY.player.location = MY.player_start_position

def initialize(window):
    """Initializes the Platformer state."""
    MY.player_health = PLAYER_START_HEALTH
    MY.player.velocity = coda.Vector2(0, 0)
    MY.level_num = 1
    load_level("level" + str(MY.level_num))
    MY.window = window

def draw(screen):
    """Draws the platformer state to the given screen."""
    # draw tilemap walls
    for wall in MY.walls:
        wall.draw(screen)
    # draw tilemap hazard
    for hazard in MY.hazards:
        hazard.draw(screen)
    for door in MY.doors:
        door.draw(screen)
    # draw player
    MY.player.draw(screen)
    # draw coins
    for coin in MY.coins:
        coin.draw(screen)
    #draw player health_bar
    health_bar(screen, MY.player_health, 10, (128, 16), (MY.window.x / 2, 4))

def cleanup():
    """Cleans up the Platformer State."""
    MY.tilemap = []
    MY.sky = []
    MY.walls = []
    MY.hazards = []
    MY.doors = []
    MY.coins = []