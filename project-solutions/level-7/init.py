#============================================================
#PART 1: IMPORTING DEPENDENCIES AND ASSIGNING GLOBAL VARIABLES
import pygame
import random
import sys
from os import path
import textwrap

base_dir = path.dirname(__file__)
assets_path = path.join(base_dir, 'Assets')

WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
RED = [255, 0, 0]
GREEN = [0, 128, 0, 128]
BLUE = [0, 192, 255, 128]
WINDOW_WIDTH = 1000
X_CENTER = WINDOW_WIDTH // 2
WINDOW_HEIGHT = 700
Y_CENTER = WINDOW_HEIGHT // 2
CENTER_COORD = (X_CENTER, Y_CENTER)
WINDOW = (WINDOW_WIDTH, WINDOW_HEIGHT)
BACKGROUND_IMAGE = pygame.image.load(path.join(assets_path, "IncrediCards_Background.png")) 
TITLE_IMAGE = pygame.image.load(path.join(assets_path, "title_screen_wide_shadows.png")) 
TITLE_LOGO = pygame.image.load(path.join(assets_path, "IncredicodersLogo_850.png")) 
CARD_L_POS = pygame.math.Vector2(200,305)
CARD_R_POS = pygame.math.Vector2(800,305)
INSTRUCTIONS = ["Click Tech Type Attack", "to flip the coin: heads", "does 3 damage and", "tails misses.", "Be sure to check out", "your card's weaknesses", "and resistance. You can", "give more damage to a", "weak Tech Type, and you", "can receive less damage if", "you're resistant to a", "Tech Type."]
CHALLENGE_INSTRUCTIONS = "Click Tech Type Attack to flip the coin - heads does 3 damage (or more/less depending on your weakness and resistance) and tails misses. Or click Coded Attack to do 1 damage. Flip the coin - heads will do your card's special move!"
FPS = 30

pygame.init()
SCREEN = pygame.display.set_mode(WINDOW)
pygame.display.set_caption("IncrediCards")

#============================================================
#PART 2: CREATING A FRAMEWORK OF GENERAL CLASSES AND FUNCTIONS
class GameObject(object):
	
	def __init__(self, name = None, image = None, location = (0,0)):
		self.name = name
		self.image = image
		self.location = location
		
		if self.image is not None:
			self.rect = self.image.get_rect()
			self.rect.center = self.location
				
	def set_location(self, location):
		self.location = location
		self.rect.center = self.location
		
	def update(self, dt):
		pass
		
	def draw(self, surf):
		surf.blit(self.image, self.rect)

	def __str__(self):
		data = "name: " + self.name + "\n"
		data += "location: " + str(self.rect) + "\n"
		
		return data

class AnimatedObject(GameObject):
	def __init__(self, name, images, location):
		super().__init__(name)
		self.images = strip_from_sheet(images, (0, 0), (200, 200), 13)
		
		self.image = self.images[0]
		self.location = location
		
		self.rect = self.image.get_rect()
		self.rect.center = self.location
		
		self.current_frame = 0
		self.anim_time = 0
		
	def update(self, dt):
		pass
				
	def animate(self):
		self.current_frame = (self.current_frame + 1) % len(self.images)
		#bottom = self.rect.bottom
		self.image = self.images[self.current_frame]			
		#self.rect = self.image.get_rect(bottom = bottom)
		
	def draw(self, surf):
		surf.blit(self.image, self.rect)
		
class Card(GameObject):
	def __init__(self, name, techtype, weakness, resistance, image, typelogo, coded_type = 'none', coded_attack = ""):
		super().__init__(name, image)

		self.techtype = techtype
		self.weakness = weakness
		self.resistance = resistance
		self.HP = 15
		self.alive = True
		self.typelogo = typelogo
		self.coded_type = coded_type
		self.coded_attack = coded_attack
		# coded types are: extra_hit, extra_turn, gain_health, opponent_tails
	
	def attacked_by(self, offense_card):
		damage = 3 # default value
		
		# check strength/weakness and determine damage	
		if offense_card.techtype == self.resistance:
			damage = damage - 1
		elif offense_card.techtype == self.weakness:
			damage = damage + 1
		
		# take damage and return the damage amount
		self.take_damage(damage)
		return damage

	def gain_hp(self, gained_hp):
		self.HP = self.HP + gained_hp

	def check_max_hp(self):
		if self.HP > 15:
			self.HP = 15

	def take_damage(self, damage):
		self.HP = self.HP - damage
		if self.HP <= 0:
			self.HP = 0
			self.alive = False

	def __str__(self):
		data = super().__str__()
		
		data += "techtype: " + str(self.techtype) + "\n"
		data += "weakness: " + str(self.weakness) + "\n"
		data += "resistance: " + str(self.resistance) + "\n"
		data += "HP: " + str(self.HP) + "\n" 
		
		return data

class Player(object):
	def __init__(self, name):
		self.hand = [] # list of Cards
		self.name = name
		self.current_card = None
		self.active = True
		self.active_turn = False
		
		self.winner = False
		
	def set_as_winner(self):
		self.winner = True
		
	def set_card(self, chosen_card):
		self.current_card = chosen_card
	
	def switch_card(self, card_name):
		for card in self.hand:
			if card.name == card_name:
				self.current_card = card
				break
				
	def refresh_hand(self):
		if not self.current_card.alive:
			self.hand.remove(self.current_card)
			if len(self.hand) > 0:
				self.current_card = self.hand[0]	
			else:
				self.active = False

	def get_current_card(self):
		return self.current_card

	def gain_health(self, health_gained):
		if self.current_card.HP<15:
			self.current_card.gain_hp(health_gained)
			self.current_card.check_max_hp()
			return self.current_card
		else:
			for card in self.hand:
				if card.HP < 15:
					card.gain_hp(health_gained)
					card.check_max_hp()
					return card
		return None

	def __str__(self):
		data = "player name: " + self.name + "\n"
		data += "active turn: " + str(self.active_turn) + "\n"

		for i, card in enumerate(self.hand):
			data += "card " + str(i) + ": " + card.name + "\n"
		
		return data

class GameState(object):
	def __init__(self):
		self.done = False
		self.quit = False
	
	def start(self, players):
		pass
	
	def update(self, dt):
		pass
		
	def get_event(self, event):
		pass
		
	def draw(self, surf):
		surf.blit(BACKGROUND_IMAGE, (0,0))

class TitleScreen(GameState):
	def __init__(self):
		super().__init__()
		self.next_state = "GetNames"

	def start(self, players):
		self.start_button = Button("START", 425, 225, 170, 40, button_orange, button_red_orange, WHITE, round_font, self)
		
	def update(self, dt):
		pass
	
	def get_event(self, event):
		self.start_button.get_event(event)
		
	def draw(self, surf):
		super().draw(surf)
		surf.blit(TITLE_IMAGE, (0,0))
		surf.blit(TITLE_LOGO, (75,30))        
		self.start_button.draw(surf)

	def button_action(self, params):
		self.done = True

class GetNameScreen(GameState):
	def __init__(self):
		super().__init__()
		self.next_state = "CoinFlip" 
		self.input_box = InputBox(X_CENTER-150, 375, 300, 50, active_purple, inactive_dark_green, parent = self)
		
	def start(self, players):
		players["player1"] = Player("player 1")
		players["player2"] = Player("player 2")
		self.players = players
		self.current_player = players["player1"]	
		self.text = ""
		
		prompt_1 = "Click in the box to type in the"
		prompt_2 = "name for {} and press Enter.".format(self.current_player.name)
		
		self.info_box = InfoBox([prompt_1, prompt_2], bold_font, BLACK, (600,300), (X_CENTER, 320), 200, True)

	def update(self, dt):
		
		self.input_box.update()
		
		self.prompt_1 = "Click in the box to type in the"
		self.prompt_2 = "name for {} and press Enter.".format(self.current_player.name)

		self.info_box.update([self.prompt_1, self.prompt_2])

	def get_event(self, event):
		done = self.input_box.get_event(event)
		
		if done:
			if self.current_player == self.players["player1"]:
				self.current_player = self.players["player2"]
			else:
				self.done = True

	def set_name(self, name):
		self.current_player.name = name
		
	def draw(self, surf):
		super().draw(surf)
		self.info_box.draw(surf)	
		self.input_box.draw(surf)

class CoinFlipScreen(GameState):
	def __init__(self):
		super().__init__()
		self.next_state = "ChooseHand"
		
	def start(self, players):
		self.player1 = players["player1"]
		self.player2 = players["player2"]
		self.flipping = False
		self.choosing = True
		
		self.instructions = ["Flip to see who goes first!", "Heads for {}, tails for {}.".format(self.player1.name, self.player2.name)]
		
		self.flip_box = InfoBox(self.instructions, bold_font, BLACK,  (600,200), (X_CENTER, 150), 200)
	
		self.coin_flip_button = Button("Flip the Coin!", X_CENTER-85, 500, 170, 40, coin_yellow, coin_dark_yellow, parent = self)
		self.start_button =  Button("START", 425, 500, 150, 40, button_orange, button_red_orange, WHITE, round_font, parent = self)

		self.coin = Coin(coin_img, (X_CENTER, 375))
		
		self.winner = self.player1 if random.random() < 0.5 else self.player2
		self.winner.active_turn = True
		
	def get_event(self, event):
		if self.choosing and not self.flipping:
			self.coin_flip_button.get_event(event)
		else:
			self.start_button.get_event(event)
			
	def update(self, dt):
		if self.flipping:
			self.flipping = self.coin.update(dt)
			if not self.flipping:
				self.choosing = False
		else:
			self.winner_box = InfoBox(["{} will go first!".format(self.winner.name)], bold_font, BLACK, (550,100),(X_CENTER,200),200)
		
	def button_action(self, params):
		if self.choosing and not self.flipping:
			self.flipping = True
			if self.winner == self.player1:
				self.coin.set_side("Heads")
			else:
				self.coin.set_side("Tails")
		else:
			self.done = True
			
	def draw(self, surf):
		super().draw(surf)		
		if self.choosing:
			self.flip_box.draw(surf)
			self.coin_flip_button.draw(surf)
			self.coin.draw(surf)	
		else:
			self.coin.draw(surf)	
			self.winner_box.draw(surf)
			self.start_button.draw(surf)

class ChooseHandScreen(GameState):
	def __init__(self, deck, flag = False):
		super().__init__()
		self.next_state = "Game"
		self.card_shadow = pygame.Surface((300,421))
		self.card_shadow.fill(BLACK)
		self.card_shadow.set_alpha(50)
		self.shadows = []
		self.deck = deck
		self.challenge_flag = flag
		
	def start(self, players):
		self.players = players
		self.player1 = players["player1"]
		self.player2 = players["player2"]
				
		self.current_player = self.player1 if self.player1.active_turn else self.player2
	
		self.reset_cards()
	
		name = "{},".format(self.current_player.name)
		instructions_1 = "Click on the card"
		instructions_2 = "you want to use."
		
		self.info_box = InfoBox([name, instructions_1, instructions_2], bold_font, BLACK, (300,300), (800,300), 200)
		self.set_card_locations(self.player1)
		self.set_card_locations(self.player2)
		
	def set_card_locations(self, player):
		self.count = 0
		
		if self.challenge_flag:
			x, y = 175, 225
			x_delta = 60
			y_delta = 60	
		else:
			x, y = 200, 250
			x_delta = 100
			y_delta = 100
		for card in player.hand:
			card.set_location((x,y))
			shadow_pos = (x-144, y-204)
			self.shadows.append(shadow_pos)
			y = y + y_delta
			x = x + x_delta
	
	def get_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			for card in self.current_player.hand[::-1]:
				if card.rect.collidepoint(event.pos):
					self.current_player.set_card(card)
	
					self.count += 1
					if self.count == 2:
						break
					
					self.current_player = self.player2 if self.player1.active_turn else self.player1
					
					name = "{},".format(self.current_player.name)
					self.info_box.change_line(name, 0)
					return
					
			if self.current_player == self.player2:
				self.done = True
			
	def update(self, dt):
		if self.count == 2:
			self.done = True
		
	def draw(self, surf):
		super().draw(surf)		
		self.info_box.draw(surf)
		for i, card in enumerate(self.current_player.hand):
			surf.blit(self.card_shadow, self.shadows[i])
			card.draw(surf)
			
	def reset_cards(self):
		# Reset cards
		for card in self.deck:
			card.HP = 15
			card.alive = True

		# Shuffle deck
		random.shuffle(self.deck)
		
		# Deal cards to players
		if self.challenge_flag:
			self.player1.hand = self.deck[:5]
			self.player2.hand = self.deck[5:10]
		else:
			self.player1.hand = self.deck[:3]
			self.player2.hand = self.deck[3:6]
				
class VictoryScreen(GameState):
	def __init__(self):
		super().__init__()
		self.next_state = "GetNames"
			
	def start(self, players):
		self.player1 = players["player1"]
		self.player2 = players["player1"]
		
		self.winner = self.player1 if self.player1.winner else self.player2

		self.victor_box = InfoBox(["{} has won!".format(self.winner.name)], bold_font, WHITE, (300,75), (X_CENTER, 225), 150, bg_color = BLACK)
		self.play_button = Button("Play Again?", 250, 400, 200, 40, button_orange, button_red_orange, WHITE, round_font, self)
		self.play_button.action_params = "play"
		self.exit_button = Button("Exit", 625, 400, 100, 40, button_orange, button_red_orange, WHITE, round_font, self)
		self.exit_button.action_params = "exit"
		
	def get_event(self, event):
		self.play_button.get_event(event)
		self.exit_button.get_event(event)

	def update(self, dt):
		pass
		
	def button_action(self, params):
		if params == "exit":
			self.quit = True
		else:
			self.done = True
			
	def draw(self, surf):
		super().draw(surf)
		# surf.blit(self.victor_msg, self.victor_msg_rect)
		self.victor_box.draw(surf)
		self.play_button.draw(surf)
		self.exit_button.draw(surf)

class GameRunner(object):	
	def __init__(self, screen, states, start_state):
		self.screen = screen
		self.states = states
		self.start_state = start_state
		self.state = self.states[self.start_state]
		self.players = { }
		self.state.start(self.players)
		self.clock = pygame.time.Clock()
		self.run()
		
	def run(self):
		self.running = True

		while self.running:
			dt = self.clock.tick(FPS)
			self.get_events()
			self.update(dt)
			self.draw()
			
	def get_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
				
			self.state.get_event(event)
			
	def update(self, dt):
		self.state.update(dt)
		
		if self.state.done:
			self.next_state()
		
		if self.state.quit:
			self.running = False
			
	def next_state(self):
		next_state = self.state.next_state
		self.state.done = False
		self.state_name = next_state
		self.state = self.states[self.state_name]
		self.state.start(self.players)
				
	def quit(self):
		pygame.quit()
		sys.exit()

	def draw(self):
		self.state.draw(self.screen)
		pygame.display.update()

#============================================================
#PART 3: SETUP FOR THE BATTLE CARDS GAME

# Fonts
bold_font = pygame.font.SysFont('Arial', 35)
button_font = pygame.font.SysFont('Arial', 25)
round_font = pygame.font.SysFont('Arial', 25, True)
dialog_font = pygame.font.SysFont('Arial', 14)
dialog_bold = pygame.font.SysFont('Arial', 14, True)
dialog_inst = pygame.font.SysFont('Arial', 16)
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
TURN = 1
	
# on deck box 
on_deck_box_size = (250,100)

# healthbar locations		
player1_healthbar_data = {
					"name_x" : 68,
					"name_y" : 17,
					"healthbar_pos" : (68, 62),
					"width" : 265,
					"height" : 25,
					"change_val" : 8,
					"health_inc" : 15,
					"font" : dialog_font,
					"font_color" : hb_grey	
					}	

player2_healthbar_data = {
					"name_x" : X_CENTER + 168,
					"name_y" : 17,
					"healthbar_pos" : (X_CENTER + 168, 62),
					"width" : 265,
					"height" : 25,
					"change_val" : 8,
					"health_inc" : 15,
					"font" : dialog_font,
					"font_color" : hb_grey	
					}	

# card display locations and sizes
player1_card_display_data = {
					"active_box_pos" : (23, 15),
					"active_box_pos_s" : (25, 17),
					"shadow_pos" : (57, 102),
					"card_x" : 200,
					"card_y" : 305,
					"active_box_size" : (355,670),
					"active_box_size_s" : (350,665)
					}

player2_card_display_data = {
					"active_box_pos" : (X_CENTER+123, 15),
					"active_box_pos_s" : (X_CENTER+125, 17),
					"shadow_pos" : (X_CENTER+157, 102),
					"card_x" : 800,
					"card_y" : 305,
					"active_box_size" : (355,670),
					"active_box_size_s" : (350,665)
					}

player1_card_display_data_challenge = {
					"active_box_pos" : (23, 15),
					"active_box_pos_s" : (25, 17),
					"shadow_pos" : (57, 102),
					"card_x" : 200,
					"card_y" : 305,
					"active_box_size" : (355,680),
					"active_box_size_s" : (350,675)
					}

player2_card_display_data_challenge = {
					"active_box_pos" : (X_CENTER+123, 15),
					"active_box_pos_s" : (X_CENTER+125, 17),
					"shadow_pos" : (X_CENTER+157, 102),
					"card_x" : 800,
					"card_y" : 305,
					"active_box_size" : (355,680),
					"active_box_size_s" : (350,675)
					}

# ondeck boxes locations and sizes					
player1_ondeck_data = {
					"box_size" : (250, 100),
					"box_pos" : (75, 562),
					
					"title_x" : 130,
					"title_y" : 525,
					"title_w" : 150,
					"title_h" : 30,
					
					"card_box_size" : (200, 25),
					"on_deck_label_pos" : (24, 10),
					}

player2_ondeck_data = {
					"box_size" : (250, 100),
					"box_pos" : (675, 562),
					
					"title_x" : 730,
					"title_y" : 525,
					"title_w" : 150,
					"title_h" : 30,
					
					"card_box_size" : (200, 25),
					"on_deck_label_pos" : (24, 10),
					}

player1_ondeck_data_challenge = {
					"box_size" : (250, 130),
					"box_pos" : (75, 558),
					
					"title_x" : 130,
					"title_y" : 525,
					"title_w" : 150,
					"title_h" : 30,
					
					"card_box_size" : (200, 25),
					"on_deck_label_pos" : (24, 6),
					}

player2_ondeck_data_challenge = {
					"box_size" : (250, 130),
					"box_pos" : (675, 558),
					
					"title_x" : 730,
					"title_y" : 525,
					"title_w" : 150,
					"title_h" : 30,
					
					"card_box_size" : (200, 25),
					"on_deck_label_pos" : (24, 6),
					}
coin_img = pygame.image.load(path.join(assets_path, "CoinFlip03.png"))

# icon images
icon_bash = pygame.image.load(path.join(assets_path, "icon_bash.png"))
icon_java = pygame.image.load(path.join(assets_path, "icon_java.png"))
icon_python = pygame.image.load(path.join(assets_path, "icon_python.png"))
icon_scratch = pygame.image.load(path.join(assets_path, "icon_scratch.png"))
icon_small_basic = pygame.image.load(path.join(assets_path, "icon_smallbasic.png"))
icon_ondeck = pygame.image.load(path.join(assets_path, "icon_ondeck.png"))
icon_codedattack = pygame.image.load(path.join(assets_path, "icon_codedattack.png"))

# card images
annie_conda_img = pygame.image.load(path.join(assets_path, "Annie_Highlight_02.png")).convert()
bayo_wolf_img = pygame.image.load(path.join(assets_path, "Bayo_Highlight_02.png")).convert()
captain_javo_img = pygame.image.load(path.join(assets_path, "Cpt_Javo_Highlight_02.png")).convert()
cryptic_creeper_img = pygame.image.load(path.join(assets_path, "Creeper_Highlight_02.png")).convert()
emily_airheart_img = pygame.image.load(path.join(assets_path, "Emily_AirHeart_Highlight_02.png")).convert()
grafika_turtle_img = pygame.image.load(path.join(assets_path, "Grafika_Highlight_02.png")).convert()
intelli_scents_img = pygame.image.load(path.join(assets_path, "Intelliscents_Highlight_02.png")).convert()
java_lynn_img = pygame.image.load(path.join(assets_path, "Java_Lynn_Highlight_02.png")).convert()
jitter_bug_img = pygame.image.load(path.join(assets_path, "Jitter_Bug_Highlight_02.png")).convert()
justin_timbersnake_img = pygame.image.load(path.join(assets_path, "Justin_TSnake_Highlight_02.png")).convert()
mrs_scratcher_img = pygame.image.load(path.join(assets_path, "Scratcher_Highlight_02.png")).convert()
paul_python_img = pygame.image.load(path.join(assets_path, "Paul_Highlight_02.png")).convert()
queen_cobra_img = pygame.image.load(path.join(assets_path, "Queen_Cobra_Highlight_02.png")).convert()
ram_rom_img = pygame.image.load(path.join(assets_path, "RAM_ROM_Highlight_02.png")).convert()
sidewinder_img = pygame.image.load(path.join(assets_path, "SideWinder_Highlight_02.png")).convert()
syntax_turtle_img = pygame.image.load(path.join(assets_path, "Syntax_Highlight_02.png")).convert()
viralmuto_img = pygame.image.load(path.join(assets_path, "ViralMuto_Highlight_02.png")).convert()
virobotica_img = pygame.image.load(path.join(assets_path, "Virobotica_Highlight_02.png")).convert()
virobots_img = pygame.image.load(path.join(assets_path, "ViroBots_Highlight_02.png")).convert()
woodchuck_norris_img = pygame.image.load(path.join(assets_path, "Woodchuck_Highlight_02.png")).convert()

class Button(object):
	def __init__(self, text, x, y, width, height, color, outline_color, font_color = BLACK, font = button_font, parent = None):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.color = color
		self.outline_color = outline_color
		self.font_color = font_color
		self.font = font
		self.parent = parent
		self.action_params = None
		
		self.highlight_x = x + 5
		self.highlight_y = y + 6
		
		self.highlight = pygame.Surface((width-10, height/5))
		self.highlight.set_alpha(125)
		self.highlight.fill(WHITE)
		
		self.text_surf = font.render(self.text, True, self.font_color)
		self.text_rect = self.text_surf.get_rect()
		self.text_rect.center = self.rect.center
		
	def get_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.parent.button_action(self.action_params)
			
	def draw(self, surf):
		pygame.draw.rect(surf, self.color, self.rect, 0, 3)
		surf.blit(self.highlight, (self.highlight_x, self.highlight_y))
		surf.blit(self.text_surf, self.text_rect)
		pygame.draw.rect(surf, self.outline_color, self.rect, 3, 3)

class Coin(AnimatedObject):
	def __init__(self, images, location):
		super().__init__("coin", images, location)

		self.spinning = False
		self.visible_side = "Heads"
		self.frames = 0
		
	def set_side(self, side):
		if self.visible_side == "Heads":
			if side == "Heads":
				self.frames = 13
			else:
				self.frames = 6
	
			self.visible_side = side	
		
		elif self.visible_side == "Tails":
			if side == "Heads":
				self.frames = 7
			else:
				self.frames = 13
			
			self.visible_side = side
	
	def update(self, dt):
		if self.frames > 0:
			self.anim_time += dt
			if self.anim_time > 75: # change number for speed, larger number = slower speed for coin flip animation
				self.animate()
				self.frames -= 1
				self.anim_time = 0
				
			return True
		else:
			return False
			
	def draw(self, surf):
		super().draw(surf)

class InputBox(pygame.Surface):	
	def __init__(self, x, y, width, height, active_border_color, inactive_border_color, parent = None):
		super().__init__((width, height))
		self.fill(WHITE)
		self.rect = self.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.active_border_color = active_border_color
		self.inactive_border_color = inactive_border_color
		self.text = ""
		self.parent = parent
		self.text_color = BLACK
		
		self.active = False
		self.text_surface = bold_font.render(self.text, True, self.text_color)
		
	def get_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
				return
			
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					if len(self.text) > 15:
						self.text = self.text [:15]
					self.parent.set_name(self.text)
					self.clear()
					return True
					
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
	
			return False
	
	def update(self):
		self.color = active_purple if self.active else inactive_dark_green
		pygame.draw.rect(self, self.color, (0, 0, self.rect.width - 1 , self.rect.height - 1), 2)
		
		self.text_surface = bold_font.render(self.text, True, self.color)
		
		# Resize the box if the text is too long.
		width = max(200, self.text_surface.get_width()+10)
		if width > self.rect.width:
			self.rect.width = width
			super().__init__((self.rect.width, self.rect.height))
		
	def clear(self):
		self.fill(WHITE)
		self.text = ""
		self.text_surface = bold_font.render(self.text, True, self.text_color)
			
	def draw(self, surf):
		self.blit(self.text_surface, (5, 5))
		surf.blit(self, self.rect)
 
class InfoBox(pygame.Surface):
	def __init__(self, text, font, font_color, size, center_pos, alpha, input_box = False, bg_color = WHITE):
		super().__init__(size)
		self.bg_color = bg_color
		self.fill(bg_color)
		
		self.text = text
		self.font = font
		self.font_color = font_color
		self.alpha = alpha
		self.set_alpha(alpha)
		self.input_box = input_box # used if there is a text box on the panel
		self.rect = self.get_rect(center = center_pos)

		self.set_text_surfs(self.text)
		
	def set_text_surfs(self, text):
		self.text_surfs = []
		
		index = 1
		for line in text:
			surf = self.font.render(line, True, self.font_color, self.bg_color)
		
			# this calculates the spacing and positioning of the lines of text, taking into account
			# whether there is an input box drawn on the surface.
			if self.input_box:
				division = (self.rect.height // (len(text) + 2))
			else:
				division = (self.rect.height // (len(text) + 1))
				
			rect = surf.get_rect(centery = division * index)
			rect.centerx = self.rect.width//2
			self.text_surfs.append([surf, rect])
			index += 1
			
	def update(self, new_text):
		self.set_text_surfs(new_text)
	
	def change_line(self, text, line_number):
		surf = self.font.render(text, True, self.font_color, WHITE)
		self.text_surfs[line_number][0] = surf
		old_rect = self.text_surfs[line_number][1]
		rect = surf.get_rect(centery = old_rect.centery)
		rect.centerx = self.rect.width//2
		self.text_surfs[line_number][1] = rect
		
	def draw(self, surf):
		self.fill(self.bg_color)
		for line in self.text_surfs:
			self.blit(line[0], line[1])
		surf.blit(self, self.rect)
		pygame.draw.rect(surf, (84,84,84), self.rect, 3)

class Label(object):
	def __init__(self, text, img = None, x = 0, y = 0, width = 50, height = 27, label_font = cardshand_font, font_color = BLACK, alpha = 255):
		self.text = text
		self.img = img
		self.rect = pygame.Rect(x, y, width, height)
		self.font = label_font
		self.font_color = font_color
		self.alpha = alpha
		
		self.text_surf = self.font.render(self.text, True, self.font_color, ondeck_box_color)
		self.text_rect = self.text_surf.get_rect()

		if self.img is not icon_ondeck:
			self.img_x = self.rect.x + 3
			self.img_y = self.rect.y + 1

			self.text_rect.x = self.rect.x + 30
			self.text_rect.y = self.rect.y + 4
		
		else:
			self.img_x = self.rect.x + 15
			self.img_y = self.rect.y + 3

			self.text_rect.x = self.rect.x + 50
			self.text_rect.y = self.rect.y + 5
			
	def draw(self, surf):
		pygame.draw.rect(surf, ondeck_box_color, self.rect, 0, 8)
		pygame.draw.rect(surf, ondeck_teal, self.rect, 1, 8)

		if self.img is not None:
			surf.blit(self.img, (self.img_x, self.img_y))

		surf.blit(self.text_surf, (self.text_rect.x, self.text_rect.y))

class OnDeck(pygame.Surface):
	def __init__(self, player, deck_dict):
		self.player = player
		
		for key, val in deck_dict.items():
			
			if key == "box_size":
				self.box_size = val
				
			if key == "box_pos":
				self.pos = val
				
			if key == "title_x":
				title_x = val
				
			if key == "title_y":
				title_y = val

			if key == "title_w":
				title_w = val

			if key == "title_h":
				title_h = val
			
			if key == "card_box_size":
				self.card_box_size = val
				self.box_x = val[0]
				self.box_y = val[1]
			
			if key == "on_deck_label_pos":
				self.label_x = self.pos[0] + val[0]
				self.label_y = self.pos[1] + val[1]
			
		super().__init__(self.box_size)
		self.fill(ondeck_ltblue)
		self.set_alpha(85)
		
		# on deck title box
		self.ondeck_title = Label("On Deck", icon_ondeck, title_x, title_y, title_w, title_h, cardshand_font, ondeck_text)
		
		self.update()
		
	def get_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			for card_label in self.cards:
				if card_label.rect.collidepoint(event.pos):
					self.player.switch_card(card_label.text)
					break
					
	def update(self):	
		self.cards = []
		label_y = self.label_y
		
		for card in self.player.hand:
			if card.alive:
				if card == self.player.current_card:
					continue
	
				card_label = Label(card.name, card.typelogo, self.label_x, label_y, 200, 27, cardshand_font, BLACK)	
				self.cards.append(card_label)
				label_y += 30
			else:
				for card_label in self.cards:
					if card_label.text == card.name:
						self.cards.remove(card_label)
						break
			
	def draw(self, surf):
		self.ondeck_title.draw(surf)
		
		surf.blit(self, self.pos)
		
		pygame.draw.rect(surf, ondeck_outline_blue, (self.pos, self.box_size), 2, 3)
		
		for card in self.cards:
			card.draw(surf)
	
class Healthbar(object):
	def __init__(self, player, settings_dict):
		self.player = player
		self.player_health = 15
		self.settings_dict = settings_dict
		self.setup()
		
	def setup(self):
	
		for key, val in self.settings_dict.items():
				
			if key == "name_x":
				self.name_x = val
			
			if key == "name_y":
				self.name_y = val
			
			if key == "healthbar_pos":
				self.healthbar_pos = val
				self.healthbar_x = val[0]
				self.healthbar_y = val[1]
		
			if key == "width":
				self.width = val
				
			if key == "height":
				self.height = val
				
			if key == "change_val":
				self.color_change_val = val
				
			if key == "health_inc":
				self.health_inc = val
				
			if key == "font":
				self.font = val
				
			if key == "font_color":
				self.font_color = val

	def update(self):
		self.player_health = self.player.current_card.HP
		
	def draw(self, surf):
		name = bold_font.render(self.player.name, True, BLACK)
		surf.blit(name, (self.name_x, self.name_y))

		hb_size = (self.width, self.height)

		if self.player_health < 8:
			p1_color = hb_yellow
		else:
			p1_color = hb_green

		p1_bar = self.width * self.player_health / self.health_inc

		pygame.draw.rect(surf, hb_red, (self.healthbar_pos, (self.width, self.height)), 0, 2)
		pygame.draw.rect(surf, p1_color, (self.healthbar_pos, (p1_bar, self.height)), 0, 2)
		
		# add highlight to healthbars
		hl_w = p1_bar-10 if (p1_bar-10) >0 else 0
		hl_pos = (self.name_x + 5, self.name_y + 48)
		hl_size = (hl_w, self.height/3)
		hl = pygame.Surface(hl_size)
		hl.set_alpha(75)
		hl.fill(WHITE)

		surf.blit(hl, hl_pos)
		
		health = dialog_font.render("{}/15".format(self.player_health), True, hb_grey)
		surf.blit(health, (self.name_x + 5, self.name_y + 50))

class CardDisplay(object):
	def __init__(self, player, data_dict):
		self.player = player
		self.cards = player.hand
		self.active_card = self.player.get_current_card()
		self.card_shadow = pygame.Surface((300,421))
		self.card_shadow.fill(BLACK)
		self.card_shadow.set_alpha(50)
		
		for key, val in data_dict.items():
			
			if key == "active_box_pos":
				self.box_pos = val
				
			if key == "active_box_pos_s":
				self.box_pos_s = val
				
			if key == "shadow_pos":
				self.shadow_pos = val
				
			if key == "card_x":
				self.card_x = val
				
			if key == "card_y":
				self.card_y = val
			
			if key == "active_box_size":
				self.active_box_size = val
			
			if key == "active_box_size_s":
				self.active_box_size_s = val
				self.active_surface = pygame.Surface(self.active_box_size)

		self.active_surface.set_alpha(75)
		self.active_surface.fill(active_cyan)
		
		self.active_surface_s = pygame.Surface(self.active_box_size_s)
		self.active_surface_s.set_alpha(75)
		self.active_surface_s.fill(active_cyan)

		self.active_card.set_location((self.card_x, self.card_y))

	def update(self):
		self.active_card = self.player.get_current_card()
		self.active_card.set_location((self.card_x, self.card_y))

	def draw(self, surf):
		if self.player.active_turn:
			pygame.draw.rect(surf, active_cyan, (self.box_pos, self.active_box_size), 3, 10)
			surf.blit(self.active_surface_s, self.box_pos_s)
	
		# draw shadow first
		surf.blit(self.card_shadow, self.shadow_pos)
		self.active_card.draw(surf)

class DialogBox(object):
	def __init__(self, size, position):
		self.size = size
		self.position = position
		self.surface = pygame.Surface(size)
		self.surface.set_alpha(200)
		self.surface.fill(WHITE)
		self.rect = self.surface.get_rect(center=(X_CENTER, position[1]+150))
		self.message = None
			
	def set_message(self, message):
		self.message = message
		self.lines = message.splitlines()
		self.rd = "ROUND {}".format(self.lines[0])
		self.player = self.lines[1]
		self.coin = self.lines[2]
		self.status = self.lines[3:]
	
	def draw(self, surf):
		if self.message is not None:
			surf.blit(self.surface, self.rect)
			pygame.draw.rect(surf, (84,84,84), self.rect, 3)
			
			# render Round Number
			round_num = round_font.render(self.rd, True, round_dark_blue)
			round_surf = round_num.get_rect()
			round_surf.top = self.position[1] + 10
			round_surf.centerx = WINDOW_WIDTH//2
			
			surf.blit(round_num, round_surf)
		
			# render line separator
			pygame.draw.rect(surf, round_dark_blue, ((self.position[0] + 5, self.position[1] + 40), (190, 3)))
			# render current player
			current_player = dialog_bold.render("Player:", True, BLACK)
			surf.blit(current_player, (self.position[0] + 10, self.position[1] + 70))
			player_name = dialog_font.render(self.player, True, BLACK)
			surf.blit(player_name, (self.position[0] + current_player.get_width() + 12, self.position[1] + 70))
			# render Coin Toss
			coin_toss = dialog_bold.render("Coin Toss:", True, BLACK)
			surf.blit(coin_toss, (self.position[0] + 10, self.position[1] + 100))
			coin_result = dialog_font.render(self.coin, True, BLACK)
			surf.blit(coin_result, (self.position[0] + 10 + coin_toss.get_width(), self.position[1] + 100))
			# render turn result - may be over multiple lines
			x = self.position[0] + 10
			y = self.position[1] + 130
			for line in self.status:
				dlg_pos = (x,y)
				dlg_line = status_font.render(line, True, (BLACK))
				surf.blit(dlg_line, dlg_pos)
				y = y + 20

def add_to_message(msg, text_add):
    # Helper method to build game dialog messages and wrap over lines
    text = textwrap.wrap(text_add, 30)
    for line in text:
        msg += line + "\n"
    return msg

def strip_from_sheet(sheet, start, size, columns, rows=1):
	"""Strips individual frames from a sprite sheet given a start location,
		sprite size, and number of columns and rows."""

	frames = []

	for j in range(rows):
		for i in range(columns):
			location = (start[0]+size[0]*i, start[1]+size[1]*j)
			img = sheet.subsurface(pygame.Rect(location, size))
			frames.append(img)

	return frames

