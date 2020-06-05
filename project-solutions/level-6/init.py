#=============================================================
#PART 1: IMPORTING DEPENDENCIES AND ASSIGNING GLOBAL VARIABLES
import pygame
import random
import time
from os import path
import math
import sys

# colors
WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
GREEN = [0, 128, 0, 128]
BLUE = [0, 192, 255, 128]

# directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

_data = {}

x_value = 0
y_value = 0

#============================================================
#PART 2: CREATING A FRAMEWORK OF GENERAL CLASSES AND FUNCTIONS
def start(window, name):
    """Initialize pygame and random seed."""
    pygame.init()
    random.seed(time.time())
    pygame.display.set_caption(name)
    return pygame.display.set_mode((int(window[0]), int(window[1])))

def stop():
    """
    Stops pygame and closes the window immediately.
        coda.stop();
    """
    sys.exit()

def check_stop():
    for event in pygame.event.get():
        # Checks if you closed the window
        if event.type == pygame.QUIT:
            stop()
        elif event.type == MY.boss_attack_event:
            MY.is_boss_attacking = True
            print("hello")
        else:
            MY.is_boss_attacking = False
            print("goodbye")
        

def draw_rect(screen, color, top_left, size):
    """
    Draw's a rectangle with the given values. Doesn't return.
        coda.draw_rect(SCREEN, (r, g, b, a), (0, 0), (10, 10));
    """
    pygame.draw.rect(screen, color, (top_left[0], top_left[1], size[0], size[1]))

def key_down(event, key):
    """
    Checks if the keyboard key is pressed.
        for ev in coda.event.listing():
            # Space key pressed.
            if coda.event.key_down(ev, " "):
                do_things();
    """
    if isinstance(key, str):
        return event.type == pygame.KEYDOWN and event.key == key
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

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs your files from your folder.
    return path.join(path.dirname(__file__), fileName)

def read_file(filename):
    """Read a file line by line and return it as an array of strings."""
    # Create an empty array.
    array = []
    # Open our file for read.
    file = open(filename, 'r')

    # put all the lines in an array
    for line in file:
        array.append(line.rstrip())

    return array

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

    def run(self, screen, window, fill_color):
        """Runs the state given machine."""
        clock = pygame.time.Clock()
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
            screen.blit(BACKGROUND_IMAGE.data, (0, 0))
            self.states[self.current]['draw'](screen)
            pygame.display.flip()

class Image:
    """Loads an image object"""
    def __init__(self, image_file_name):
        if image_file_name is not None:
            self.data = pygame.image.load(get_file(image_file_name)).convert_alpha()
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

    def __init__(self, filename, frame_size):
        self.sheet = pygame.image.load(get_file(filename)).convert_alpha()
        rect = self.sheet.get_rect()
        self.columns = rect.width / frame_size[0]
        self.rows = rect.height / frame_size[1]
        rect.width = frame_size[0]
        rect.height = frame_size[1]
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

class Object:
    """
    Object class used to organize and track common game object data, such as location and appearance.

        obj = Object(IMAGE);
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
            obj1.snap_to_object_x(obj2, LEFT);
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
            obj1.snap_to_object(obj2, LEFT);
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

class CountdownTimer:
    """
    Countdown timer class for timer logic.
        timer = CountdownTimer(seconds);
        if (timer.tick(delta_time)):
            do_things();
    """
    def __init__(self, max_time):
        """Initialize the timer with the given values."""
        self.max_time = max_time
        self.current_time = 0

    def tick(self, delta_time):
        """update timer and check if finished."""
        self.current_time += delta_time
        if self.current_time >= self.max_time:
            return False
        return True

class TextObject:
    """
    Create an object that renders text. Assumes that the default font 
    freesansbold exists in the project directory as a true type font.
        #create a text object
        title = TextObject(color.RED, 12, "example");
    """

    def __init__(self, color_value, font_size, text):
        self.location = pygame.math.Vector2(0, 0)
        self.color = color_value
        self.font_size = font_size
        self.text = text
        self.centered = False

    def __setattr__(self, name, value):
        if name == "location":
            self.__dict__[name] = pygame.math.Vector2(value[0], value[1])
        elif name == "font_size":
            self.__dict__[name] = value
            self.font = pygame.font.Font('freesansbold.ttf', int(self.font_size))
        else:
            self.__dict__[name] = value

    def draw(self, screen):
        """
        Draws the object text to the screen.
            text.draw(SCREEN);
        """

        obj = self.font.render(self.text, 1, self.color)
        loc = pygame.math.Vector2(self.location.x, self.location.y)
        if self.centered is True:
            loc.x -= obj.get_rect().width / 2
        screen.blit(obj, loc)

class Animator:
    def __init__(self, sheet, duration_seconds):
        self.sheet = sheet
        self.frame_num = 0

        self.frame_time = 0.0

        self.playing = True
        self.playspeed = 1.0
        self.looping = True

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

#============================================================
#PART 3: SETUP FOR THE BOSS BATTLE GAME
Manager = Machine()

window_width = 800
window_length = 600
WINDOW = pygame.math.Vector2(800, 600)
SCREEN = start(WINDOW, "Boss Battle")

#load sprites constants
PROJECTILE_IMAGE = Image("assets/Projectile.png")
HITBOX_IMAGE = Image("assets/Hitbox.png")
BACKGROUND_IMAGE = Image("assets/Background.png")
IMAGE_GAMEOVER = Image("assets/Background.png")
IMAGE_BUTTON = Image("assets/Background.png")

#constants
PLAYER = 0
BOSS = 1
GRASS = 4
TILE_SIZE = 32

class Data:
    """Modifiable data"""
    player_idle_forward_sheet = SpriteSheet("assets/paul/PaulIdleFront.png", (64, 64))
    player_idle_backward_sheet = SpriteSheet("assets/paul/PaulIdleBack.png", (64, 64))
    player_idle_left_sheet = SpriteSheet("assets/paul/PaulIdleLeft.png", (64, 64))
    player_idle_right_sheet = SpriteSheet("assets/paul/PaulIdleRight.png", (64, 64))
    idle_forward = Animator(player_idle_forward_sheet, 1)
    idle_backward = Animator(player_idle_backward_sheet, 1)
    idle_left = Animator(player_idle_left_sheet, 1)
    idle_right = Animator(player_idle_right_sheet, 1)
    player_walk_forward_sheet = SpriteSheet("assets/paul/PaulMoveFront.png", (64, 64))
    player_walk_backward_sheet = SpriteSheet("assets/paul/PaulMoveBack.png", (64, 64))
    player_walk_left_sheet = SpriteSheet("assets/paul/PaulMoveLeft.png", (64, 64))
    player_walk_right_sheet = SpriteSheet("assets/paul/PaulMoveRight.png", (64, 64))
    walk_forward = Animator(player_walk_forward_sheet, 1)
    walk_backward = Animator(player_walk_backward_sheet, 1)
    walk_left = Animator(player_walk_left_sheet, 1)
    walk_right = Animator(player_walk_right_sheet, 1)
    player_attack_forward_sheet = SpriteSheet("assets/paul/PaulAttackFront.png", (100, 100))
    player_attack_backward_sheet = SpriteSheet("assets/paul/PaulAttackBack.png", (100, 100))
    player_attack_left_sheet = SpriteSheet("assets/paul/PaulAttackLeft.png", (128, 64))
    player_attack_right_sheet = SpriteSheet("assets/paul/PaulAttackRight.png", (128, 64))
    attack_forward = Animator(player_attack_forward_sheet, 0.5)
    attack_backward = Animator(player_attack_backward_sheet, 0.5)
    attack_left = Animator(player_attack_left_sheet, 0.5)
    attack_right = Animator(player_attack_right_sheet, 0.5)
    player_pain_forward_sheet = SpriteSheet("assets/paul/PaulPainFront.png", (64, 64))
    player_pain_backward_sheet = SpriteSheet("assets/paul/PaulPainBack.png", (64, 64))
    player_pain_left_sheet = SpriteSheet("assets/paul/PaulPainLeft.png", (64, 64))
    player_pain_right_sheet = SpriteSheet("assets/paul/PaulPainRight.png", (64, 64))
    pain_forward = Animator(player_pain_forward_sheet, 0.5)
    pain_backward = Animator(player_pain_backward_sheet, 0.5)
    pain_left = Animator(player_pain_left_sheet, 0.5)
    pain_right = Animator(player_pain_right_sheet, 0.5)
    player = Object(player_walk_forward_sheet.image_at(2))
    player_start_position = pygame.math.Vector2(0, 0)
    player_health = 100
    player_dir = DOWN
    player_text = TextObject(BLACK, 24, "Player: ")
    player_hitbox = Object(HITBOX_IMAGE)
    wall_height = 45
    boss_attack_sheet = SpriteSheet("assets/creeper/CreeperAttack.png", (96, 96))
    boss_attack = Animator(boss_attack_sheet, 2)
    boss_idle_sheet = SpriteSheet("assets/creeper/CreeperIdle.png", (96, 96))
    boss_idle = Animator(boss_idle_sheet, 2.5)
    boss_pain_sheet = SpriteSheet("assets/creeper/CreeperPain.png", (96, 96))
    boss_pain = Animator(boss_pain_sheet, 0.5)
    boss = Object(boss_idle_sheet.image_at(0))
    boss_start_position = pygame.math.Vector2(0, 0)
    boss_health = 300
    boss_attacking = False
    numberOfprojectiles = 0
    projectiles = []
    projectile_owner = []
    rotation_speed = 180
    state = 0
    last_state = 2
    index = 0
    last = pygame.time.get_ticks()
    cooldown = 6000 
    #gameover class data
    #game_over_sheet = SpriteSheet("assets/GameOverLayover.png", (2000, 1500))
    game_over_sheet = SpriteSheet("assets/creeper/CreeperAttack.png", (96, 96))
    game_over = Animator(game_over_sheet, 2)
    #you_win_sheet = SpriteSheet("assets/YouWinLayover.png", (2000, 1500))
    you_win_sheet = SpriteSheet("assets/creeper/CreeperAttack.png", (96, 96))
    you_win = Animator(you_win_sheet, 2)
    ending_overlay = Object(game_over_sheet.image_at(0))
    restart_button = Object(Image("assets/Projectile.png"))
    display_text = TextObject(WHITE, 24, "")
    boss_attack_event = pygame.USEREVENT
    is_boss_attacking = False

class GameOver:
    MY = Data()

    def initialize(window):
        """Initializes the restart menu state."""
        MY.ending_overlay.location = window / 2
        MY.restart_button.location = window / 2
        pygame.time.set_timer(MY.boss_attack_event, 0)

    def update(delta_time):
        """Updates the restart menu state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if MY.restart_button.collides_with_point(pygame.mouse.get_pos()):
                    Manager.current = 0
                    MY.boss_health = 300
                    MY.player_health = 100

    def cleanup():
        """Cleans up the restart menu state."""
        MY.projectiles = []

    def draw(screen):
        """Draws the restart menu state."""
        #MY.ending_overlay.draw(screen)
        MY.restart_button.draw(screen)
        MY.display_text.draw(screen)

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

def initialize(window):
    MY.player.location = (window.x / 2, window.y / 4)
    MY.boss.location = window / 2
    pygame.time.set_timer(MY.boss_attack_event, 20)
    count = 0
    while count < 20:
        MY.projectiles.append(Object(PROJECTILE_IMAGE))
        MY.projectile_owner.append(BOSS)
        count += 1

def draw(screen):
    MY.player.draw(screen)
    if MY.player_hitbox.active:
        MY.player_hitbox.draw(screen)

    for i in range(len(MY.projectiles)):
        if MY.projectiles[i].active:
            MY.projectiles[i].draw(screen)

    MY.boss.draw(screen)
    MY.player_text.draw(screen)
    health_bar(screen, MY.player_health, 100, (100, 20), (85, 3))
    health_bar(screen, MY.boss_health, 300, (MY.boss.width(), 20), MY.boss.location - (MY.boss.width() / 2, (MY.boss.height() / 2) + 25))

def cleanup():
    """Cleans up the Intro State."""
    MY.projectiles = []

def player_attack_anim():
    if MY.player_dir == UP:
        MY.player.sprite = MY.attack_backward
    elif MY.player_dir == DOWN:
        MY.player.sprite = MY.attack_forward
    elif MY.player_dir == LEFT:
        MY.player.sprite = MY.attack_left
    elif MY.player_dir == RIGHT:
        MY.player.sprite = MY.attack_right

def player_pain_anim():
    if MY.player_dir == UP:
        MY.player.sprite = MY.pain_backward
    elif MY.player_dir == DOWN:
        MY.player.sprite = MY.pain_forward
    elif MY.player_dir == LEFT:
        MY.player.sprite = MY.pain_left
    elif MY.player_dir == RIGHT:
        MY.player.sprite = MY.pain_right

def player_attack_update():
    if key_held_down(pygame.K_SPACE):
        MY.player_hitbox.active = True
        player_attack_anim()

def player_move_update(delta_time):
    moving = (key_held_down(pygame.K_RIGHT) or key_held_down(pygame.K_LEFT) or
              key_held_down(pygame.K_DOWN) or key_held_down(pygame.K_UP))
    
    if not moving and not key_held_down(pygame.K_SPACE) and not MY.player.collides_with(MY.boss):
        MY.player_hitbox.active = False
        if MY.player_dir == UP:
            MY.player.sprite = MY.idle_backward
        elif MY.player_dir == DOWN:
            MY.player.sprite = MY.idle_forward
        elif MY.player_dir == LEFT:
            MY.player.sprite = MY.idle_left
        elif MY.player_dir == RIGHT:
            MY.player.sprite = MY.idle_right

    if key_held_down(pygame.K_UP):
        MY.player_hitbox.active = False
        MY.player.location.y -= 200 * delta_time
        MY.player_dir = UP
        MY.player.sprite = MY.walk_backward
    elif key_held_down(pygame.K_DOWN):
        MY.player_hitbox.active = False
        MY.player.location.y += 200 * delta_time
        MY.player_dir = DOWN
        MY.player.sprite = MY.walk_forward
    if key_held_down(pygame.K_LEFT):
        MY.player_hitbox.active = False
        MY.player.location.x -= 200 * delta_time
        MY.player_dir = LEFT
        MY.player.sprite = MY.walk_left
    elif key_held_down(pygame.K_RIGHT):
        MY.player_hitbox.active = False
        MY.player.location.x += 200 * delta_time
        MY.player_dir = RIGHT
        MY.player.sprite = MY.walk_right

def update_player(delta_time):
    """Updates the position of the players in the game window."""
    player_move_update(delta_time)
    player_attack_update()
    MY.player.update(delta_time)

def fire_projectile(player_number, degrees, speed):
    count = -1
    for projectile in MY.projectiles:
        count += 1
        if projectile.active:
            if MY.projectile_owner[count] == BOSS and projectile.collides_with(MY.player):
                MY.player_health -= 1
                projectile.active = False
                continue
            for wall in MY.walls:
                if projectile.collides_with(wall):
                    projectile.active = False
                    continue

def boss_explosion_update():
    """shoot out lots of projectiles."""
    num_projectiles = 15
    fraction = 360 / num_projectiles
    count = 0
    while count < num_projectiles:
        fire_projectile(BOSS, fraction * count, 15)
        count += 1

def boss_rotation_update(delta_time):
    """laser attack."""
    MY.boss.add_rotation(MY.rotation_speed * delta_time)
    fire_projectile(BOSS, MY.boss.rotation, 30)
    if MY.boss.rotation >= 355:
        MY.boss.rotation = 0

def boss_attack():
    '''if rand.randint(0, 1) == 0:
        boss_explosion_update(delta_time)
    else:
        boss_rotation_update(delta_time)'''
    boss_explosion_update()

def update_boss(delta_time):
    if MY.player_hitbox.active and MY.boss.collides_with(MY.player_hitbox):
        MY.boss.sprite = MY.boss_pain
    elif MY.is_boss_attacking:
         MY.boss.sprite = MY.boss_attack
         boss_attack()
    else:
        MY.boss.sprite = MY.boss_idle
    MY.boss.update(delta_time)

def check_win():
    """Check win condition and change state if a player has won the game"""
    if MY.boss_health < 1:
        Manager.current = 1
        MY.state = 1
        MY.display_text = TextObject(WHITE, 24, "You win!")
        MY.ending_layover = MY.you_win
    elif MY.player_health < 1:
        Manager.current = 1
        MY.state = 2
        MY.display_text = TextObject(WHITE, 24, "You lose!")
        MY.ending_overlay = MY.game_over