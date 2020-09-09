"""
coda-kids is a partial wrapper package around pygame. It's purpose
is to make game development more accessible to a younger audiences
of students. It provides inline documentation, wrappers for linter
unfriendly features, and provides utility functionality/classes such
as game objects and constants for common colors.

It is currently being designed for and tested with a series of
game programming exercises for an educational book titled
Coda Kids.

The package was designed and implemented with and for the
following toolset:

Python 3.5.2 with lastest Pygame and Pylint
Visual Studio Code 1.11+ with the Python extension installed.
"""
import pygame

import framework.coda_kids.color
import framework.coda_kids.utilities
import framework.coda_kids.dir
import framework.coda_kids.event
import framework.coda_kids.state
import framework.coda_kids.actions

def start(window_size, game_name):
    """
    Initializes the library and returns a pygame screen. Call this first!

        SCREEN = coda.start((w, h), "Title");
    """
    pygame.init()
    framework.coda_kids.utilities.time.sleep(2)
    framework.coda_kids.utilities.random.seed(framework.coda_kids.utilities.time.time())
    pygame.display.set_caption(game_name)
    pygame.mixer.init()
    return pygame.display.set_mode((int(window_size[0]), int(window_size[1])))

def stop():
    """
    Stops pygame and closes the window immediately.

        coda.stop();
    """
    framework.coda_kids.utilities.sys.exit()

class Image:
    def __init__(self, image_file_name):
        if image_file_name is not None:
            self.data = pygame.image.load(image_file_name).convert_alpha()
        else:
            self.data = None

    def update(self, dt):
        return

    def surface(self):
        return self.data

def Sound(sound_file_name):
    """
    Loads and returns a sound file with the given file name.

        SOUND = coda.Image("Example.wav");
    """
    return pygame.mixer.Sound(sound_file_name)

def draw_rect(screen, color, top_left, size):
    """
    Draw's a rectangle with the given values. Doesn't return.

        coda.draw_rect(SCREEN, (r, g, b, a), (0, 0), (10, 10));
    """
    pygame.draw.rect(screen, color, (top_left[0], top_left[1], size[0], size[1]))

def Vector2(X_VALUE, Y_VALUE):
    """
    Creates a 2D coordinate with values x and y. Can also be used as a tuple.

        a = coda.Vector2(1, 1) # a = (1, 1);

        b = coda.vector2(2, 4) # b = (2, 4);

        c = coda.Vector2(a.x, b.y) # c = (a[0], b[1]);
    """
    return pygame.math.Vector2(X_VALUE, Y_VALUE)

def start_draw(screen, fill_color):
    """Begin drawing to the screen."""
    screen.fill(fill_color)

def end_draw():
    """End drawing to screen."""
    pygame.display.flip()

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

class SpriteSheet:
    """
    Sprite sheet class for managing sprite animations.

        sheet = coda.SpriteSheet("image.png", (16, 16));
    """

    def __init__(self, filename, frame_size):
        self.sheet = pygame.image.load(filename).convert_alpha()
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
        x = framework.coda_kids.utilities.math.floor(index % self.columns) * self.rectangle.width
        y = framework.coda_kids.utilities.math.floor(index / self.columns) * self.rectangle.height
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
        direction = Vector2(framework.coda_kids.utilities.math.cos(framework.coda_kids.utilities.math.radians(direction - 90)),
                            framework.coda_kids.utilities.math.sin(framework.coda_kids.utilities.math.radians(direction - 90)))
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
        self.velocity = Vector2(-1 * framework.coda_kids.utilities.math.cos(framework.coda_kids.utilities.math.radians(degrees - 90)) * speed,
                                framework.coda_kids.utilities.math.sin(framework.coda_kids.utilities.math.radians(degrees - 90)) * speed)

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
            self.collision[coda_kids.dir.DOWN] = self.collision[coda_kids.dir.UP] = False
            self.collision[coda_kids.dir.LEFT] = self.collision[coda_kids.dir.RIGHT] = False
            return False

        #get transformed rectangles
        rect1 = self.get_transformed_rect()
        rect2 = other_obj.get_transformed_rect()

        if not rect1.colliderect(rect2):
            return False

        self.collision[coda_kids.dir.DOWN] = rect2.collidepoint((rect1.center[0] - rect1.width / 4, rect1.center[1] + rect1.height / 2)) or rect2.collidepoint((rect1.center[0] + rect1.width / 4, rect1.center[1] + rect1.height / 2))
        self.collision[coda_kids.dir.UP] = rect2.collidepoint((rect1.center[0] - rect1.width / 4, rect1.center[1] - rect1.height / 2)) or rect2.collidepoint((rect1.center[0] + rect1.width / 4, rect1.center[1] - rect1.height / 2))
        self.collision[coda_kids.dir.LEFT] = rect2.collidepoint((rect1.center[0] - rect1.width / 2, rect1.center[1] + rect1.height / 4)) or rect2.collidepoint((rect1.center[0] - rect1.width / 2, rect1.center[1] - rect1.height / 4))
        self.collision[coda_kids.dir.RIGHT] = rect2.collidepoint((rect1.center[0] + rect1.width / 2, rect1.center[1] + rect1.height / 4)) or rect2.collidepoint((rect1.center[0] + rect1.width / 2, rect1.center[1] - rect1.height / 4))

        return True

    def snap_to_object_x(self, other_obj, facing):
        """
        Snaps the object to the left or right of the other object given.

            # Snap obj1 left of obj2
            obj1.snap_to_object_x(obj2, coda.dir.LEFT);
        """
        if facing == framework.coda_kids.dir.LEFT:
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
        if facing == framework.coda_kids.dir.UP:
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

class TextObject:
    """
    Create an object that renders text. Assumes that the default font 
    freesansbold exists in the project directory as a true type font.

        #create a text object
        title = TextObject(coda.color.RED, 12, "example");
    """

    def __init__(self, color_value, font_size, text):
        self.location = Vector2(0, 0)
        self.color = color_value
        self.font_size = font_size
        self.text = text
        self.centered = False

    def __setattr__(self, name, value):
        if name == "location":
            self.__dict__[name] = Vector2(value[0], value[1])
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
        loc = Vector2(self.location.x, self.location.y)
        if self.centered is True:
            loc.x -= obj.get_rect().width / 2
        screen.blit(obj, loc)

class FiniteState:
    """Simple state. Used by state machine. TO BE REPLACED."""
    def __init__(self, owner, init_function, update_function):
        self.owner = owner
        self.initialize = init_function
        self.update = update_function

class StateMachine:
    """Simple variable finite state machine. TO BE REPLACED."""
    def __init__(self):
        """Initialize the state machine."""
        self.current_state = 0
        self.previous_state = -1
        self.states = []

    def add_state(self, init_function, update_function):
        """append a state to the state machine."""
        self.states.append(FiniteState(self, init_function, update_function))

    def update(self, delta_time):
        """update the the state at index current_state of states."""
        if self.current_state != self.previous_state:
            if self.states[self.current_state].initialize != None:
                self.states[self.current_state].initialize(self.states[self.current_state], delta_time)
            self.previous_state = self.current_state

        self.states[self.current_state].update(self.states[self.current_state], delta_time)


"""
To do notes:

1. Because of rotation set attribute, rotation might be unnecessary.
2. Set and add velocity methods do not follow convention
3. create animation system
4. get rid of finite state machine. please. its so bad.
5. Add animation system for sprite sheets.
"""