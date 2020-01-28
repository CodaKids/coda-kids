#============================================================
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
            return True
        return False

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
window_length = 608
WINDOW = pygame.math.Vector2(800, 608)
SCREEN = start(WINDOW, "Boss Battle")

#load sprites constants
BOSS_IMAGE = Image("assets/boss.png")
PROJECTILE_IMAGE = Image("assets/projectile.png")
BACKGROUND_IMAGE = Image("assets/Background.png")

#constants
PLAYER = 0
BOSS = 1
GRASS = 4
TILE_SIZE = 32

class Data:
    """Modifiable data"""
    player_walk_forward_sheet = SpriteSheet("assets/paul_front_run_12fps.png", (64, 64))
    player_walk_backward_sheet = SpriteSheet("assets/paul_back_run_12fps.png", (64, 64))
    player_walk_left_sheet = SpriteSheet("assets/paul_side_run_left_12fps.png", (64, 64))
    player_walk_right_sheet = SpriteSheet("assets/paul_side_run_right_12fps.png", (64, 64))
    player_attack_forward_sheet = SpriteSheet("assets/paul_front_attack_12fps.png", (100, 100))
    player_attack_backward_sheet = SpriteSheet("assets/paul_back_attack_12fps.png", (100, 100))
    player_attack_left_sheet = SpriteSheet("assets/paul_side_attack_left_12fps.png", (128, 64))
    player_attack_right_sheet = SpriteSheet("assets/paul_side_attack_right_12fps.png", (128, 64))
    walk_forward = Animator(player_walk_forward_sheet, 1)
    attack_forward = Animator(player_attack_forward_sheet, 0.5)
    walk_backward = Animator(player_walk_backward_sheet, 1)
    attack_backward = Animator(player_attack_backward_sheet, 0.5)
    walk_left = Animator(player_walk_left_sheet, 1)
    attack_left = Animator(player_attack_left_sheet, 0.5)
    walk_right = Animator(player_walk_right_sheet, 1)
    attack_right = Animator(player_attack_right_sheet, 0.5)
    player = Object(player_walk_forward_sheet.image_at(2))
    player_start_position = pygame.math.Vector2(0, 0)
    player_health = 100
    player_dir = DOWN
    player_text = TextObject(BLACK, 24, "Player: ")
    player_hitbox = Object(PROJECTILE_IMAGE)
    wall_height = 45
    boss_start_position = pygame.math.Vector2(0, 0)
    boss = Object(BOSS_IMAGE)
    boss_health = 300
    timer1 = CountdownTimer(0.1)
    timer3 = CountdownTimer(0.1)
    numberOfBullets = 0
    bullets = []
    bullet_owner = []
    rotation_speed = 180
    state = 0
    last_state = 2
    index = 0

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

def fire_bullet(player_number, degrees, speed):
    """fire a bullet for the player"""
    index = -1
    for i in range(len(MY.bullets)):
        if not MY.bullets[i].active:
            index = i
            break
    if index >= 0:
        MY.bullets[index].active = True
        if player_number == 1:
            MY.bullets[index].location = MY.boss.location
            MY.bullets[index].set_velocity(degrees, speed)
        else:
            MY.bullets[index].location = MY.player.location
            MY.bullets[index].set_velocity(degrees, speed)
        MY.bullet_owner[index] = player_number

def boss_wait_init(state, delta_time):
    state.timer = CountdownTimer(3)
    state.previous = state.owner.previous_state

def boss_wait_update(state, delta_time):
    """wait between attacks."""
    if state.timer.tick(delta_time):
        if state.previous == 0:
            state.owner.current_state = 1
        else:
            state.owner.current_state = 0

def boss_explosion_update(state, delta_time):
    """shoot out lots of projectiles."""
    num_projectiles = 15
    fraction = 360 / num_projectiles
    count = 0
    while count < num_projectiles:
        fire_bullet(BOSS, fraction * count, 15)
        count += 1

    state.owner.current_state = 2

def boss_laser_update(state, delta_time):
    """laser attack."""
    MY.boss.add_rotation(MY.rotation_speed * delta_time)
    fire_bullet(BOSS, MY.boss.rotation, 30)
    if MY.boss.rotation >= 355:
        MY.boss.rotation = 0
        state.owner.current_state = 2

def player_attack(delta_time):
    if MY.player_dir == UP:
        MY.player.sprite = MY.attack_backward
    elif MY.player_dir == DOWN:
        MY.player.sprite = MY.attack_forward
    elif MY.player_dir == LEFT:
        MY.player.sprite = MY.attack_left
    elif MY.player_dir == RIGHT:
        MY.player.sprite = MY.attack_right

def player_move_update(delta_time):
    moving = (key_held_down(pygame.K_RIGHT) or key_held_down(pygame.K_LEFT) or
              key_held_down(pygame.K_DOWN) or key_held_down(pygame.K_UP))
    
    if not moving and not key_held_down(pygame.K_SPACE):
        if MY.player_dir == UP:
            MY.player.sprite = MY.player_walk_backward_sheet.image_at(2)
        elif MY.player_dir == DOWN:
            MY.player.sprite = MY.player_walk_forward_sheet.image_at(2)
        elif MY.player_dir == LEFT:
            MY.player.sprite = MY.player_walk_left_sheet.image_at(2)
        elif MY.player_dir == RIGHT:
            MY.player.sprite = MY.player_walk_right_sheet.image_at(2)

    if key_held_down(pygame.K_UP):
        MY.player.location.y -= 200 * delta_time
        MY.player_dir = UP
        MY.player.sprite = MY.walk_backward
    elif key_held_down(pygame.K_DOWN):
        MY.player.location.y += 200 * delta_time
        MY.player_dir = DOWN
        MY.player.sprite = MY.walk_forward
    if key_held_down(pygame.K_LEFT):
        MY.player.location.x -= 200 * delta_time
        MY.player_dir = LEFT
        MY.player.sprite = MY.walk_left
    elif key_held_down(pygame.K_RIGHT):
        MY.player.location.x += 200 * delta_time
        MY.player_dir = RIGHT
        MY.player.sprite = MY.walk_right

def initialize(window):
    MY.player.location = (window.x / 2, window.y / 4)
    MY.boss.location = window / 2
    count = 0
    while count < 100:
        MY.bullets.append(Object(PROJECTILE_IMAGE))
        MY.bullet_owner.append(BOSS)
        count += 1

def draw(screen):
    """Draws the state to the given screen."""
    for bullet in MY.bullets:
        if  bullet.active:
            bullet.draw(screen)

    MY.player.draw(screen)
    if MY.player_hitbox.active:
        MY.player_hitbox.draw(screen)

    MY.boss.draw(screen)
    MY.player_text.draw(screen)
    health_bar(screen, MY.player_health, 100, (100, 20), (85, 3))
    health_bar(screen, MY.boss_health, 300, (MY.boss.width(), 20), MY.boss.location - (MY.boss.width() / 2, (MY.boss.height() / 2) + 25))

def update_player(delta_time):
    """Updates the position of the players in the game window."""
    player_move_update(delta_time)
    MY.player.update(delta_time)

def check_win():
    """Check win condition and change state if a player has won the game"""
    if MY.boss_health < 1:
        Manager.current = 1
        MY.state = 1
        MY.display_text = TextObject(WHITE, 24, "You win!")
        
    elif MY.player_health < 1:
        Manager.current = 1
        MY.state = 1
        MY.display_text = TextObject(WHITE, 24, "You lose!")

def cleanup():
    """Cleans up the Intro State."""

class GameOver:
    """Restarter class to be loaded if Player 1 wins."""
    # load sprites
    # IMAGE_GAMEOVER = Image("assets/GameOverBackground.png")
    # IMAGE_BUTTON = Image("assets/ReplayButton.png")

    # modifiable data
    class Data:
        """place changable state variables here."""
        # gameoverbackground = Object(IMAGE_GAMEOVER)
        # restart_button = Object(IMAGE_BUTTON)
        display_text = TextObject(WHITE, 24, "Player 1 wins! Play again?")

    MY = Data()

    def initialize(self, window):
        """Initializes the restart menu state."""
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2

    def update(self, delta_time):
        """Updates the restart menu state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if MY.restart_button.collides_with_point(pygame.mouse.get_pos()):
                    Manager.current = 0

    def cleanup(self):
        """Cleans up the restart menu state."""

    def draw(self, screen):
        """Draws the restart menu state."""
        # MY.gameoverbackground.draw(screen)
        # MY.restart_button.draw(screen)
        MY.display_text.draw(screen)