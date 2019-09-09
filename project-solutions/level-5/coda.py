import math
from os import path
import pygame
import random
import time

BLUE = [0, 192, 255, 128]
GREEN = [0, 128, 0, 128]
RED = [255, 0, 0]
YELLOW = [255, 255, 0]

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

_data = {}

def listing():
    """
    Returns a list of all events currently in the event system.

        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop();
    """
    return pygame.event.get()

def quit_game(event):
    """
    Checks for quit game event.

        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop();
    """
    return event.type == pygame.QUIT

def mouse_l_button_up(event):
    """
    Checks if the left mouse button was released.

        for event in coda.event.listing():
            if coda.event.mouse_l_button_up(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONUP and event.button == 1

def mouse_l_button_down(event):
    """
    Checks if the left mouse button was clicked.

        for event in coda.event.listing():
            if coda.event.mouse_l_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def mouse_m_button_up(event):
    """
    Checks if the middle mouse button was released.

        for event in coda.event.listing():
            if coda.event.mouse_m_button_up(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONUP and event.button == 2

def mouse_m_button_down(event):
    """
    Checks if the middle mouse button was clicked.

        for event in coda.event.listing():
            if coda.event.mouse_m_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 2

def mouse_r_button_up(event):
    """
    Checks if the right mouse button was released.

        for event in coda.event.listing():
            if coda.event.mouse_r_button_up(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONUP and event.button == 3

def mouse_r_button_down(event):
    """
    Checks if the right mouse button was clicked.

        for event in coda.event.listing():
            if coda.event.mouse_r_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 3

def mouse_down(event, button):
    """
    Checks if the left/right mouse button is being held down.

        for event in coda.event.listing():
            if coda.event.mouse_down(coda.dir.LEFT):
                do_things();
    """
    return pygame.mouse.get_pressed()[button]

def mouse_position():
    """
    Returns the position of the mouse as a tuple.

        data = coda.event.mouse_position();
    """
    pos = pygame.mouse.get_pos()
    return Vector2(pos[0], pos[1])

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

def key_up(event, key):
    """
    Checks if the keyboard key is released.

        for ev in coda.event.listing():
            # Space key released.
            if coda.event.key_up(ev, " "):
                do_things();
    """
    if isinstance(key, str):
        return event.type == pygame.KEYUP and event.key == ord(key)
    return event.type == pygame.KEYUP and event.key == key

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

def listing():
    """
    Returns a list of all events currently in the event system.

        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop();
    """
    return pygame.event.get()

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

def Vector2(x_value, y_value):
    """
    Creates a 2D coordinate with values x and y. Can also be used as a tuple.

        a = coda.Vector2(1, 1) # a = (1, 1);

        b = coda.vector2(2, 4) # b = (2, 4);

        c = coda.Vector2(a.x, b.y) # c = (a[0], b[1]);
    """
    return pygame.math.Vector2(x_value, y_value)

def draw_rect(screen, color, top_left, size):
    """
    Draw's a rectangle with the given values. Doesn't return.

        coda.draw_rect(SCREEN, (r, g, b, a), (0, 0), (10, 10));
    """
    pygame.draw.rect(screen, color, (top_left[0], top_left[1], size[0], size[1]))

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

class Object:
    """
    Object class used to organize and track common game object data, such as location and appearance.

        obj = coda.Object(IMAGE);
    """
    location = Vector2(0, 0)
    scale = 1
    velocity = Vector2(0, 0)

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
        direction = Vector2(math.cos(math.radians(direction - 90)),
                            math.sin(math.radians(direction - 90)))
        if direction.x < epsilon and direction.x > 0:
            direction.x = 0

        if direction.y < epsilon and direction.y > 0:
            direction.y = 0

        vel = Vector2(-1 * direction.x * speed, direction.y * speed)

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
        self.velocity = Vector2(-1 * math.cos(math.radians(degrees - 90)) * speed,
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
    coda_kids.utilities.sys.exit()

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

Manager = Machine()

def change(new_state):
    """Requests a change in game state."""
    Manager.current = new_state