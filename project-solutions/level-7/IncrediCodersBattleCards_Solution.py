from init import *
import random

def flip_coin():
    return "Heads" if random.randint(0,1) == 1 else "Tails"

def get_active_player(turn):
    # TODO change logic when coinflip determines first player
    # use player.active_turn
    if turn%2 == 1:
        player_one.active_turn = True
        player_two.active_turn = False
        return player_one, player_two  
    else:
        player_one.active_turn = False
        player_two.active_turn = True
        return player_two, player_one

def check_game_end():
    # check status of both players, if one player surviving then end the game
    if player_one.active == False:
        victory(player_two)
        return True
    elif player_two.active == False:
        victory(player_one)
        return True
    return False

def victory(player):
    # display victor - TODO: render victory on screen
    print("Player {} has won the game!".format(player.name))

def add_to_message(msg, text_add):
    # TODO play with max width, may not need to be 22 once font is smaller
    text = textwrap.wrap(text_add, 30)
    for line in text:
        msg += line + "\n"
    return msg
    
def check_cards(player):
    if not player.HAND[player.current_card].alive:
        player.current_card += 1
    if player.current_card > 2: # TODO need to update this logic for other scenarios
        player.active = False

DECK = []
# Move to Data class????
annie_conda = Card('Annie Conda', 'python', 'java', 'bash', "assets/AnnieConda.png")
bayo_wolf = Card('Bayo Wolf', 'scratch', 'turtle', 'java', "assets/BayoWolf.png")
captain_javo = Card('Captain Java', 'java', 'scratch', 'python', "assets/CaptainJavo.png")
cryptic_creeper = Card('Cryptic Creeper', 'bash', 'python', 'turtle', "assets/CrypticCreeper.png")
emily_airheart = Card('Emily Airheart', 'turtle', 'bash', 'scratch', "assets/EmilyAirHeart.png")
grafika_turtle = Card('Grafika Turtle', 'turtle', 'bash', 'scratch', "assets/GrafikaTurtle.png")
intelli_scents = Card('Intelli-Scents', 'scratch', 'turtle', 'java', "assets/IntelliScents.png")
java_lynn = Card('Java Lynn', 'java', 'scratch', 'python', "assets/JavaLynn.png")
jitter_bug = Card('Jitter Bug', 'java', 'scratch', 'python', "assets/JitterBug.png")
justin_timbersnake = Card('Justin Timbersnake', 'python', 'java', 'bash', "assets/JustinTimbersnake.png")
mrs_scratcher = Card('Mrs. Scratcher', 'scratch', 'turtle', 'java', "assets/MrsScratcher.png")
paul_python = Card('Paul Python', 'python', 'java', 'bash', "assets/PaulPython.png")
queen_cobra = Card('Queen Cobra', 'python', 'java', 'bash', "assets/QueenCobra.png")
ram_rom = Card('Ram Rom', 'java', 'scratch', 'python', "assets/RAMROM.png")
sidewinder = Card('Sidewinder', 'python', 'java', 'bash', "assets/SideWinder.png")
syntax_turtle = Card('Syntax Turtle', 'turtle', 'bash', 'scratch', "assets/SyntaxTurtle.png")
viralmuto = Card('Viralmuto', 'bash', 'python', 'scratch', "assets/ViralMuto.png")
virobotica = Card('Virobotica', 'bash', 'python', 'turtle', "assets/Virobotica.png")
virobots = Card('Virobots', 'bash', 'python', 'turtle', "assets/Virobots.png")
woodchuck_norris = Card('Woodchuck Norris', 'scratch', 'turtle', 'java', "assets/WoodchuckNorris.png")

# Move all of this to Data class in init??? makes more sense logically
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

# default version is that each character gets 3 randomly chosen cards
# challenge version could be that they program choosing their cards? or each gets half the deck
random.shuffle(DECK)

# draw_title_screen()

# Intro Screen - Enter player names
# p1_name, p2_name = draw_name_screen()

# skip intro screen for debugging
p1_name, p2_name = "p1", "p2"

#create player
player_one = Player()
player_one.name = p1_name
# TODO coin toss to determine who goes first, for now set P1 first
player_one.active_turn = True

player_two = Player()
player_two.name = p2_name

# player_one.HAND = DECK[:int(len(DECK)/2)]
# player_two.HAND = DECK[int(len(DECK)/2):]
player_one.HAND = DECK[:3]
player_two.HAND = DECK[3:6]
# TODO add method to add the card objects to player decks for rendering, need new card images first

running = True
turn = 1

# pick cards before game loop? see display_intro_screen() in level 3
# choose_hand()

# Run the game
draw_screen(player_one, player_two)

# Game loop below
while running: 
    clock.tick(60)
    for event in pygame.event.get():
        # Checks to see if player clicked close button on window
        check_stop(event)
        
        # draw/update screen
        # draw_screen()
        coin_button_rect = draw_coin_flip_button()

        # turn for each character:
        # choose attack (safe or risk) - only advanced, "big hit" is default
        # player clicks on attack

        # TODO player can choose which card to be active

        # player clicks on flip coin
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if coin_button_rect.collidepoint(mouse_position):
                offense, defense = get_active_player(turn)
                offense_card = offense.HAND[offense.current_card]
                defense_card = defense.HAND[defense.current_card]

                # add pieces of message together to show in dialog box
                message = ""
                message = add_to_message(message, "{}".format(turn))
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

                if check_game_end():
                    running = False
                    # TODO render some victory graphic?
                    # TODO ask to play again before closing
                turn = turn + 1


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
