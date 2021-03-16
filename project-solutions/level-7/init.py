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
        self.active_turn = False

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
WINDOW_WIDTH = 1000
X_CENTER = WINDOW_WIDTH // 2
WINDOW_LENGTH = 700
Y_CENTER = WINDOW_LENGTH // 2
CENTER_COORD = (X_CENTER, Y_CENTER)
WINDOW = pygame.math.Vector2(WINDOW_WIDTH, WINDOW_LENGTH)
SCREEN = start(WINDOW, "IncrediCards")
BACKGROUND_IMAGE = pygame.image.load("project-solutions/level-7/Assets/Table.png") 
TITLE_IMAGE = pygame.image.load("project-solutions/level-7/Assets/title_screen_test_wide.png") 
CARD_L_POS = pygame.math.Vector2(200,300)
CARD_R_POS = pygame.math.Vector2(800,300)
bold_font = pygame.font.SysFont('Arial', 35)
coin_font = pygame.font.SysFont('Arial', 25)
round_font = pygame.font.SysFont('Arial', 25, True)
dialog_font = pygame.font.SysFont('Arial', 14)
dialog_bold = pygame.font.SysFont('Arial', 14, True)
status_font = pygame.font.SysFont('Arial', 12)
cardshand_font = pygame.font.SysFont('Arial', 16, True)
ondeck_font = pygame.font.SysFont('Arial', 14, True)

clock = pygame.time.Clock()
# TODO maybe place all rects for drawing screen elements here instead
# List of Rects:
# name screen overlay, text entry box
# card/shadow box and position, active player boxes
# on deck box, inactive cards
# dialog box


class Data:
    # coin = Object(Image("Assets/CoinFlip.png")) - will need to be spritesheet object
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

def draw_title_screen():
    running = True
    while running:
        clock.tick(60)
        SCREEN.fill(BLUE)
        SCREEN.blit(BACKGROUND_IMAGE, (0,0))
        SCREEN.blit(TITLE_IMAGE, (0,0))

        button_pos = (425, 200)
        button_color = (220,90,25) # orange
        button_border_color = (170,45,10) # red-orange
        pygame.draw.rect(SCREEN, button_color, (button_pos, (150,40)), 0, 3)
        pygame.draw.rect(SCREEN, button_border_color, (button_pos, (150,40)), 3, 3)

        highlight = pygame.Surface((140,9))
        highlight.set_alpha(40)
        highlight.fill(WHITE)
        SCREEN.blit(highlight, (430,206))

        start_click = round_font.render("START", True, WHITE)
        text_pos = (455, 207)
        SCREEN.blit(start_click, text_pos)
        start_click_rect = start_click.get_rect(topleft=text_pos)

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_click_rect.collidepoint(mouse_pos):
                    running = False  
            pygame.display.update()
    return

def draw_name_screen():
    SCREEN.fill(BLUE)
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    p1 = get_name("Player 1")
    p2 = get_name("Player 2")
    return p1, p2

def get_name(current_player):
    clock = pygame.time.Clock()
    input_box = pygame.Rect(390, 375, 300, 50)

    dialog_surface = pygame.Surface((600,250))
    dialog_rect = dialog_surface.get_rect(center=CENTER_COORD)
    dialog_surface.set_alpha(200)
    dialog_surface.fill(WHITE)
    SCREEN.blit(dialog_surface, dialog_rect)

    color_inactive = (10,55,35)
    color_active = (60,0,200)
    color = color_inactive
    active = False
    text = ''
    done = False
    prompt_1 = "Click in the box to type in the"
    prompt_2 = "name for {} and press Enter.".format(current_player)
    
    prompt1_pos = (255, 125)
    prompt2_pos = (230, 175)
    prompt1_surface = bold_font.render(prompt_1, True, BLACK)
    prompt2_surface = bold_font.render(prompt_2, True, BLACK)
    text_rect = prompt1_surface.get_rect(center=(X_CENTER,275))
    text_rect2 = prompt2_surface.get_rect(center=(X_CENTER,325))
    SCREEN.blit(prompt1_surface, text_rect)
    SCREEN.blit(prompt2_surface, text_rect2)
    # add other instructions?

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if len(text) > 15:
                            text = text [:15]
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        SCREEN.blit(BACKGROUND_IMAGE, (0,0))
        SCREEN.blit(dialog_surface, dialog_rect)
        SCREEN.blit(prompt1_surface, text_rect)
        SCREEN.blit(prompt2_surface, text_rect2)
        pygame.draw.rect(SCREEN, WHITE, input_box)
        txt_surface = bold_font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        SCREEN.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(SCREEN, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def draw_screen(p1, p2, message=""):
    SCREEN.fill(BLUE)
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    draw_dialog_box()
    populate_dialog_box(message)
    draw_active_player(p1, p2)
    draw_active_cards(p1, p2)
    draw_inactive_cards(p1, p2)
    draw_healthbars(p1, p2)
    draw_coin_flip_button()
    pygame.display.update()

# draw screen - composed of:
# draw dialog box
def draw_dialog_box():
    dialog_surface = pygame.Surface((200,350))
    dialog_rect = dialog_surface.get_rect(center = (X_CENTER,300))
    dialog_surface.set_alpha(200)
    dialog_surface.fill(WHITE)
    SCREEN.blit(dialog_surface, dialog_rect)

def populate_dialog_box(message):
    if message == "":
        return
    round_color = (0,20,110) # dark blue

    lines = message.splitlines()
    rd = "ROUND {}".format(lines[0])
    player = lines[1]
    coin = lines[2]
    status = lines[3:]
    # render Round Number
    round_num = round_font.render(rd, True, round_color)
    round_surf = round_num.get_rect(center=(WINDOW_WIDTH//2,170))
    SCREEN.blit(round_num, round_surf)
    # render line separator
    pygame.draw.rect(SCREEN, round_color, ((405,200), (190,3)))
    # render current player
    current_player = dialog_bold.render("Current Player:", True, BLACK)
    SCREEN.blit(current_player, (410, 240))
    player_name = dialog_font.render(player, True, BLACK)
    SCREEN.blit(player_name, (425, 270))
    # render Coin Toss
    coin_toss = dialog_bold.render("Coin Toss:", True, BLACK)
    SCREEN.blit(coin_toss, (410, 300))
    coin_result = dialog_font.render(coin, True, BLACK)
    SCREEN.blit(coin_result, (500, 300))
    # render turn result - may be over multiple lines
    x = 410
    y = 350
    for line in status:
        dlg_pos = (x,y)
        dlg_line = status_font.render(line, True, (BLACK))
        SCREEN.blit(dlg_line, dlg_pos)
        y = y + 20

def draw_active_player(p1, p2):
    active_color = (65,255,210) # light cyan
    active_box_size = (355,665)
    active_box_size_s = (350,660)
    active_box_pos_L = (23,17)
    active_box_pos_R = (X_CENTER+123,17)
    active_box_pos_L_s = (25,19)
    active_box_pos_R_s = (X_CENTER+125,19)
    
    active_surface = pygame.Surface(active_box_size)
    active_surface.set_alpha(75)
    active_surface.fill(active_color)
    active_surface_s = pygame.Surface(active_box_size_s)
    active_surface_s.set_alpha(75)
    active_surface_s.fill(active_color)

    if p1.active_turn:
        # draw left active box
        pygame.draw.rect(SCREEN, active_color, (active_box_pos_L, active_box_size), 3, 10)
        SCREEN.blit(active_surface_s, active_box_pos_L_s)
    else:
        # draw right active box
        pygame.draw.rect(SCREEN, active_color, (active_box_pos_R, active_box_size), 3, 10)
        SCREEN.blit(active_surface_s, active_box_pos_R_s)

# draw active cards and health bars
def draw_active_cards(p1, p2):
    # draw shadow first
    shadow_surface = pygame.Surface((270,375))
    shadow_surface.set_alpha(50)
    shadow_surface.fill(BLACK)
    shadow_l_pos = (70,117)
    shadow_r_pos = (X_CENTER+170,117)
    SCREEN.blit(shadow_surface, shadow_l_pos)
    SCREEN.blit(shadow_surface, shadow_r_pos)

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
    draw_on_deck_boxes()

    card_box_size = (200,25)
    card_box_color = (255,240,225) # blue green
    card_box_b_color = (35,180,145) # dark blue
    card_surface = pygame.Surface(card_box_size)
    card_surface.set_alpha(150)
    card_surface.fill(card_box_color)

    L_pos_x, L_pos_y = 102, 560
    for card in p1.HAND:
        if card == p1.HAND[p1.current_card]:
            continue
        box_x = L_pos_x - 3
        box_y = L_pos_y - 1
        pygame.draw.rect(SCREEN, card_box_color, ((box_x,box_y), card_box_size), 0, 8)
        pygame.draw.rect(SCREEN, card_box_b_color, ((box_x,box_y), card_box_size), 1, 8)
        name = card.name
        SCREEN.blit(MY.insignia, (L_pos_x,L_pos_y))
        card_name = cardshand_font.render(name, True, BLACK)
        name_x = L_pos_x + 25
        name_y = L_pos_y + 3
        SCREEN.blit(card_name, (name_x, name_y))
        L_pos_y = L_pos_y + 32
    R_pos_x, R_pos_y = 702, 560
    for card in p2.HAND:
        if card == p2.HAND[p2.current_card]:
            continue
        box_x = R_pos_x - 3
        box_y = R_pos_y - 1
        pygame.draw.rect(SCREEN, card_box_color, ((box_x,box_y), card_box_size), 0, 8)
        pygame.draw.rect(SCREEN, card_box_b_color, ((box_x,box_y), card_box_size), 1, 8)
        name = card.name
        SCREEN.blit(MY.insignia, (R_pos_x,R_pos_y))
        card_name = cardshand_font.render(name, True, BLACK)
        name_x = R_pos_x + 25
        name_y = R_pos_y + 3
        SCREEN.blit(card_name, (name_x, name_y))
        R_pos_y = R_pos_y + 32

def draw_on_deck_boxes():
    box_size = (250,100)
    l_box_pos = (75, 552)
    r_box_pos = (675, 552)
    deck_color = (0,130,200)
    deck_border_color = (0,20,70)
    text_color = (0,20,110)
    
    deck_surface = pygame.Surface(box_size)
    deck_surface.set_alpha(85)
    deck_surface.fill(deck_color)
    SCREEN.blit(deck_surface, l_box_pos)
    SCREEN.blit(deck_surface, r_box_pos)
    pygame.draw.rect(SCREEN, deck_border_color, (l_box_pos, box_size), 2, 3)
    pygame.draw.rect(SCREEN, deck_border_color, (r_box_pos, box_size), 2, 3)
    on_deck = ondeck_font.render("ON DECK", True, text_color)

    od_l_pos = (165, 525)
    od_r_pos = (765, 525)
    SCREEN.blit(on_deck, od_l_pos)
    SCREEN.blit(on_deck, od_r_pos)

def draw_healthbars(p1, p2):
    p1_x = 68
    p_y = 20
    p2_x = X_CENTER + p1_x + 100
    p1_name = bold_font.render(p1.name, True, BLACK)
    SCREEN.blit(p1_name, (p1_x, p_y))
    p2_name = bold_font.render(p2.name, True, BLACK)
    SCREEN.blit(p2_name, (p2_x, p_y))
    p1_hp = p1.HAND[p1.current_card].HP
    p2_hp = p2.HAND[p2.current_card].HP
    p1_hp_pos = (p1_x,p_y+50)
    p2_hp_pos = (p2_x,p_y+50)
    width, height = 265, 25
    hb_size = (width, height)
    red = (150,20,10)
    green = (60,210,70)
    yellow = (240,220,50)
    if p1_hp < 8:
        p1_color = yellow
    else:
        p1_color = green
    if p2_hp < 8:
        p2_color = yellow
    else:
        p2_color = green
    p1_bar = width * p1_hp / 15
    p2_bar = width * p2_hp / 15
    pygame.draw.rect(SCREEN, red, (p1_hp_pos, (width,height)), 0, 2)
    pygame.draw.rect(SCREEN, red, (p2_hp_pos, (width,height)), 0, 2)
    pygame.draw.rect(SCREEN, p1_color, (p1_hp_pos, (p1_bar,height)), 0, 2)
    pygame.draw.rect(SCREEN, p2_color, (p2_hp_pos, (p2_bar,height)), 0, 2)
    # add highlight to healthbars
    p1_hl_w = p1_bar-10 if (p1_bar-10)>0 else 0
    p1_hl_pos = (p1_x+5, p_y+52)
    p2_hl_pos = (p2_x+5, p_y+52)
    p1_hl_size = (p1_hl_w,height/3)
    p1_hl = pygame.Surface(p1_hl_size)
    p1_hl.set_alpha(75)
    p1_hl.fill(WHITE)
    SCREEN.blit(p1_hl, p1_hl_pos)
    p2_hl_w = p2_bar-10 if (p2_bar-10)>0 else 0
    p2_hl_size = (p2_hl_w,height/3)
    p2_hl = pygame.Surface(p2_hl_size)
    p2_hl.set_alpha(75)
    p2_hl.fill(WHITE)
    SCREEN.blit(p2_hl, p2_hl_pos)
    grey = (65,65,65)
    p1_health = dialog_font.render("{}/15".format(p1_hp), True, grey)
    SCREEN.blit(p1_health, (p1_x+5, p_y+55))
    p2_health = dialog_font.render("{}/15".format(p2_hp), True, grey)
    SCREEN.blit(p2_health, (p2_x+5, p_y+55))

# draw coin flip button and text
def draw_coin_flip_button():
    coin_x, coin_y = X_CENTER-85, 585
    coin_button_pos = (coin_x, coin_y)
    coin_button_color = (230,200,35)
    # coin_button_border_color = (0,30,135)
    coin_button_border_color = (210,125,0)
    pygame.draw.rect(SCREEN, coin_button_color, (coin_button_pos, (170,40)), 0, 3)
    pygame.draw.rect(SCREEN, coin_button_border_color, (coin_button_pos, (170,40)), 3, 3)

    highlight = pygame.Surface((160,9))
    highlight.set_alpha(110)
    highlight.fill(WHITE)
    SCREEN.blit(highlight, (coin_x+5,coin_y+4))

    coin_click = coin_font.render("Flip the Coin!", True, BLACK)
    coin_text_pos = (coin_x+11, coin_y+5)
    SCREEN.blit(coin_click, coin_text_pos)
    coin_click_rect = coin_click.get_rect(topleft=coin_text_pos)    

    return coin_click_rect
    # use sprite when coin flip animation resized
    