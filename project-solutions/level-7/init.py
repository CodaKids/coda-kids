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



class Card:
    def __init__(self, name, techtype, weakness, resistance, image_path):
        self.name = name
        self.techtype = techtype
        self.weakness = weakness
        self.resistance = resistance
        self.image_path = image_path
        self.HP = 15
        self.alive = True
    
    def check_alive(self):
        if self.HP <= 0:
            self.HP = 0
            self.alive = False

    def attack(self, offense_card):
        damage = 3 # default value

        # check strength/weakness and determine damage
        if offense_card.techtype == self.resistance:
            damage = damage - 1
        if offense_card.techtype == self.weakness:
            damage = damage + 1
        # take damage and return the damage amount
        self.take_damage(damage)
        return damage

    def take_damage(self, damage):
        self.HP = self.HP - damage
        self.check_alive()

class Player:
    def __init__(self):
        self.HAND = [] # array of cards
        self.name = ""
        self.current_card = 0
        self.active = True

    def choose_card(self, chosen_card):
        if not HAND[chosen_card].check_alive():
            # TODO add method to find alive card just in case
            return
        self.current_card = chosen_card
    
    def refresh_hand(self):
        cur = 0
        for card in self.HAND:
            if not card.alive:
                self.HAND.pop(cur)
            cur += 1
        if len(self.HAND) == 0:
            self.active = False


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

    CARD2IMG = Image('Assets/BayoWolf_300.png')
    insignia = pygame.image.load(get_file('Assets/TypePython.png'))

    CARDIMG = Image('Assets/AnnieConda_300.png')
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

def draw_screen(p1, p2, message=""):
    SCREEN.fill(BLUE)
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    draw_dialog_box()
    populate_dialog_box(message)
    draw_active_cards(p1, p2)
    draw_inactive_cards(p1, p2)
    draw_healthbars(p1, p2)
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
def draw_active_cards(p1, p2):
    # TODO get cards from player's hand
    # p1_card, p2_card = get_current_card(p1, p2)
    # p1_card.draw(SCREEN)
    # p2_card.draw(SCREEN)
    MY.CARD_R.draw(SCREEN)
    MY.CARD_L.draw(SCREEN)

def get_current_card(p1, p2):
    p1_card = p1.HAND[p1.current_card]
    p1_card_img = Image(p1_card_img.image_path)
    p1_card_obj = Object(p1_card_img)
    p1_card_obj.__setattr__("location", CARD_L_POS)
    p1_card_obj.__setattr__("sprite", p1_card_img)
    p2_card = p2.HAND[p2.current_card]
    p2_card_img = Image(p2_card.image_path)
    p2_card_obj = Object(p2_card_img)
    p2_card_obj.__setattr__("location", CARD_R_POS)
    p2_card_obj.__setattr__("sprite", p2_card_img)
    return p1_card_obj, p2_card_obj

# draw inactive cards
def draw_inactive_cards(p1, p2):
    # TODO skip current card
    L_pos_x, L_pos_y = 35, 475
    for card in p1.HAND:
        name = card.name
        SCREEN.blit(MY.insignia, (L_pos_x,L_pos_y))
        card_name = cardshand_font.render(name, True, BLACK)
        name_x = L_pos_x + 25
        name_y = L_pos_y + 3
        SCREEN.blit(card_name, (name_x, name_y))
        L_pos_y = L_pos_y + 25
    R_pos_x, R_pos_y = 535, 475
    for card in p2.HAND:
        name = card.name
        SCREEN.blit(MY.insignia, (R_pos_x,R_pos_y))
        card_name = cardshand_font.render(name, True, BLACK)
        name_x = R_pos_x + 25
        name_y = R_pos_y + 3
        SCREEN.blit(card_name, (name_x, name_y))
        R_pos_y = R_pos_y + 25

def draw_healthbars(p1, p2):
    p1_hp = p1.HAND[p1.current_card].HP
    p2_hp = p2.HAND[p2.current_card].HP
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
    # use sprite when coin flip animation resized
    

def coin_flip_click():
    coin_click = coin_font.render("flip the coin.", True, BLACK)
    coin_click_rect = coin_click.get_rect(topleft=(300,500))
    return coin_click_rect