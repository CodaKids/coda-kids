"""This module provides a framework that can be used to create games."""
import time
import math
import random
import pygame

# Colors
WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
GREEN = [0, 128, 0, 128]
BLUE = [0, 192, 255, 128]

# Directions
BOTTOM = 0
TOP = 1
LEFT = 2
RIGHT = 3

# State variables
CURRENT_STATE = 0
PREVIOUS_STATE = 0
EPSILON = 1.0e-15

def init(window, name):
    """Initialize pygame and random seed."""
    pygame.init()
    random.seed(time.time())
    pygame.display.set_caption(name)
    return pygame.display.set_mode(window.as_sequence())

# create a random position from the given range of values
def random_position(minimum, maximum):
    """create a random position from the given range of values"""
    return (random.randint(minimum, maximum), random.randint(minimum, maximum))

class SIZE:
    """Size class used to keep track of a width and height."""
    width = 1.0
    height = 1.0
    def __init__(self, width_value, height_value):
        self.width = width_value
        self.height = height_value

    def as_sequence(self):
        """Returns the width and height as a truple."""
        return (self.width, self.height)

class OBJECT:
    """Object class used to track objects, their positions, and their image data."""
    sprite = 0
    location = pygame.math.Vector2(0, 0)
    scale = pygame.math.Vector2(1, 1)
    velocity = pygame.math.Vector2(0, 0)
    rotation = 0
    active = False
    collision = [False] * 4

    def __init__(self, image):
        self.location = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.sprite = image

    def get_transformed_rect(self):
        """returns a transformed version of the object sprite."""
        sprite = pygame.transform.rotate(self.sprite, self.rotation)
        rect = sprite.get_rect()
        rect.center = self.location + self.velocity
        return rect

    def width(self):
        """Gets the width of the object."""
        rect = self.get_transformed_rect()
        return rect.width

    def height(self):
        """Gets the height of the object."""
        rect = self.get_transformed_rect()
        return rect.height

    def move(self, x_value, y_value):
        """Move the object by the given coordinates"""
        self.location += pygame.math.Vector2(x_value, y_value)

    def set_position(self, x_value, y_value):
        """Teleport the object to the given values (x, y)"""
        self.location = pygame.math.Vector2(x_value, y_value)

    def add_rotation(self, degrees):
        """Add to the existing rotation of an object in degrees. Positive is clockwise."""
        self.rotation = self.rotation + degrees
        self.rotation = self.rotation - 360 * int(self.rotation /360)

    def set_rotation(self, degrees):
        """Set the rotation of the object to the given value in degrees. Positive is clockwise."""
        self.rotation = degrees - 360 * int(degrees / 360)

    def add_velocity(self, direction, speed, max_speed):
        """Add velocity to the object with the given direction and speed."""
        direction = pygame.math.Vector2(math.cos(math.radians(direction - 90)),
                                        math.sin(math.radians(direction - 90)))
        if direction.x < EPSILON and direction.x > 0:
            direction.x = 0

        if direction.y < EPSILON and direction.y > 0:
            direction.y = 0

        vel = pygame.math.Vector2(-1 * direction.x * speed, direction.y * speed)

        self.velocity += vel
        distance_sq = self.velocity.length()

        if distance_sq > max_speed:
            self.velocity.normalize_ip()
            self.velocity *= max_speed

    def set_velocity(self, direction, speed):
        """Set the velocity of the object to the given value given an angle and speed."""
        self.velocity.x = -1 * math.cos(math.radians(direction - 90)) * speed
        self.velocity.y = math.sin(math.radians(direction - 90)) * speed

    def collides_with(self, other_obj):
        """Check if this object collides with the given object."""
        # check for early rejection.
        dist = (self.location - other_obj.location).length_squared()
        # if distance between objects is greater then 64^2
        if dist > 4096:
            self.collision[BOTTOM] = self.collision[TOP] = False
            self.collision[LEFT] = self.collision[RIGHT] = False
            return False

        #get transformed rectangles
        rect1 = self.get_transformed_rect()
        rect2 = other_obj.get_transformed_rect()

        if not rect1.colliderect(rect2):
            return False

        self.collision[BOTTOM] = rect2.collidepoint((rect1.center[0] - rect1.width / 4, rect1.center[1] + rect1.height / 2)) or rect2.collidepoint((rect1.center[0] + rect1.width / 4, rect1.center[1] + rect1.height / 2))
        self.collision[TOP] = rect2.collidepoint((rect1.center[0] - rect1.width / 4, rect1.center[1] - rect1.height / 2)) or rect2.collidepoint((rect1.center[0] + rect1.width / 4, rect1.center[1] - rect1.height / 2))
        self.collision[LEFT] = rect2.collidepoint((rect1.center[0] - rect1.width / 2, rect1.center[1] + rect1.height / 4)) or rect2.collidepoint((rect1.center[0] - rect1.width / 2, rect1.center[1] - rect1.height / 4))
        self.collision[RIGHT] = rect2.collidepoint((rect1.center[0] + rect1.width / 2, rect1.center[1] + rect1.height / 4)) or rect2.collidepoint((rect1.center[0] + rect1.width / 2, rect1.center[1] - rect1.height / 4))

        return True

    def snap_to_object_x(self, other_obj, direction):
        """Snaps the object to the left or right of the other object given."""
        if direction == LEFT:
            self.location.x = (other_obj.location.x +
                               other_obj.width() / 2 +
                               self.width() / 2)
        else:
            self.location.x = (other_obj.location.x -
                               (other_obj.width() / 2 +
                                self.width() / 2))

    def snap_to_object_y(self, other_obj, direction):
        """Snaps the object to the left or right of the other object given."""
        if direction == TOP:
            self.location.y = (other_obj.location.y +
                               other_obj.height() / 2 +
                               self.height() / 2)
        else:
            self.location.y = (other_obj.location.y -
                               (other_obj.height() / 2 +
                                self.height() / 2))

    def collides_with_point(self, point):
        """Check if this object collides with the given point."""
        sprite = pygame.transform.rotate(self.sprite, self.rotation)
        rect = sprite.get_rect()
        location = self.location + self.velocity
        rect.center = location
        return rect.collidepoint(point)

    def draw(self, screen):
        """Updates and draws the object to the screen."""
        sprite = pygame.transform.rotate(self.sprite, self.rotation)
        rect = sprite.get_rect()
        self.location += self.velocity
        rect.center = self.location
        screen.blit(sprite, rect)

# Returns an array of all lines in a given file.
def read_file(filename):
    """Read a file line by line and return an array of strings."""
    # Create an empty array.
    array = []
    # Open our file for read.
    file = open(filename, 'r')

    # put all the lines in an array
    for line in file:
        array.append(line.rstrip())

    return array

def screen_wrap(obj, window):
    """Wraps a given framework object around the screen, returns true if object is at edge."""
    flag = False
    # Wrap X direction
    if obj.location.x > window.width:
        obj.location.x = 0
        flag = True
    elif obj.location.x < 0:
        obj.location.x = window.width
        flag = True

    # Wrap Y direction
    if obj.location.y > window.height:
        obj.location.y = 0
        flag = True
    elif obj.location.y < 0:
        obj.location.y = window.height
        flag = True

    return flag

def health_bar(screen, health, max_health, max_size, location):
    """Creates a health bar at the given position."""
    if health > max_health - max_health * 0.25:
        bar_color = GREEN
    elif health > max_health - max_health * 0.5:
        bar_color = YELLOW
    else:
        bar_color = RED

    width = max_size[0] * (health / max_health)
    pygame.draw.rect(screen, bar_color, (location[0], location[1], width, max_size[1]))