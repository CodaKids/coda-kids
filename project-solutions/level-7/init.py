#============================================================
#PART 1: IMPORTING DEPENDENCIES AND ASSIGNING GLOBAL VARIABLES
import pygame
import random
import math
import sys
import time
from os import path
import textwrap

# colors
WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
GREEN = [0, 128, 0, 128]
BLUE = [0, 192, 255, 128]

_data = {}

#============================================================
#PART 2: CREATING A FRAMEWORK OF GENERAL CLASSES AND FUNCTIONS
def start(window_size, game_name):
    """ Initializes the library and returns a pygame screen.  """
    pygame.init()
    pygame.display.set_caption(game_name)
    pygame.mixer.init()
    return pygame.display.set_mode((int(window_size[0]), int(window_size[1])))

def stop():
    """ Stops pygame and closes the window immediately. """
    pygame.quit()
    sys.exit()

def check_stop(event):
    # Checks if you closed the window
    if event.type == pygame.QUIT:
        stop()

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

# class Machine:
    # """Game state machine class."""
    # def __init__(self):
    #     self.current = 0
    #     self.previous = 0
    #     self.states = []

    # def register(self, module):
    #     """Registers the state's init, update, draw, and cleanup functions."""
    #     self.states.append({'initialize': module.initialize,
    #                         'update': module.update,
    #                         'draw': module.draw,
    #                         'cleanup': module.cleanup})

    # def run(self, screen, window, fill_color):
    #     """Runs the state given machine."""
    #     clock = pygame.time.Clock()
        # first run initialize!
        # self.states[self.current]['initialize'](window)

        # print("before run() loop")
        # while True:
        #     print("run loop inf")
        #     delta_time = clock.tick(60) / 1000
        #     if self.current != self.previous:
        #         self.states[self.current]['cleanup']()
        #         self.states[self.current]['initialize'](window)
        #         self.previous = self.current
        #     update(delta_time)
        #     self.states[self.current]['update'](delta_time)
        #     screen.fill(fill_color)
        #     self.states[self.current]['draw'](screen)
        #     pygame.display.flip()

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs the image files from your folder.
    return path.join(path.dirname(__file__), fileName)

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
        obj = Object(IMAGE);
    """
    location = pygame.math.Vector2(0, 0)
    scale = 1

    def __init__(self, image):
        self.sprite = image
        self.rotation = 0
        self.active = False

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
#============================================================
#PART 3: SETUP FOR THE BATTLE CARDS GAME
# Manager = Machine()

#constants for screen
WINDOW_WIDTH = 800
WINDOW_LENGTH = 600
WINDOW = pygame.math.Vector2(WINDOW_WIDTH, WINDOW_LENGTH)
SCREEN = start(WINDOW, "IncrediCards")
BACKGROUND_IMAGE = pygame.image.load("project-solutions/level-7/Assets/Table.png") 
CARD_L_POS = pygame.math.Vector2(150,275)
CARD_R_POS = pygame.math.Vector2(650,275)
coin_font = pygame.font.SysFont('Arial', 35)
dialog_font = pygame.font.Font('freesansbold.ttf', 14)
cardshand_font = pygame.font.SysFont('Arial', 16)

clock = pygame.time.Clock()

class Data:
    # coin = Object(Image("Assets/CoinFlip.png")) - will need to be spritesheet object
    # card1 = Object(Image("Assets/AnnieConda.png"))
    CARDIMG = Image('Assets/AnnieConda_300.png')
    CARD2IMG = Image('Assets/BayoWolf_300.png')
    insignia = pygame.image.load(get_file('Assets/TypePython.png'))

    CARD_R = Object(CARDIMG)
    CARD_R.__setattr__("location", CARD_L_POS)
    CARD_R.__setattr__("sprite", CARDIMG)
    CARD_L = Object(CARD2IMG)
    CARD_L.__setattr__("location", CARD_R_POS)
    CARD_L.__setattr__("sprite", CARD2IMG)

MY = Data()


def initialize(WINDOW):
    MY.coin.location = WINDOW / 2
    MY.card1.location = WINDOW / 4

def draw_screen(message="", p1_hp=15, p2_hp=15):
    SCREEN.fill(BLUE)
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    draw_dialog_box()
    populate_dialog_box(message)
    draw_active_cards()
    draw_inactive_cards()
    draw_healthbars(p1_hp, p2_hp)
    draw_coin_flip_button()
    pygame.display.update()

def cleanup():
    print("clean up")   

# draw screen - composed of:
# draw dialog box
def draw_dialog_box():
    dialog_surface = pygame.Surface((200,350))
    dialog_surface.set_alpha(100)
    dialog_surface.fill(WHITE)
    SCREEN.blit(dialog_surface, (300, 100))

def populate_dialog_box(message):
    if message == "":
        return
    lines = message.splitlines()
    x = 310
    y = 145
    for line in lines:
        dlg_pos = (x,y)
        dlg_line = dialog_font.render(line, True, (BLACK))
        SCREEN.blit(dlg_line, dlg_pos)
        y = y + 25

# draw active cards and health bars
def draw_active_cards():
    MY.CARD_R.draw(SCREEN)
    MY.CARD_L.draw(SCREEN)

# draw inactive cards
def draw_inactive_cards():
    SCREEN.blit(MY.insignia, (35,475))
    cards_in_hand = cardshand_font.render("Paul Python", True, BLACK)
    SCREEN.blit(cards_in_hand, (60, 475))

def draw_healthbars(p1_hp, p2_hp):
    p1_hp_pos = (25,50)
    p2_hp_pos = (525,50)
    width, height = 250, 25
    hb_size = (width, height)
    red = (215,65,55)
    green = (80,150,65)
    p1_bar = width * p1_hp / 15
    p2_bar = width * p2_hp / 15
    pygame.draw.rect(SCREEN, red, (p1_hp_pos, (width,height)))
    pygame.draw.rect(SCREEN, red, (p2_hp_pos, (width,height)))
    pygame.draw.rect(SCREEN, green, (p1_hp_pos, (p1_bar,height)))
    pygame.draw.rect(SCREEN, green, (p2_hp_pos, (p2_bar,height)))

# draw coin flip
def draw_coin_flip_button():
    coin_click = coin_font.render("flip the coin.", True, BLACK)
    SCREEN.blit(coin_click, (300,500))
    

def coin_flip_click():
    coin_click = coin_font.render("flip the coin.", True, BLACK)
    coin_click_rect = coin_click.get_rect(topleft=(300,500))
    return coin_click_rect