"""General information on your module and what it does."""
import coda_kids as coda

#load sprites
TILE_IMAGES = [None,                     # Sky
               coda.Image("Ground.png"), # Ground
               coda.Image("Hazard.png"), # Hazard
               coda.Image("Exit.png"),   # Door
               None,                     # Player
               coda.Image("Coin.png")]   # Coin

PLAYER_IMAGE = coda.Image("player.png")

#constants
SKY = 0
GROUND = 1
HAZARD = 2
DOOR = 3
PLAYER_START = 4
COINS = 5

PLAYER_START_HEALTH = 10
PLAYER_ACCEL = 16
GRAVITY_ACCEL = 98
PLAYER_DECEL = 500
PLAYER_MAX_SPEED = 64

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
        bar_color = coda.color.GREEN
    elif health > max_health - max_health * 0.5:
        bar_color = coda.color.YELLOW
    else:
        bar_color = coda.color.RED

    width = max_size[0] * (health / max_health)
    coda.draw_rect(screen, bar_color, location, (width, max_size[1]))

def load_level(level_name_as_string):
    """Cleans up resources and loads a specified level. Can be used to reload the same level."""
    cleanup()
    MY.tilemap = coda.utilities.read_file(level_name_as_string + ".txt")
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

def update(delta_time):
    """Update method for platform state."""
    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.key_down(event, " ") and (MY.grounded or MY.level_num > 1):
            MY.player.velocity.y = -12
            MY.grounded = False

    if coda.event.key_held_down("a"):
        MY.player.velocity.x = max(MY.player.velocity.x - PLAYER_ACCEL, -PLAYER_MAX_SPEED)
    elif coda.event.key_held_down("d"):
        MY.player.velocity.x = min(MY.player.velocity.x + PLAYER_ACCEL, PLAYER_MAX_SPEED)
    elif MY.grounded:
        if MY.player.velocity.x > 0:
            MY.player.velocity.x = max(0, MY.player.velocity.x - PLAYER_DECEL)
            print(MY.player.velocity.x)
        elif MY.player.velocity.x < 0:
            MY.player.velocity.x = min(0, MY.player.velocity.x + PLAYER_DECEL)
            print(MY.player.velocity.x)
    load = False
    print(MY.grounded)
    if coda.event.key_held_down("w"):
        for door in MY.doors:
            if MY.player.collides_with(door):
                load = True

    if load is True:
        MY.level_num += 1
        if MY.level_num < 4:
            load_level("level" + str(MY.level_num))
        else:
            coda.state.change(2)
        return

    # Gravity
    if not MY.grounded:
        MY.player.velocity.y = min(MY.player.velocity.y + GRAVITY_ACCEL, PLAYER_MAX_SPEED)

    # Check for hazard collisions
    for hazard in MY.hazards:
        if MY.player.collides_with(hazard):
            MY.player_health -= 2
            if MY.player_health <= 0:
                coda.state.change(1)
            else:
                MY.player.location = MY.player_start_position
                MY.player.set_velocity(0, 0)
                break
    for coin in MY.coins:
        if MY.player.collides_with(coin):
            MY.coins.remove(coin)
            MY.player_health += 1
    
    MY.player.update(delta_time)

    # check for wall collisions
    touching = False
    for wall in MY.walls:
        if MY.player.collides_with(wall):
            if MY.player.collision[coda.dir.DOWN]:
                MY.player.snap_to_object_y(wall, coda.dir.DOWN)
                MY.player.velocity.y = 0
                MY.grounded = touching = True
                continue
            if MY.player.collision[coda.dir.LEFT]:
                MY.player.snap_to_object_x(wall, coda.dir.LEFT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[coda.dir.RIGHT]:
                MY.player.snap_to_object_x(wall, coda.dir.RIGHT)
                MY.player.velocity.x = 0
                touching = True
                continue
            if MY.player.collision[coda.dir.UP]:
                MY.player.snap_to_object_y(wall, coda.dir.UP)
                MY.player.velocity.y = 0
                touching = True
                continue
    if not touching:
        MY.grounded = False

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
