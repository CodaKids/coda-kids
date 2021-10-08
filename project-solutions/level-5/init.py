#============================================================
#PART 1: IMPORTING DEPENDENCIES AND ASSIGNING GLOBAL VARIABLES
"""General information on your module and what it does."""
import pygame
from types import ModuleType
import sys
import math
import time
import random
from os import path

# Global color values
BLUE = [0, 192, 255, 128]
GREEN = [0, 128, 0, 128]
RED = [255, 0, 0]
YELLOW = [255, 255, 0]

# Global direction variables
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

# data used to store all lerps
_data = {}

#Path to level file
LEVEL_FILE_PATH = ''

#============================================================
# PART 2: CREATING A FRAMEWORK OF GENERAL CLASSES AND FUNCTIONS

def key_down(event, key):
    """
    Checks if the keyboard key is pressed.

        for ev in coda.event.listing():
            # Space key pressed.
            if coda.event.key_down(ev, " "):
                do_things();
    """
    if isinstance(key, str):
        return event.type == pygame.KEYDOWN and event.key == ord(key)
    return event.type == pygame.KEYDOWN and event.key == key

def key_held_down(key):
    """
    Checks if a key is being held down over multiple frames.

        # 'a' key held down.
        if coda.key_held_down("a"):
            do_things();
    """
    if isinstance(key, str):
        return pygame.key.get_pressed()[ord(key)]
    return pygame.key.get_pressed()[key]

def draw_rect(screen, color, top_left, size):
    """
    Draw's a rectangle with the given values. Doesn't return.

        coda.draw_rect(SCREEN, (r, g, b, a), (0, 0), (10, 10));
    """
    pygame.draw.rect(screen, color, (top_left[0], top_left[1], size[0], size[1]))

def update(delta_time):
    """
    Update all of the lerps. Auto removes lerps when done.
    Called internally by the state manager.
    """
    to_delete = []
    for (obj, lerp_list) in _data.items():
        if not lerp_list:
            to_delete.append(obj)
        elif lerp_list[0].update(obj, delta_time):
            lerp_list.pop(0)
            # remove duplicates
            while lerp_list and lerp_list[0].end == getattr(obj, lerp_list[0].member):
                lerp_list.pop(0)

    for key in to_delete:
        del _data[key]

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs the image files from your folder.
    return path.join(path.dirname(__file__), fileName)

def read_file(filename):
    """Read a file line by line and return it as an array of strings."""
    # Create an empty array.
    array = []
    # Open our file for read.
    file = open(get_file(filename), 'r')

    # put all the lines in an array
    for line in file:
        array.append(line.rstrip())

    return array

class Image:
    def __init__(self, image_file_name):
        if image_file_name is not None:
            self.data = pygame.image.load(get_file(image_file_name))
        else:
            self.data = None

    def update(self, dt):
        return

    def surface(self):
        return self.data

class SpriteSheet:
    """
    Sprite sheet class for managing sprite animations.

        sheet = SpriteSheet("image.png", (16, 16));
    """

    def __init__(self, filename, frame_size, scale=1):
        self.sheet = pygame.image.load(get_file(filename)).convert_alpha()
        rect = self.sheet.get_rect()
        self.sheet = pygame.transform.scale(self.sheet, (int(scale*rect.width), int(scale*rect.height)))
        rect = self.sheet.get_rect()
        self.columns = int (rect.width / int(frame_size[0] * scale) )
        self.rows = int ( rect.height / int(frame_size[1] * scale) )
        rect.width = int(frame_size[0] * scale)
        rect.height = int(frame_size[1] * scale)
        self.rectangle = rect

    def image_at(self, index):
        """
        Get an image at the given 0 based index.

            obj.sprite = sheet.image_at(0);
        """
        x = math.floor(index % self.columns) * self.rectangle.width
        y = math.floor(index / self.columns) * self.rectangle.height
        self.rectangle.centerx = x + self.rectangle.width / 2
        self.rectangle.centery = y + self.rectangle.height / 2
        image = Image(None)
        image.data = pygame.Surface(self.rectangle.size, pygame.SRCALPHA, 32).convert_alpha()
        image.data.blit(self.sheet, (0, 0), self.rectangle)
        return image

    def num_frames(self):
        """
        Return the number of frames of animation for the given sheet.

            size = sheet.num_frames();
        return self.columns * self.rows
        """
        return self.columns * self.rows

class Animator:

    def __init__(self, sheet, duration_seconds, looping= True):
        self.sheet = sheet
        self.frame_num = 0

        self.frame_time = 0.0

        self.playing = True
        self.playspeed = 1.0
        self.looping = looping

        self.reset()
        self.set_duration(duration_seconds)
    
    def set_duration(self, duration_seconds):
        self.duration = duration_seconds
        self.transition = self.duration / self.num_frames
    
    def use_anim(self, sheet):
        self.sheet = sheet
        self.reset()

    def reset(self):
        self.frame_num = 0
        self.current = self.sheet.image_at(self.frame_num)
        self.frame_time = 0
        self.num_frames = self.sheet.num_frames()

    def play(self, playspeed=1.0):
        self.playspeed = playspeed
        self.reset()
        self.unpause()

    def pause(self):
        self.playing = False

    def unpause(self):
        self.playing = True

    def update(self, dt):
        dt = dt * self.playspeed

        if self.playing:
            self.frame_time += dt

            if self.frame_time >= self.transition:
                self.frame_time -= self.transition
                self.frame_num += 1

                if self.looping:
                    self.frame_num %= self.num_frames

                self.current = self.sheet.image_at(self.frame_num)

                if self.frame_num >= self.num_frames:
                    self.playing = False

    def surface(self):
        return self.current.surface()

class Object:
    """
    Object class used to organize and track common game object data, such as location and appearance.

        obj = coda.Object(IMAGE);
    """
    location = pygame.math.Vector2(0, 0)
    scale = 1
    velocity = pygame.math.Vector2(0, 0)

    def __init__(self, image):
        self.sprite = image
        self.rotation = 0
        self.active = False
        self.collision = [False] * 5

    def __setattr__(self, name, value):
        if name == "location" or name == "velocity":
            self.__dict__[name] = pygame.math.Vector2(value[0], value[1])
        elif name == "rotation":
            self.__dict__[name] = value - 360 * int(value / 360)
        elif name == "sprite":
            if isinstance(value, Image):
                self.__dict__[name] = value
            elif isinstance(value, Animator):
                self.__dict__[name] = value
        else:
            self.__dict__[name] = value

    def get_transformed_rect(self):
        """
        Returns a transformed version of the object sprite. Generally for internal use only.

            rect = obj.get_transformed_rect();
        """
        sprite = pygame.transform.rotozoom(self.sprite.surface(), self.rotation, self.scale)
        rect = sprite.get_rect()
        rect.center = self.location
        return rect

    def width(self):
        """
        Gets the width of the object in reference to it's image data.

            width = obj.width();
        """
        rect = self.get_transformed_rect()
        return rect.width

    def height(self):
        """
        Gets the height of the object in reference to it's image data.

            height = obj.height();
        """
        rect = self.get_transformed_rect()
        return rect.height

    def add_rotation(self, degrees):
        """
        Add to the existing rotation of an object in degrees. Positive is clockwise.

            obj.add_rotation(90);
        """
        self.rotation = self.rotation + degrees
        self.rotation = self.rotation - 360 * int(self.rotation /360)

    def add_velocity(self, direction, speed, max_speed):
        """
        Add velocity to the object with the given direction and speed.

            obj.add_velocity((0, 1), 1, 10); # increase upwards
        """
        epsilon = 1.0e-15
        direction = pygame.math.Vector2(math.cos(math.radians(direction - 90)),
                            math.sin(math.radians(direction - 90)))
        if direction.x < epsilon and direction.x > 0:
            direction.x = 0

        if direction.y < epsilon and direction.y > 0:
            direction.y = 0

        vel = pygame.math.Vector2(-1 * direction.x * speed, direction.y * speed)

        self.velocity += vel
        distance_sq = self.velocity.length()

        if distance_sq > max_speed:
            self.velocity.normalize_ip()
            self.velocity *= max_speed

    def set_velocity(self, degrees, speed):
        """
        set velocity of the object with the given angle and speed.

            obj.set_velocity(45, 5); # left 5
        """
        self.velocity = pygame.math.Vector2(-1 * math.cos(math.radians(degrees - 90)) * speed,
                                math.sin(math.radians(degrees - 90)) * speed)

    def collides_with(self, other_obj):
        """
        Check if this object collides with the given object.

            if obj1.collides_with(obj2):
                do_things();
        """
        # check for early rejection.
        dist = (self.location - other_obj.location).length_squared()
        # if distance between objects is greater then 64^2
        if dist > 4096:
            self.collision[DOWN] = self.collision[UP] = False
            self.collision[LEFT] = self.collision[RIGHT] = False
            return False

        #get transformed rectangles
        rect1 = self.get_transformed_rect()
        rect2 = other_obj.get_transformed_rect()

        if not rect1.colliderect(rect2):
            return False

        self.collision[DOWN] = rect2.collidepoint((rect1.center[0] - rect1.width / 4, rect1.center[1] + rect1.height / 2)) or rect2.collidepoint((rect1.center[0] + rect1.width / 4, rect1.center[1] + rect1.height / 2))
        self.collision[UP] = rect2.collidepoint((rect1.center[0] - rect1.width / 4, rect1.center[1] - rect1.height / 2)) or rect2.collidepoint((rect1.center[0] + rect1.width / 4, rect1.center[1] - rect1.height / 2))
        self.collision[LEFT] = rect2.collidepoint((rect1.center[0] - rect1.width / 2, rect1.center[1] + rect1.height / 4)) or rect2.collidepoint((rect1.center[0] - rect1.width / 2, rect1.center[1] - rect1.height / 4))
        self.collision[RIGHT] = rect2.collidepoint((rect1.center[0] + rect1.width / 2, rect1.center[1] + rect1.height / 4)) or rect2.collidepoint((rect1.center[0] + rect1.width / 2, rect1.center[1] - rect1.height / 4))

        return True

    def snap_to_object_x(self, other_obj, facing):
        """
        Snaps the object to the left or right of the other object given.

            # Snap obj1 left of obj2
            obj1.snap_to_object_x(obj2, coda.dir.LEFT);
        """
        if facing == LEFT:
            self.location.x = (other_obj.location.x +
                               other_obj.width() / 2 +
                               self.width() / 2)
        else:
            self.location.x = (other_obj.location.x -
                               (other_obj.width() / 2 +
                                self.width() / 2))

    def snap_to_object_y(self, other_obj, facing):
        """
        Snaps the object to the left or right of the other object given.

            # Snap obj1 left of obj2
            obj1.snap_to_object(obj2, coda.dir.LEFT);
        """
        if facing == UP:
            self.location.y = (other_obj.location.y +
                               other_obj.height() / 2 +
                               self.height() / 2)
        else:
            self.location.y = (other_obj.location.y -
                               (other_obj.height() / 2 +
                                self.height() / 2))

    def collides_with_point(self, point):
        """
        Check if this object collides with the given position.

            # point
            obj.collides_with_point(10, 10);

            # Mouse position
            obj.collides_with_point(coda.event.mouse_position());
        """
        sprite = pygame.transform.rotate(self.sprite.surface(), self.rotation)
        rect = sprite.get_rect()
        location = self.location + self.velocity
        rect.center = location
        return rect.collidepoint(point)

    def update(self, delta_time):
        self.location += self.velocity * delta_time
        self.sprite.update(delta_time)

    def draw(self, screen):
        """
        draws the object to the screen.

            # draw the object
            obj.draw(SCREEN);
        """
        sprite = pygame.transform.rotozoom(self.sprite.surface(), self.rotation, self.scale)
        rect = sprite.get_rect()
        rect.center = self.location
        screen.blit(sprite, rect)

def start(window_size, game_name):
    """
    Initializes the library and returns a pygame screen. Call this first!

        SCREEN = coda.start((w, h), "Title");
    """
    pygame.init()
    time.sleep(2)
    random.seed(time.time())
    pygame.display.set_caption(game_name)
    pygame.mixer.init()
    return pygame.display.set_mode((int(window_size[0]), int(window_size[1])))

def stop():
    """
    Stops pygame and closes the window immediately.

        coda.stop();
    """
    sys.exit()

class Machine:
    """Game state machine class."""
    def __init__(self):
        self.current = 0
        self.previous = 0
        self.states = []

    def register(self, module):
        """Registers the state's init, update, draw, and cleanup functions."""
        self.states.append({'initialize': module.initialize,
                            'update': module.update,
                            'draw': module.draw,
                            'cleanup': module.cleanup})

    def run(self, screen, window, fill_color, tilemap):
        """Runs the state given machine."""
        clock = pygame.time.Clock()

        #Save filepath to level's tilemap
        global LEVEL_FILE_PATH
        LEVEL_FILE_PATH = tilemap

        # first run initialize!
        self.states[self.current]['initialize'](window)

        while True:
            delta_time = clock.tick(60) / 1000
            if self.current != self.previous:
                self.states[self.current]['cleanup']()
                self.states[self.current]['initialize'](window)
                self.previous = self.current

            update(delta_time)
            self.states[self.current]['update'](delta_time)
            screen.fill(fill_color)
            screen.blit(pygame.transform.scale(BACKGROUND_IMAGE.data, [int(x) for x in WINDOW]), (0, 0))
            self.states[self.current]['draw'](screen)
            pygame.display.flip()

Manager = Machine()

def change(new_state):
    """Requests a change in game state."""
    Manager.current = new_state

#============================================================
#PART 3: SETUP FOR THE CREEPERCHASE GAME
#Initializes the game window and game screen
WINDOW = pygame.math.Vector2(800, 608)
SCREEN = start(WINDOW, "Creeper Chase")

#load sprites
TILE_IMAGES = [None,                     # Sky
               Image("assets/Ground.png"), # Ground
               Image("assets/Hazard.png"), # Hazard
               Image("assets/Exit.png"),   # Door
               None,                     # Player
               Image("assets/Coin.png")]   # Coin

BACKGROUND_IMAGE = Image("assets/Background.png")
PLAYER_IMAGE = Image("assets/player.png")

# Constants
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

#Loads modifiable data for gameplay
class Data:
    """Place modifiable data here."""
    tilemap = []
    sky = []
    walls = []
    hazards = []
    doors = []
    coins = []
    start_time = 0

    ground_cookie = SpriteSheet("assets/Cookie.png", (32, 32), 0.5).image_at(0)
    ground_cupcake = SpriteSheet("assets/Cupcake.png", (32, 32), 0.5).image_at(0)
    ground_marshmallow = SpriteSheet("assets/Marshmallow.png", (32, 32), 0.5).image_at(0)
    ground_marshmallow_chocolate = SpriteSheet("assets/Marshmallow_Chocolate.png", (32, 32), 0.5).image_at(0)
    ground_orange = SpriteSheet("assets/Orange.png", (32, 32), 0.5).image_at(0)

    ground_food = [ground_cookie, ground_cupcake, ground_marshmallow, ground_marshmallow_chocolate, ground_orange] 

    lava_ground_pulse_sheet = SpriteSheet("assets/ground_lava.png", (32, 32), 0.5)
    lava_ground_pulse = Animator(lava_ground_pulse_sheet, 1)

    hazard_lava_pulse_sheet = SpriteSheet("assets/hazard_lava.png", (32, 32), 0.6)
    hazard_lava_pulse = Animator(hazard_lava_pulse_sheet, 30)

    hazard_pepper_pulse_sheet = SpriteSheet("assets/hazard_pepper.png", (32, 32), 0.5)
    hazard_pepper_pulse = Animator(hazard_pepper_pulse_sheet, 8)

    portal_enter_closing_sheet = SpriteSheet("assets/portal_enter_closing.png", (128, 128), 0.25)
    portal_enter_closing = Animator(portal_enter_closing_sheet, 1)

    portal_enter_pulse_sheet = SpriteSheet("assets/portal_enter_idle.png", (128, 128), 0.25)
    portal_enter_pulse = Animator(portal_enter_pulse_sheet, 1)

    portal_exit_pulse_sheet = SpriteSheet("assets/portal_exit_idle.png", (128, 128), 0.25)
    portal_exit_pulse = Animator(portal_exit_pulse_sheet, 1)

    portal_exit_closing_sheet = SpriteSheet("assets/portal_exit_closing.png", (128, 128), 0.25)
    portal_exit_closing = Animator(portal_exit_closing_sheet, 1)

    paul_idle_right_sheet = SpriteSheet("assets/paul_idle_right.png", (64, 64), 0.5)
    paul_idle_right = Animator(paul_idle_right_sheet, 1)

    paul_idle_left_sheet = SpriteSheet("assets/paul_idle_left.png", (64, 64), 0.5)
    paul_idle_left = Animator(paul_idle_left_sheet, 1)

    paul_run_right_sheet = SpriteSheet("assets/paul_run_right.png", (64, 64), 0.5)
    paul_run_right = Animator(paul_run_right_sheet, 1)

    paul_run_left_sheet = SpriteSheet("assets/paul_run_left.png", (64, 64), 0.5)
    paul_run_left = Animator(paul_run_left_sheet, 1)

    paul_fall_right_sheet = SpriteSheet("assets/paul_fall_right.png", (64, 64), 0.5)
    paul_fall_right = Animator(paul_fall_right_sheet, 1)

    paul_fall_left_sheet = SpriteSheet("assets/paul_fall_left.png", (64, 64), 0.5)
    paul_fall_left = Animator(paul_fall_left_sheet, 1)

    paul_pain_right_sheet = SpriteSheet("assets/paul_pain_right.png", (64, 64), 0.5)
    paul_pain_right = Animator(paul_pain_right_sheet, 1)

    paul_pain_left_sheet = SpriteSheet("assets/paul_pain_left.png", (64, 64), 0.5)
    paul_pain_left = Animator(paul_pain_left_sheet, 1)

    paul_jetpack_right_sheet = SpriteSheet("assets/paul_jetpack_right.png", (64, 64), 0.5)
    paul_jetpack_right = Animator(paul_jetpack_right_sheet, 1)

    paul_jetpack_left_sheet = SpriteSheet("assets/paul_jetpack_left.png", (64, 64), 0.5)
    paul_jetpack_left = Animator(paul_jetpack_left_sheet, 1)

    creeper_exit_sheet = SpriteSheet("assets/creeper_exit.png", (80, 80), 0.40)
    creeper_exit = Animator(creeper_exit_sheet, 1, False)


    player = Object(paul_idle_right_sheet.image_at(0))
    player.sprite = paul_idle_right
    player_health = PLAYER_START_HEALTH
    player_max_speed = 100
    player_start_position = pygame.math.Vector2(0, 0)
    player_direction = RIGHT

    creeper = Object(creeper_exit_sheet.image_at(0))

    entrance = Object(portal_enter_pulse_sheet.image_at(0))
    entrance.sprite = portal_enter_pulse

    exit_portal = Object(portal_exit_pulse_sheet.image_at(0))
    exit_portal.sprite = portal_exit_pulse
            
    grounded = False
    can_fly = False
    level_num = 1
    window = pygame.math.Vector2(0, 0)



# Initializes the data
MY = Data()

def health_bar(screen, health, max_health, max_size, location):
    """Creates a health bar at the given position."""
    if health > max_health - max_health * 0.25:
        bar_color = GREEN
    elif health > max_health - max_health * 0.5:
        bar_color = YELLOW
    else:
        bar_color = RED

    width = max_size[0] * (health / max_health)
    draw_rect(screen, bar_color, location, (width, max_size[1]))

def load_level(level_file_path):
    """Cleans up resources and loads a specified level. Can be used to reload the same level."""
    cleanup()

    MY.tilemap = level_file_path 
    for row in range(len(MY.tilemap)):
        for column in range(len(MY.tilemap[row])):
            obj = Object(TILE_IMAGES[int(MY.tilemap[row][column])])
            obj.location = pygame.math.Vector2(column * TILE_SIZE + TILE_SIZE/2, row * TILE_SIZE + TILE_SIZE/2)
            if int(MY.tilemap[row][column]) == GROUND:
                ground_obj = Object(MY.lava_ground_pulse_sheet.image_at(random.randint(0,3)))
                ground_obj.sprite = MY.lava_ground_pulse
                # ground_obj = Object(random.choice(MY.ground_food)) 
                ground_obj.location = pygame.math.Vector2(column * TILE_SIZE + TILE_SIZE/2, row * TILE_SIZE + TILE_SIZE/2)
                MY.walls.append(ground_obj)
            elif int(MY.tilemap[row][column]) == HAZARD:
                hazard_obj = Object(MY.hazard_lava_pulse_sheet.image_at(0))
                hazard_obj.sprite = MY.hazard_lava_pulse
                hazard_obj.location = pygame.math.Vector2(column * TILE_SIZE + TILE_SIZE/2, row * TILE_SIZE + TILE_SIZE/2)
                MY.hazards.append(hazard_obj)
            elif int(MY.tilemap[row][column]) == DOOR and row < len(MY.tilemap) - 1 and int(MY.tilemap[row + 1][column]) == DOOR:
                MY.exit_portal.location = pygame.math.Vector2(column * TILE_SIZE + TILE_SIZE/2, row * TILE_SIZE + TILE_SIZE/2)
                MY.creeper.location = pygame.math.Vector2((column - 1) * TILE_SIZE + TILE_SIZE/2, row * TILE_SIZE + TILE_SIZE/2)
            elif int(MY.tilemap[row][column]) == PLAYER_START:
                MY.player_start_position = obj.location
            elif int(MY.tilemap[row][column]) == COINS:
                MY.coins.append(obj)

    MY.player.location = MY.player_start_position
    MY.entrance.location = MY.player_start_position
    MY.start_time = pygame.time.get_ticks()

def initialize(window):
    """Initializes the Platformer state."""
    MY.player_health = PLAYER_START_HEALTH
    MY.player.velocity = pygame.math.Vector2(0, 0)
    MY.level_num = 1
    load_level(LEVEL_FILE_PATH)
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
    
    # draw coins
    for coin in MY.coins:
        coin.draw(screen)

    # draw player
    MY.player.draw(screen)
    MY.exit_portal.draw(screen)

    if pygame.time.get_ticks() - MY.start_time < 1500:
        MY.creeper.draw(screen)
        MY.entrance.draw(screen)
    elif pygame.time.get_ticks() - MY.start_time < 4000:
        MY.creeper.sprite = MY.creeper_exit
        MY.entrance.sprite = MY.portal_enter_closing
        MY.creeper.draw(screen)
        MY.entrance.draw(screen)
    
    #draw player health_bar
    health_bar(screen, MY.player_health, 10, (128, 16), (MY.window.x * 0.75, 20))

def update_level(delta_time):
    # MY.player.update(delta_time)
    for wall in MY.walls:
        wall.update(delta_time)
    for hazard in MY.hazards:
        hazard.update(delta_time)
    for door in MY.doors:
        door.update(delta_time)
    
    MY.creeper.update(delta_time)
    MY.entrance.update(delta_time)
    MY.exit_portal.update(delta_time)
    
    # if pygame.time.get_ticks() - MY.start_time < 1000:
    #     MY.creeper.update(delta_time)
    
def cleanup():
    """Cleans up the Platformer State."""
    MY.tilemap = []
    MY.sky = []
    MY.walls = []
    MY.hazards = []
    MY.doors = []
    MY.coins = []

class Win:
    #load sprites
    BUTTON_IMAGE = Image("assets/WinButton.png")

    class Data:
        button = Object(Image("assets/WinButton.png"))

    MY = Data()


    def initialize(self, window):
        """Initializes the lose menu state."""
        MY.button.location = window / 2

    def update(self, delta_time):
        """Updates the lose menu state."""
        for event in event.listing():
            if event.quit_game(event):
                stop()
            elif event.mouse_l_button_down(event):
                if MY.button.collides_with_point(event.mouse_position()):
                    change(0)

    def draw(self, screen):
        """Draws the lose menu state."""
        MY.button.draw(screen)

    def cleanup():
        """Cleans up the lose menu state."""

class Lose:
    #load sprites
    BUTTON_IMAGE = Image("assets/LoseButton.png")

    class Data:
        button = Object(Image("assets/LoseButton.png"))

    MY = Data()

    def initialize(self, window):
        """Initializes the lose menu state."""
        MY.button.location = window / 2

    def update(self, delta_time):
        """Updates the lose menu state."""
        for event in event.listing():
            if event.quit_game(event):
                stop()
            elif event.mouse_l_button_down(event):
                if MY.button.collides_with_point(event.mouse_position()):
                    change(0)

    def draw(self, screen):
        """Draws the lose menu state."""
        MY.button.draw(screen)

    def cleanup():
        """Cleans up the lose menu state."""
