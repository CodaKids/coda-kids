from init import *

# Create all of the Cards		
annie_conda = Card('Annie Conda', 'python', 'java', 'bash', annie_conda_img, icon_python)
bayo_wolf = Card('Bayo Wolf', 'scratch', 'turtle', 'java', bayo_wolf_img, icon_scratch)
captain_javo = Card('Captain Javo', 'java', 'scratch', 'python', captain_javo_img, icon_java)
cryptic_creeper = Card('Cryptic Creeper', 'bash', 'python', 'turtle', cryptic_creeper_img, icon_bash)
emily_airheart = Card('Emily Airheart', 'turtle', 'bash', 'scratch', emily_airheart_img, icon_smallbasic)
grafika_turtle = Card('Grafika Turtle', 'turtle', 'bash', 'scratch', grafika_turtle_img, icon_smallbasic)
intelli_scents = Card('Intelli-Scents', 'scratch', 'turtle', 'java', intelli_scents_img, icon_scratch)
java_lynn = Card('Java Lynn', 'java', 'scratch', 'python', java_lynn_img, icon_java)
jitter_bug = Card('Jitter Bug', 'java', 'scratch', 'python', jitter_bug_img, icon_java)
justin_timbersnake = Card('Justin Timbersnake', 'python', 'java', 'bash', justin_timbersnake_img, icon_python)
mrs_scratcher = Card('Mrs. Scratcher', 'scratch', 'turtle', 'java', mrs_scratcher_img, icon_scratch)
paul_python = Card('Paul Python', 'python', 'java', 'bash', paul_python_img, icon_python)
queen_cobra = Card('Queen Cobra', 'python', 'java', 'bash', queen_cobra_img, icon_python)
ram_rom = Card('Ram Rom', 'java', 'scratch', 'python', ram_rom_img, icon_java)
sidewinder = Card('Sidewinder', 'python', 'java', 'bash', sidewinder_img, icon_python)
syntax_turtle = Card('Syntax Turtle', 'turtle', 'bash', 'scratch', syntax_turtle_img, icon_smallbasic)
viralmuto = Card('Viralmuto', 'bash', 'python', 'scratch', viralmuto_img, icon_bash)
virobotica = Card('Virobotica', 'bash', 'python', 'turtle', virobotica_img, icon_bash)
virobots = Card('Virobots', 'bash', 'python', 'turtle', virobots_img, icon_bash)
woodchuck_norris = Card('Woodchuck Norris', 'scratch', 'turtle', 'java', woodchuck_norris_img, icon_scratch)

DECK = []

# Add all cards to deck
DECK.append(annie_conda)
DECK.append(bayo_wolf)
DECK.append(captain_javo)
DECK.append(cryptic_creeper)
DECK.append(emily_airheart)
DECK.append(grafika_turtle)
DECK.append(intelli_scents)
DECK.append(java_lynn)
DECK.append(jitter_bug)
DECK.append(justin_timbersnake)
DECK.append(mrs_scratcher)
DECK.append(paul_python)
DECK.append(queen_cobra)
DECK.append(ram_rom)
DECK.append(sidewinder)
DECK.append(syntax_turtle)
DECK.append(viralmuto)
DECK.append(virobotica)
DECK.append(virobots)
DECK.append(woodchuck_norris)

class ChooseHandScreen(GameState):
	def __init__(self):
		super().__init__()
		self.next_state = "Game"
		self.card_shadow = pygame.Surface((300,421))
		self.card_shadow.fill(BLACK)
		self.card_shadow.set_alpha(50)
		self.shadows = []
		
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
		x, y = 200, 250
		self.count = 0
			
		for card in player.hand:
			card.set_location((x,y))
			shadow_pos = (x-144, y-204)
			self.shadows.append(shadow_pos)
			y = y + 100
			x = x + 100
	
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
		for card in DECK:
			card.HP = 15
			card.alive = True

		# Shuffle deck
		random.shuffle(DECK)
		
		# Deal cards to players
		self.player1.hand = DECK[:3]
		self.player2.hand = DECK[3:6]
				
class GameScreen(GameState):
	
	def __init__(self):
		super().__init__()
		self.next_state = "Victory"

		self.tech_attack_button = Button("Tech Type Attack", X_CENTER-105, 575, 210, 40, ondeck_teal, round_dark_blue, parent = self)		
		# self.coded_attack_button = Button("Coded Attack", X_CENTER-85, 625, 170, 40, coin_yellow, coin_dark_yellow, parent = self)
		self.instructions_box = InfoBox(INSTRUCTIONS, dialog_inst, BLACK, (200, 300), (X_CENTER, 200), 200)

		self.coin = Coin(coin_img, (X_CENTER, 475))
		self.turn_counter = 1
		self.flipping = False
		self.attacking = False
		self.coin_side = None
		
	def start(self, players):
		self.players = players
		self.player1 = players["player1"]
		self.player2 = players["player2"]
		
		self.attacker = self.player1 if self.player1.active_turn else self.player2
		self.defender = self.player1 if not self.player1.active_turn else self.player2
		
		self.player1_card_display = CardDisplay(self.player1, player1_card_display_data)
		self.player2_card_display = CardDisplay(self.player2, player2_card_display_data)

		self.player1_healthbar = Healthbar(self.player1, player1_healthbar_data)
		self.player2_healthbar = Healthbar(self.player2, player2_healthbar_data)
		
		self.player1_ondeck = OnDeck(self.player1, player1_ondeck_data)
		self.player2_ondeck = OnDeck(self.player2, player2_ondeck_data)

		self.dialog_box = DialogBox((200,300), (X_CENTER-100, 50))
		
	def get_event(self, event):
		if not self.flipping:
			self.tech_attack_button.get_event(event)
	
		self.player1_ondeck.get_event(event)
		self.player2_ondeck.get_event(event)
		
	def button_action(self, params):
		self.coin_side = self.flip_coin()
		self.coin.set_side(self.coin_side)
		self.flipping = True
				
	def update(self, dt):
		self.player1_healthbar.update()
		self.player2_healthbar.update()
		
		self.player1_ondeck.update()
		self.player2_ondeck.update()
		
		self.player1_card_display.update()
		self.player2_card_display.update()
		
		if self.flipping:
			self.flipping = self.coin.update(dt)
			if not self.flipping:
				self.attacking = True
		
		if self.attacking:
			offense_card = self.attacker.current_card 
			defense_card = self.defender.current_card
			
			message = ""
			message = add_to_message(message, "{}".format(self.turn_counter))
			message = add_to_message(message, "{}".format(self.attacker.name))
			message = add_to_message(message, "{}".format(self.coin_side))

			if self.coin_side == 'Heads':
				damage = defense_card.attacked_by(offense_card)
			
				s_flag = "" if offense_card.name.endswith('s') else "s"
				turn_msg = "{} took {} damage from {}'{} attack\n".format(defense_card.name, damage, offense_card.name, s_flag)
				message = add_to_message(message, turn_msg)
			else:
	
				turn_msg = "{} took no damage from {}\n".format(defense_card.name, offense_card.name)
				message = add_to_message(message, turn_msg)
			
			# Dialog box shows the result of the turn

			self.dialog_box.set_message(message)
			
			# update player hands
			
			self.player1.refresh_hand()
			self.player2.refresh_hand()
			
			self.attacking = False
			self.turn_counter += 1
					
			# Switch active player
			self.switch_active_player()
		
			winner = self.check_game_end()
			if winner:
				winner.set_as_winner()
				self.done = True
			
	def flip_coin(self):
		side = "Heads" if random.random() < 0.5 else "Tails"
		if side == "Heads":
			self.attacker.heads_count += 1
		else:
			self.attacker.heads_count = 0
	
		return side

	def switch_active_player(self):
		if self.player1.active_turn:
			self.attacker = self.player2
			self.defender = self.player1
		else:
			self.attacker = self.player1
			self.defender = self.player2
		
		self.attacker.active_turn = True
		self.defender.active_turn = False

	def check_game_end(self):
		# Check status of both players, if one player surviving then end the game
		exiting = False
		if not self.player1.active:
		    exiting = self.player2
		elif not self.player2.active:
		    exiting = self.player1

		return exiting
		
	def draw(self, surf):
		super().draw(surf)
		
		if self.turn_counter == 1:
			self.instructions_box.draw(surf)
		self.dialog_box.draw(surf)
		
		self.player1_card_display.draw(surf)
		self.player2_card_display.draw(surf)
		
		self.player1_healthbar.draw(surf)
		self.player2_healthbar.draw(surf)
		
		self.player1_ondeck.draw(surf)
		self.player2_ondeck.draw(surf)
		
		self.coin.draw(surf)
		self.tech_attack_button.draw(surf)
		# self.coded_attack_button.draw(surf)
		
if __name__=="__main__":		
	
	states = {
			"Title" : TitleScreen(),
			"GetNames": GetNameScreen(),
			"CoinFlip": CoinFlipScreen(),
			"ChooseHand" : ChooseHandScreen(),
			"Game" : GameScreen(),
			"Victory" : VictoryScreen()
			 }

game = GameRunner(SCREEN, states, "Title")

