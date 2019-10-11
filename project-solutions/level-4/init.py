import pygame
from types import ModuleType
import sys
import math
import time
import random
from os import path

#Global color values
WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
GREEN = [0, 128, 0, 128]
BLUE = [0, 192, 255, 128]

#Global direction variables
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

# data used to store all lerps
_data = {}

#coda_kids framework
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
            self.states[self.current]['draw'](screen)
            pygame.display.flip()

def start(window_size, game_name):
    """
    Initializes the library and returns a pygame screen. Call this first!

        SCREEN = start((w, h), "Title");
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

        stop();
    """
    sys.exit()

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs your files from your folder.
    return path.join(path.dirname(__file__), fileName)

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

def Sound(sound_file_name):
    """
    Loads and returns a sound file with the given file name.

        SOUND = Sound("Example.wav");
    """
    return pygame.mixer.Sound(get_file(sound_file_name))

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

class Animator:
    """Animator class for animation functions"""
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

def draw_rect(screen, color, top_left, size):
    """
    Draw's a rectangle with the given values. Doesn't return.

        coda.draw_rect(SCREEN, (r, g, b, a), (0, 0), (10, 10));
    """
    pygame.draw.rect(screen, color, (top_left[0], top_left[1], size[0], size[1]))

def rand(minimum, maximum):
    """Generates a random whole number."""
    return random.randint(minimum, maximum)

def rand_location(minimum, maximum):
    """Generates a random location from the given min and max."""
    return pygame.math.Vector2(rand(minimum, maximum), rand(minimum, maximum))

def quit_game(event):
    """
    Checks for quit game event.

        for event in event.listing():
            if event.quit_game(event):
                stop();
    """
    return event.type == pygame.QUIT


def mouse_l_button_down(event):
    """
    Checks if the left mouse button was clicked.

        for event in event.listing():
            if event.mouse_l_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def mouse_position():
    """
    Returns the position of the mouse as a tuple.

        data = event.mouse_position();
    """
    pos = pygame.mouse.get_pos()
    return pygame.math.Vector2(pos[0], pos[1])

"""Setup for the SpaceWars game"""
#initialize state manager
Manager = Machine()

#initialize the game window and game screen
WINDOW = pygame.math.Vector2(900, 500)
SCREEN = start(WINDOW, "Space Wars Tournament")

#load sprites, sounds, and images
IMAGE_BACKGROUND = Image("assets/Background.jpg")
IMAGE_PLAYER1 = Image("assets/Player1.png")
IMAGE_PLAYER2 = Image("assets/Player2.png")
IMAGE_ASTEROID = Image("assets/AsteroidLarge.png")
IMAGE_ASTEROID_2 = Image("assets/AsteroidSmall.png")

sound_explosions = [Sound("assets/Explosion1.wav"),
                    Sound("assets/Explosion2.wav")]
sound_laser = [Sound("assets/LaserShoot1.wav"),
               Sound("assets/LaserShoot2.wav")]

SPRITESHEET_PROJECTILE = [None,
                          SpriteSheet("assets/Player1Projectile.png", (36, 24)),
                          SpriteSheet("assets/Player2Projectile.png", (48, 48))]
PROJECTILE_ANIMATION = [None,
                        Animator(SPRITESHEET_PROJECTILE[1], 0.4),
                        Animator(SPRITESHEET_PROJECTILE[2], 0.4)]
IMAGE_GAMEOVER = Image("assets/GameOverBackground.png")
IMAGE_BUTTON = Image("assets/ReplayButton.png")

# constants for movement and gameplay
ship_rotate = 120
ship_max_speed = 500
ship_accel = 10
BULLET_SPEED = 1000
PLAYER_MAX_HP = 10

#Load the changeable data for gameplay
class Data:
    player1 = Object(IMAGE_PLAYER1)
    player1_hp = 1
    player2 = Object(IMAGE_PLAYER2)
    player2_hp = 1
    bullets = []
    asteroids = []
    bullet_owner = []
    maxFrameTime = 0.05
    window = pygame.math.Vector2(10, 10)
    background = Object(IMAGE_BACKGROUND)
    gameoverbackground = Object(IMAGE_GAMEOVER)
    restart_button = Object(IMAGE_BUTTON)
    display_text = TextObject(WHITE, 24, "")
    state = 0

#Initialize the data
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

def screen_wrap(obj, window):
    """Wraps a given framework object around the screen, returns true if object is at edge."""
    flag = False

    # Wrap X direction
    if obj.location.x > window.x:
        obj.location.x = 0
        flag = True
    elif obj.location.x < 0:
        obj.location.x = window.x
        flag = True

    # Wrap Y direction
    if obj.location.y > window.y:
        obj.location.y = 0
        flag = True
    elif obj.location.y < 0:
        obj.location.y = window.y
        flag = True

    return flag

def initialize(window):
    """Initializes the shooter class."""
    MY.player1.location = window / 4
    MY.player1.rotation = 90
    MY.player1.set_velocity(MY.player1.rotation, 0)
    MY.player1_hp = PLAYER_MAX_HP
    MY.player2.location = window - window / 4
    MY.player2.rotation = -90
    MY.player2.set_velocity(MY.player2.rotation, 0)
    MY.player2_hp = PLAYER_MAX_HP
    count = 0
    MY.window = window
    MY.background.location = window / 2
    if MY.state!=0:
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2
        MY.display_text = TextObject(WHITE, 24, "")
    while count < 20:
        MY.bullets.append(Object(PROJECTILE_ANIMATION[1]))
        MY.bullet_owner.append(1)
        count = count + 1

    count = 0
    while count < 5:
        if (rand(0, 1) == 0):
            image = IMAGE_ASTEROID
        else:
            image = IMAGE_ASTEROID_2
        obj = Object(image)
        obj.location = rand_location(0, MY.window.x)
        obj.velocity = rand_location(-50, 50)
        obj.scale = 2
        obj.active = True
        MY.asteroids.append(obj)
        count = count + 1

def fire_bullet(player_number):
    """fire a bullet for the player"""
    index = -1
    for i in range(len(MY.bullets)):
        if not MY.bullets[i].active:
            index = i
            break
    if index >= 0:
        MY.bullets[index].active = True
        if player_number == 1:
            MY.bullets[index].location = MY.player1.location
            MY.bullets[index].set_velocity(MY.player1.rotation, BULLET_SPEED)
            MY.bullets[index].rotation = MY.player1.rotation
        else:
            MY.bullets[index].location = MY.player2.location
            MY.bullets[index].set_velocity(MY.player2.rotation, BULLET_SPEED)
            MY.bullets[index].rotation = MY.player2.rotation

        MY.bullet_owner[index] = player_number
        MY.bullets[index].sprite = PROJECTILE_ANIMATION[player_number]

def draw(screen):
    """Draws the state to the given screen for SpaceWars."""
    MY.background.draw(screen)
    MY.player1.draw(screen)
    MY.player2.draw(screen)
    rect = MY.player1.sprite.surface().get_rect()
    rect.center = MY.player1.location
    health_bar(screen, MY.player1_hp,
                PLAYER_MAX_HP, pygame.math.Vector2(rect.width, 10), rect.topleft)
    rect = MY.player2.sprite.surface().get_rect()
    rect.center = MY.player2.location
    health_bar(screen, MY.player2_hp,
                PLAYER_MAX_HP, pygame.math.Vector2(rect.width, 10), rect.topleft)
    
    for i in range(len(MY.bullets)):
        if MY.bullets[i].active:
            MY.bullets[i].draw(screen)

    for i in range(len(MY.asteroids)):
        if MY.asteroids[i].active:
            MY.asteroids[i].draw(screen)

def cleanup():
    """Cleans up the Intro State for SpaceWars."""
    MY.bullets = []
    MY.asteroids = []

class restarter_player1:
    """Restarter class to be loaded if Player 1 wins."""
    # load sprites
    IMAGE_GAMEOVER = Image("assets/GameOverBackground.png")
    IMAGE_BUTTON = Image("assets/ReplayButton.png")

    # modifiable data
    class Data:
        """place changable state variables here."""
        gameoverbackground = Object(IMAGE_GAMEOVER)
        restart_button = Object(IMAGE_BUTTON)
        display_text = TextObject(WHITE, 24, "Player 1 wins! Play again?")

    MY = Data()

    def initialize(window):
        """Initializes the restart menu state."""
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2

    def update(delta_time):
        """Updates the restart menu state."""
        for event in pygame.event.get():
            if quit_game(event):
                stop()
            if mouse_l_button_down(event):
                if MY.restart_button.collides_with_point(mouse_position()):
                    Manager.current = 0

    def draw(screen):
        """Draws the restart menu state."""
        MY.gameoverbackground.draw(screen)
        MY.restart_button.draw(screen)
        MY.display_text.draw(screen)

    def cleanup():
        """Cleans up the restart menu state."""

class restarter_player2:
    """Restarter class to be loaded if Player 2 wins."""    
    # load sprites
    IMAGE_GAMEOVER = Image("assets/GameOverBackground.png")
    IMAGE_BUTTON = Image("assets/ReplayButton.png")

    # modifiable data
    class Data:
        """place changable state variables here."""
        gameoverbackground = Object(IMAGE_GAMEOVER)
        restart_button = Object(IMAGE_BUTTON)
        display_text = TextObject(WHITE, 24, "Player 2 wins! Play again?")

    MY = Data()

    def initialize(window):
        """Initializes the restart menu state."""
        MY.gameoverbackground.location = window / 2
        MY.restart_button.location = window / 2

    def update(delta_time):
        """Updates the restart menu state."""
        for event in pygame.event.get():
            if quit_game(event):
                stop()
            if mouse_l_button_down(event):
                if MY.restart_button.collides_with_point(mouse_position()):
                    Manager.current = 0

    def draw(screen):
        """Draws the restart menu state."""
        MY.gameoverbackground.draw(screen)
        MY.restart_button.draw(screen)
        MY.display_text.draw(screen)

    def cleanup():
        """Cleans up the restart menu state."""