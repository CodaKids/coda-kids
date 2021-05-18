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
    velocity = pygame.math.Vector2(0, 0)

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



# class Card:
#     def __init__(self, name, techtype, weakness, resistance, image_path):
#         self.name = name
#         self.techtype = techtype
#         self.weakness = weakness
#         self.resistance = resistance
#         self.image_path = image_path
#         self.HP = 15
#         self.alive = True
    
#     def check_alive(self):
#         if self.HP <= 0:
#             self.HP = 0
#             self.alive = False
#             return False

#     def attack(self, offense_card):
#         damage = 3 # default value

#         # check strength/weakness and determine damage
#         if offense_card.techtype == self.resistance:
#             damage = damage - 1
#         if offense_card.techtype == self.weakness:
#             damage = damage + 1
#         # take damage and return the damage amount
#         self.take_damage(damage)
#         return damage

#     def take_damage(self, damage):
#         self.HP = self.HP - damage
#         self.check_alive()

# class Player:
#     def __init__(self):
#         self.HAND = [] # array of cards
#         self.name = ""
#         self.current_card = 0
#         self.active = True
#         self.active_turn = False

#     def choose_card(self, chosen_card):
#         # chosen_card is int index of card
#         # if not HAND[chosen_card].check_alive():
#         #     # TODO add method to find alive card just in case
#         #     return
#         self.current_card = chosen_card
    
#     def refresh_hand(self):
#         cur = 0
#         for card in self.HAND:
#             if not card.alive:
#                 self.HAND.pop(cur)
#                 self.current_card = 0
#                 if len(self.HAND) == 2:
#                     return True
#                 if len(self.HAND) == 0:
#                     self.active = False
#             cur += 1
#         return False


#constants for screen
WINDOW_WIDTH = 1000
X_CENTER = WINDOW_WIDTH // 2
WINDOW_LENGTH = 700
Y_CENTER = WINDOW_LENGTH // 2
CENTER_COORD = (X_CENTER, Y_CENTER)
WINDOW = pygame.math.Vector2(WINDOW_WIDTH, WINDOW_LENGTH)
SCREEN = start(WINDOW, "IncrediCards")
BACKGROUND_IMAGE = pygame.image.load("project-solutions/level-7/Assets/Table.png") 
TITLE_IMAGE = pygame.image.load("project-solutions/level-7/Assets/title_screen_wide_shadows.png") 
CARD_L_POS = pygame.math.Vector2(200,305)
CARD_R_POS = pygame.math.Vector2(800,305)
# Fonts
bold_font = pygame.font.SysFont('Arial', 35)
button_font = pygame.font.SysFont('Arial', 25)
round_font = pygame.font.SysFont('Arial', 25, True)
dialog_font = pygame.font.SysFont('Arial', 14)
dialog_bold = pygame.font.SysFont('Arial', 14, True)
status_font = pygame.font.SysFont('Arial', 12)
cardshand_font = pygame.font.SysFont('Arial', 16, True)
# Colors
button_orange = (220,90,25)
button_red_orange = (170,45,10)
inactive_dark_green = (10,55,35)
active_purple = (60,0,200)
round_dark_blue = (0,20,110)
active_cyan = (65,255,210)
hb_red = (150,20,10)
hb_green = (60,210,70)
hb_yellow = (240,220,50)
hb_grey = (65,65,65)
coin_yellow = (230,200,35)
coin_dark_yellow = (210,125,0)
ondeck_box_color = (255,240,225)
ondeck_teal = (35,180,145)
ondeck_ltblue = (0,130,200) 
ondeck_outline_blue = (0,20,70)
ondeck_text = (0,20,110)
ondeck_titlebox = (255,235,210)

clock = pygame.time.Clock()
# TODO maybe place all rects for drawing screen elements here instead
# List of Rects:
# name screen overlay, text entry box
# card/shadow box and position, active player boxes
# on deck box, inactive cards
# dialog box

class Data:
    coin_sheet = SpriteSheet("Assets/CoinFlip03.png", (200,200))
    coin_anim = Animator(coin_sheet, 2)
    coin_obj = Object(coin_sheet.image_at(0))
    coin_obj.location = (X_CENTER, 450)
    # TODO need to dynamically assign type insignias
    insignia = pygame.image.load(get_file('Assets/TypePython.png'))
    card_shadow = pygame.Surface((300,421))
    card_shadow.set_alpha(50)
    card_shadow.fill(BLACK)

    TURN = 1

MY = Data()

def fill_screen():
    clock.tick(60)
    SCREEN.fill(BLUE)
    SCREEN.blit(BACKGROUND_IMAGE, (0,0))
    
def draw_transparent_white_rect(size, center_pos, alpha_value):
    white_surface = pygame.Surface(size)
    white_rect = white_surface.get_rect(center = center_pos)
    white_surface.set_alpha(alpha_value)
    white_surface.fill(WHITE)
    SCREEN.blit(white_surface, white_rect)

def draw_title_screen():
    running = True
    while running:
        fill_screen()
        SCREEN.blit(TITLE_IMAGE, (0,0))

        start_click_rect = draw_button(button_orange, button_red_orange, "START", 150, 40, 425, 200, WHITE, round_font)

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_click_rect.collidepoint(mouse_pos):
                    running = False  
            pygame.display.update()
    return

def draw_name_screen():
    fill_screen()
    p1 = get_name("Player 1")
    p2 = get_name("Player 2")
    return p1, p2
  
def get_name(current_player):
    clock = pygame.time.Clock()
    input_box = pygame.Rect(390, 375, 300, 50)

    draw_transparent_white_rect((600,250),CENTER_COORD,200)

    color = inactive_dark_green
    active = False
    text = ''
    done = False
    prompt_1 = "Click in the box to type in the"
    prompt_2 = "name for {} and press Enter.".format(current_player)

    prompt1_surface = bold_font.render(prompt_1, True, BLACK)
    prompt2_surface = bold_font.render(prompt_2, True, BLACK)
    text_rect = prompt1_surface.get_rect(center=(X_CENTER,275))
    text_rect2 = prompt2_surface.get_rect(center=(X_CENTER,325))
    SCREEN.blit(prompt1_surface, text_rect)
    SCREEN.blit(prompt2_surface, text_rect2)

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
                color = active_purple if active else inactive_dark_green
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
        draw_transparent_white_rect((600,300),(X_CENTER,320),200)
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

def draw_turn_flip_screen(p1_name, p2_name):
    # display coin, instruction and flip button
    flipping = True
    while flipping:
        fill_screen()

        # draw white box for instructions
        draw_transparent_white_rect((600,200), (X_CENTER, 150), 200)

        # draw instructions
        instruction = bold_font.render("Flip to see who goes first!", True, BLACK)
        instruction_rect = instruction.get_rect(center=(X_CENTER, 130))
        SCREEN.blit(instruction, instruction_rect)
        instruction_b_text = "Heads for {}, tails for {}.".format(p1_name,p2_name)
        instruction_b = bold_font.render(instruction_b_text, True, BLACK)
        instruction_b_rect = instruction_b.get_rect(center=(X_CENTER, 170))
        SCREEN.blit(instruction_b, instruction_b_rect)

        # draw coin flip button
        coin_rect = draw_coin_flip_button(415, 500)
        MY.coin_obj.location = (X_CENTER, 375)
        MY.coin_obj.draw(SCREEN)

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if coin_rect.collidepoint(mouse_pos):
                    draw_coin_animation()
                    winner = p1_name if random.randint(0,1) == 1 else p2_name
                    flipping = False  
            pygame.display.update()

    # display result and show start button
    first_player = True
    while first_player:
        fill_screen()

        # draw start button
        start_click_rect = draw_button(button_orange, button_red_orange, "START", 150, 40, 425,400, WHITE, round_font)

        # draw white box for visual clarity
        draw_transparent_white_rect((550,100),(X_CENTER,300),200)

        # draw first player name
        first_player = bold_font.render("{} will go first!".format(winner), True, BLACK)
        fp_rect = first_player.get_rect(center=(X_CENTER, 300))
        SCREEN.blit(first_player, fp_rect)

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_click_rect.collidepoint(mouse_pos):
                    first_player = False  
                    return winner
            pygame.display.update()

def draw_choose_hand_screen(current_player):
    # draw table
    # draw cards in player's hand, vertical cascade on left hand side showing top part of cards (more flexibility for more than three cards in their hand)
    # draw instructions on right hand side
    # once a card is clicked, should we show the card? just the name of the card?
    # set clicked card to first card in player's hand
    running = True
    while running:
        fill_screen()

        # draw white box for instructions
        draw_transparent_white_rect((300,300),(800,300),200)

        # draw instructions
        name = bold_font.render("{},".format(current_player.name), True, BLACK)
        name_rect = name.get_rect(center=(800, 260))
        SCREEN.blit(name, name_rect)

        instruction = bold_font.render("Click on the card", True, BLACK)
        instruction_rect = instruction.get_rect(center=(800, 300))
        SCREEN.blit(instruction, instruction_rect)

        instruction_b = bold_font.render("you want to use.", True, BLACK)
        instruction_b_rect = instruction_b.get_rect(center=(800, 340))
        SCREEN.blit(instruction_b, instruction_b_rect)

        x, y = 200, 250
        clickable_rects = []
        for card in current_player.HAND:
            card_pos = pygame.math.Vector2(x,y)
            card_img = Image(card.image_path)
            card_obj = Object(card_img)
            card_obj.location = card_pos
            r = card_obj.get_transformed_rect()
            shadow_pos = (x-144, y-204)
            SCREEN.blit(MY.card_shadow, shadow_pos)
            card_obj.draw(SCREEN)
            clickable_rects.append(r)
            y = y + 100
            x = x + 100

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if clickable_rects[0].collidepoint(mouse_pos):
                    current_player.choose_card(0)
                    running = False  
                if clickable_rects[1].collidepoint(mouse_pos):
                    current_player.choose_card(1)
                    running = False  
                if clickable_rects[2].collidepoint(mouse_pos):
                    current_player.choose_card(2)
                    running = False  
            pygame.display.update()
    return

def draw_screen(p1, p2, message=""):
    fill_screen()
    draw_transparent_white_rect((200,300), (X_CENTER,200),200)
    populate_dialog_box(message, 80)
    draw_active_player(p1, p2)
    draw_active_cards(p1, p2)
    draw_inactive_cards(p1, p2)
    draw_healthbars(p1, p2)
    draw_coin_flip_button()
    draw_button(ondeck_teal, active_purple, "Tech Type Attack", 210, 40, X_CENTER-105, 380)
    MY.coin_obj.location = (X_CENTER, 525)
    MY.coin_obj.draw(SCREEN) 
    pygame.display.update()

def populate_dialog_box(message, position):
    if message == "":
        # round 0, display initial instructions in box instead
        instructions = "Click Tech Type Attack to flip the coin - heads does 3 damage (or more/less depending on your weakness and resistance) and tails misses. Or click Coded Attack to do 1 damage. Flip the coin - heads will do your card's special move!"
        text = textwrap.wrap(instructions, 25)
        pos_y = 80
        for line in text:
            inst_line = dialog_bold.render(line, True, BLACK)
            inst_surf = inst_line.get_rect(center=(WINDOW_WIDTH//2,pos_y))
            SCREEN.blit(inst_line, inst_surf)
            pos_y = pos_y + 20 
        return

    lines = message.splitlines()
    rd = "ROUND {}".format(lines[0])
    player = lines[1]
    coin = lines[2]
    status = lines[3:]
    # render Round Number
    round_num = round_font.render(rd, True, round_dark_blue)
    round_surf = round_num.get_rect(center=(WINDOW_WIDTH//2,position))
    SCREEN.blit(round_num, round_surf)
    # render line separator
    pygame.draw.rect(SCREEN, round_dark_blue, ((405,position+20), (190,3)))
    # render current player
    current_player = dialog_bold.render("Current Player:", True, BLACK)
    SCREEN.blit(current_player, (410, position+60))
    player_name = dialog_font.render(player, True, BLACK)
    SCREEN.blit(player_name, (425, position+90))
    # render Coin Toss
    coin_toss = dialog_bold.render("Coin Toss:", True, BLACK)
    SCREEN.blit(coin_toss, (410, position+120))
    coin_result = dialog_font.render(coin, True, BLACK)
    SCREEN.blit(coin_result, (500, position+120))
    # render turn result - may be over multiple lines
    x = 410
    y = position+170
    for line in status:
        dlg_pos = (x,y)
        dlg_line = status_font.render(line, True, (BLACK))
        SCREEN.blit(dlg_line, dlg_pos)
        y = y + 20

def draw_active_player(p1, p2):
    active_box_size = (355,665)
    active_box_size_s = (350,660)
    active_box_pos_L = (23,17)
    active_box_pos_R = (X_CENTER+123,17)
    active_box_pos_L_s = (25,19)
    active_box_pos_R_s = (X_CENTER+125,19)
    
    active_surface = pygame.Surface(active_box_size)
    active_surface.set_alpha(75)
    active_surface.fill(active_cyan)
    active_surface_s = pygame.Surface(active_box_size_s)
    active_surface_s.set_alpha(75)
    active_surface_s.fill(active_cyan)

    if p1.active_turn:
        # draw left active box
        pygame.draw.rect(SCREEN, active_cyan, (active_box_pos_L, active_box_size), 3, 10)
        SCREEN.blit(active_surface_s, active_box_pos_L_s)
    elif p2.active_turn:
        # draw right active box
        pygame.draw.rect(SCREEN, active_cyan, (active_box_pos_R, active_box_size), 3, 10)
        SCREEN.blit(active_surface_s, active_box_pos_R_s)

def draw_active_cards(p1, p2):
    # draw shadow first
    shadow_l_pos = (57,102)
    shadow_r_pos = (X_CENTER+157,102)
    SCREEN.blit(MY.card_shadow, shadow_l_pos)
    SCREEN.blit(MY.card_shadow, shadow_r_pos)

    p1_card = get_current_card(p1, "L")
    p2_card = get_current_card(p2, "R")
    p1_card.draw(SCREEN)
    p2_card.draw(SCREEN)

def get_current_card(player, side):
    p_card = player.HAND[player.current_card]
    p_card_img = Image(p_card.image_path)
    p_card_obj = Object(p_card_img)
    if side == "L":
        p_card_obj.__setattr__("location", CARD_L_POS)
    else:
        p_card_obj.__setattr__("location", CARD_R_POS)
    p_card_obj.__setattr__("sprite", p_card_img)
    return p_card_obj

def draw_inactive_cards(p1, p2):
    draw_on_deck_boxes()

    card_box_size = (200,25)
    card_surface = pygame.Surface(card_box_size)
    card_surface.set_alpha(150)
    card_surface.fill(ondeck_box_color)

    L_pos_x, L_pos_y = 102, 570
    for card in p1.HAND:
        if card == p1.HAND[p1.current_card]:
            continue
        box_x = L_pos_x - 3
        box_y = L_pos_y - 1
        pygame.draw.rect(SCREEN, ondeck_box_color, ((box_x,box_y), card_box_size), 0, 8)
        pygame.draw.rect(SCREEN, ondeck_teal, ((box_x,box_y), card_box_size), 1, 8)
        name = card.name
        SCREEN.blit(MY.insignia, (L_pos_x,L_pos_y))
        card_name = cardshand_font.render(name, True, BLACK)
        name_x = L_pos_x + 25
        name_y = L_pos_y + 3
        SCREEN.blit(card_name, (name_x, name_y))
        L_pos_y = L_pos_y + 32
    R_pos_x, R_pos_y = 702, 570
    for card in p2.HAND:
        if card == p2.HAND[p2.current_card]:
            continue
        box_x = R_pos_x - 3
        box_y = R_pos_y - 1
        pygame.draw.rect(SCREEN, ondeck_box_color, ((box_x,box_y), card_box_size), 0, 8)
        pygame.draw.rect(SCREEN, ondeck_teal, ((box_x,box_y), card_box_size), 1, 8)
        name = card.name
        SCREEN.blit(MY.insignia, (R_pos_x,R_pos_y))
        card_name = cardshand_font.render(name, True, BLACK)
        name_x = R_pos_x + 25
        name_y = R_pos_y + 3
        SCREEN.blit(card_name, (name_x, name_y))
        R_pos_y = R_pos_y + 32

def draw_on_deck_boxes():
    box_size = (250,100)
    l_box_pos = (75, 562)
    r_box_pos = (675, 562)
    
    deck_surface = pygame.Surface(box_size)
    deck_surface.set_alpha(85)
    deck_surface.fill(ondeck_ltblue)
    SCREEN.blit(deck_surface, l_box_pos)
    SCREEN.blit(deck_surface, r_box_pos)
    pygame.draw.rect(SCREEN, ondeck_outline_blue, (l_box_pos, box_size), 2, 3)
    pygame.draw.rect(SCREEN, ondeck_outline_blue, (r_box_pos, box_size), 2, 3)

    # on deck title boxes
    title_box_size = (150,30)
    title_surface = pygame.Surface(title_box_size)
    title_surface.fill(ondeck_titlebox)
    pygame.draw.rect(SCREEN, ondeck_titlebox, ((130,525), title_box_size), 0, 8)
    pygame.draw.rect(SCREEN, ondeck_titlebox, ((730,525), title_box_size), 0, 8)

    od_l_pos = (165, 530)
    od_r_pos = (765, 530)
    on_deck = cardshand_font.render("ON DECK", True, ondeck_text)
    SCREEN.blit(on_deck, od_l_pos)
    SCREEN.blit(on_deck, od_r_pos)

def draw_healthbars(p1, p2):
    p1_x = 68
    p_y = 17
    p2_x = X_CENTER + p1_x + 100
    p1_name = bold_font.render(p1.name, True, BLACK)
    SCREEN.blit(p1_name, (p1_x, p_y))
    p2_name = bold_font.render(p2.name, True, BLACK)
    SCREEN.blit(p2_name, (p2_x, p_y))
    p1_hp = p1.HAND[p1.current_card].HP
    p2_hp = p2.HAND[p2.current_card].HP
    p1_hp_pos = (p1_x,p_y+45)
    p2_hp_pos = (p2_x,p_y+45)
    width, height = 265, 25
    hb_size = (width, height)

    if p1_hp < 8:
        p1_color = hb_yellow
    else:
        p1_color = hb_green
    if p2_hp < 8:
        p2_color = hb_yellow
    else:
        p2_color = hb_green
    p1_bar = width * p1_hp / 15
    p2_bar = width * p2_hp / 15
    pygame.draw.rect(SCREEN, hb_red, (p1_hp_pos, (width,height)), 0, 2)
    pygame.draw.rect(SCREEN, hb_red, (p2_hp_pos, (width,height)), 0, 2)
    pygame.draw.rect(SCREEN, p1_color, (p1_hp_pos, (p1_bar,height)), 0, 2)
    pygame.draw.rect(SCREEN, p2_color, (p2_hp_pos, (p2_bar,height)), 0, 2)
    # add highlight to healthbars
    p1_hl_w = p1_bar-10 if (p1_bar-10)>0 else 0
    p1_hl_pos = (p1_x+5, p_y+48)
    p2_hl_pos = (p2_x+5, p_y+48)
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
    
    p1_health = dialog_font.render("{}/15".format(p1_hp), True, hb_grey)
    SCREEN.blit(p1_health, (p1_x+5, p_y+50))
    p2_health = dialog_font.render("{}/15".format(p2_hp), True, hb_grey)
    SCREEN.blit(p2_health, (p2_x+5, p_y+50))

def draw_coin_flip_button(x=X_CENTER-85, y=625):
    return draw_button(coin_yellow, coin_dark_yellow, "Flip the Coin!", 170, 40, x, y)

def draw_button(button_color, button_outline, button_text, width, height, x, y, font_color = BLACK, font=button_font):
    button_pos = (x, y)
    button_rect = pygame.draw.rect(SCREEN, button_color, (button_pos, (width,height)), 0, 3)
    pygame.draw.rect(SCREEN, button_outline, (button_pos, (width,height)), 3, 3)

    highlight = pygame.Surface((width-10,height/5))
    highlight.set_alpha(150)
    highlight.fill(WHITE)
    SCREEN.blit(highlight, (x+5,y+5))

    button_click = font.render(button_text, True, font_color)
    text_rect = button_click.get_rect()
    text_rect.center = button_rect.center
    SCREEN.blit(button_click, text_rect)
    click_rect = button_click.get_rect(topleft=button_pos)    

    return click_rect

def draw_coin_animation():
    # MY.coin_obj.sprite = MY.coin_anim
    # MY.coin_obj.update(10)
    MY.coin_anim.play(.01)
    MY.coin_anim.frame_time = 10000
    MY.coin_anim.set_duration(20)
    # MY.coin_anim.update(10)
    for i in range(100):
        MY.coin_anim.update(1)
        MY.coin_obj.sprite = MY.coin_anim
        MY.coin_obj.draw(SCREEN)
    MY.coin_anim.reset()

def victory(player):
    # draw screen
    # draw victory message and victor's name
    # draw play again button and exit game button

    running = True
    while running:
        fill_screen()

        victor_msg = bold_font.render("{} HAS WON!".format(player.name), True, BLACK)
        victor_msg_rect = victor_msg.get_rect(center=(X_CENTER, 240))
        SCREEN.blit(victor_msg, victor_msg_rect)

        # play again button
        play_again_rect = draw_button(button_orange, button_red_orange, "Play Again?", 200, 40, 260, 400, WHITE, round_font)
        
        # exit button
        exit_rect = draw_button(button_orange, button_red_orange, "Exit", 100, 40, 600, 400, WHITE, round_font)
        
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(mouse_pos):
                    running = False 
                    return False 
                if exit_rect.collidepoint(mouse_pos):
                    running = False 
                    return True 
            pygame.display.update()

    # # display victor - TODO: render victory on screen
    # print("Player {} has won the game!".format(player.name))
    # # return true if play again button pressed, else return false
    # return True

def switch_active_player(offense, defense):
    offense.active_turn = False
    defense.active_turn = True

def get_active_player(player_one, player_two):
    if player_one.active_turn:
        return player_one, player_two  
    else:
        return player_two, player_one

def add_to_message(msg, text_add):
    # Helper method to build game dialog messages and wrap over lines
    text = textwrap.wrap(text_add, 30)
    for line in text:
        msg += line + "\n"
    return msg
