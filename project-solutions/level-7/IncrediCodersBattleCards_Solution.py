from init import *

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
            return False

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
        # chosen_card is int index of card
        # if not HAND[chosen_card].check_alive():
        #     # TODO add method to find alive card just in case
        #     return
        self.current_card = chosen_card
    
    def refresh_hand(self):
        cur = 0
        for card in self.HAND:
            if not card.alive:
                self.HAND.pop(cur)
                self.current_card = 0
                if len(self.HAND) == 2:
                    return True
                if len(self.HAND) == 0:
                    self.active = False
            cur += 1
        return False
        
annie_conda = Card('Annie Conda', 'python', 'java', 'bash', "Assets/Annie_Highlight_02.png")
bayo_wolf = Card('Bayo Wolf', 'scratch', 'turtle', 'java', "Assets/Bayo_Highlight_02.png")
captain_javo = Card('Captain Javo', 'java', 'scratch', 'python', "Assets/Cpt_Javo_Highlight_02.png")
cryptic_creeper = Card('Cryptic Creeper', 'bash', 'python', 'turtle', "Assets/Creeper_Highlight_02.png")
emily_airheart = Card('Emily Airheart', 'turtle', 'bash', 'scratch', "Assets/Emily_AirHeart_Highlight_02.png")
grafika_turtle = Card('Grafika Turtle', 'turtle', 'bash', 'scratch', "Assets/Grafika_Highlight_02.png")
intelli_scents = Card('Intelli-Scents', 'scratch', 'turtle', 'java', "Assets/Intelliscents_Highlight_02.png")
java_lynn = Card('Java Lynn', 'java', 'scratch', 'python', "Assets/Java_Lynn_Highlight_02.png")
jitter_bug = Card('Jitter Bug', 'java', 'scratch', 'python', "Assets/Jitter_Bug_Highlight_02.png")
justin_timbersnake = Card('Justin Timbersnake', 'python', 'java', 'bash', "Assets/Justin_TSnake_Highlight_02.png")
mrs_scratcher = Card('Mrs. Scratcher', 'scratch', 'turtle', 'java', "Assets/Scratcher_Highlight_02.png")
paul_python = Card('Paul Python', 'python', 'java', 'bash', "Assets/Paul_Highlight_02.png")
queen_cobra = Card('Queen Cobra', 'python', 'java', 'bash', "Assets/Queen_Cobra_Highlight_02.png")
ram_rom = Card('Ram Rom', 'java', 'scratch', 'python', "Assets/RAM_ROM_Highlight_02.png")
sidewinder = Card('Sidewinder', 'python', 'java', 'bash', "Assets/SideWinder_Highlight_02.png")
syntax_turtle = Card('Syntax Turtle', 'turtle', 'bash', 'scratch', "Assets/Syntax_Highlight_02.png")
viralmuto = Card('Viralmuto', 'bash', 'python', 'scratch', "Assets/ViralMuto_Highlight_02.png")
virobotica = Card('Virobotica', 'bash', 'python', 'turtle', "Assets/Virobotica_Highlight_02.png")
virobots = Card('Virobots', 'bash', 'python', 'turtle', "Assets/Virobots_Highlight_02.png")
woodchuck_norris = Card('Woodchuck Norris', 'scratch', 'turtle', 'java', "Assets/Woodchuck_Highlight_02.png")

DECK = []
    #add all cards to deck
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

def reset_cards():
    for card in DECK:
        card.HP = 15
        card.alive = True

def flip_coin():
    return "Heads" if random.randint(0,1) == 1 else "Tails"

def check_game_end(player_one, player_two):
    # Check status of both players, if one player surviving then end the game
    exiting = True
    if player_one.active == False:
        exiting = victory(player_two)
    elif player_two.active == False:
        exiting = victory(player_one)
    if not exiting:
        reset_game(player_one, player_two)
    return False

def reset_game(p1, p2):
    # Reset cards
    reset_cards()

    # reshuffle deck
    # default version is that each character gets 3 randomly chosen cards
    # challenge version could be that they program choosing their cards? or each gets half the deck
    random.shuffle(DECK)
    # Deal cards to players
    p1.HAND = DECK[:3]
    p2.HAND = DECK[3:6]

    # Reset turn
    MY.TURN = 1

    # Reset players
    p1.active = True
    p1.active_turn = False
    p2.active = True
    p2.active_turn = False

    # Turn Coin Flip screen - flip a coin to see who goes first
    active = draw_turn_flip_screen(p1.name, p2.name)
    if active == p1_name:
        p1.active_turn = True
        draw_choose_hand_screen(p1)
        draw_choose_hand_screen(p2)
    elif active == p2_name:
        p2.active_turn = True
        draw_choose_hand_screen(p2)
        draw_choose_hand_screen(p1)
    
    # Run the game
    draw_screen(player_one, player_two)

draw_title_screen()

# Intro Screen - Enter player names
# p1_name, p2_name = draw_name_screen()

# OPTIONAL skip name screen for debugging, comment out previous line/uncomment following line
p1_name, p2_name = "p1", "p2"

# Create players and set active player
player_one = Player()
player_one.name = p1_name

player_two = Player()
player_two.name = p2_name

reset_game(player_one, player_two)

running = True

# Game loop 
while running: 
    clock.tick(60)
    for event in pygame.event.get():
        # Checks to see if player clicked close button on window
        check_stop(event)
        coin_button_rect = draw_coin_flip_button()

        # turn for each character:
        # choose attack (safe or risk) - only advanced, "big hit" is default
        # player clicks on attack
        # TODO player can choose which card to be active

        # player clicks on flip coin
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if coin_button_rect.collidepoint(mouse_position):
                draw_coin_animation()
                
                offense, defense = get_active_player(player_one, player_two)
                offense_card = offense.HAND[offense.current_card]
                defense_card = defense.HAND[defense.current_card]

                # add pieces of message together to show in dialog box
                message = ""
                message = add_to_message(message, "{}".format(MY.TURN))
                message = add_to_message(message, "{}".format(offense.name))
                
                # flip the coin
                coin = flip_coin()
                message = add_to_message(message, "{}".format(coin))

                # add result of the turn to dialog box message
                if coin == 'Heads':
                    damage = defense_card.attack(offense_card)
                    s_flag = "" if offense_card.name.endswith('s') == 1 else "s"
                    turn_msg = "{} took {} damage from {}'{} attack\n".format(defense_card.name, damage, offense_card.name, s_flag)
                    message = add_to_message(message, turn_msg)
                else:
                    turn_msg = "{} took no damage from {}\n".format(defense_card.name, offense_card.name)
                    message = add_to_message(message, turn_msg)

                # dialog box shows turn result
                draw_screen(player_one, player_two, message)
                player_one.refresh_hand()
                player_two.refresh_hand()
                # p1_card_check = player_one.refresh_hand()
                # if p1_card_check:
                #     draw_choose_twocard_screen(player_one)
                # p2_card_check = player_two.refresh_hand()
                # if p2_card_check:
                #     draw_choose_twocard_screen(player_two)

                # Switch active player
                switch_active_player(offense, defense)

                if check_game_end(player_one, player_two):
                    running = False
                    # TODO render some victory graphic?
                MY.TURN = MY.TURN + 1


    #Player picks card they would like to attack. 
        # how do they pick?? can they see entire hand? how to display cards?
        # do they pick one card and play til it's dead or do they pick a new card each turn? 
            # many cards have multi-turn attack implications, have to figure out how to implement future pieces
            # how to handle 2x heads.....??????
            # emily airheart - heads 2x to restore 2 health/paul python heads 2x/ramrom/woodchuck norris
            # grafika - define shell shock for one turn - does that mean she gets two turns in a row? or does that mean that dice roll is affected? 
            # intelliscents - redo a full round? what does that imply? undo HP loss? is a round defined by each player's turns? (2 turns = round?)
            # javalynn - heads gives anyone extra turn, 
            # justin timbersnake - redo opponent's next coin flip - automatic flip on next? or choice?
            # virobotica - increasing resistance by 1 - what is the scale for resistance?
        # if both players share screen have to show all cards, right?
        # how to display card HP? or just overall player HP? 
        # 150 HP seems like a lot when cards do at most 3 damage
    #Next, player picks an attack from their own card
    #Player flips coin
        # coin flip can help regular attack as well as risky attack
    #Depending on results of coin, damage is dealt to that card.
    #TODO: implement specific attacks based on the cards
    #If card health < 1, card is killed
        
    #If player has no cards left, player loses
    #Change player turn to the other player
