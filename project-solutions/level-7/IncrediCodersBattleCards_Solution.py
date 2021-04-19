from init import *
import random

def flip_coin():
    return "Heads" if random.randint(0,1) == 1 else "Tails"

def get_active_player(turn):
    if player_one.active_turn == True:
        return player_one, player_two  
    else:
        return player_two, player_one

def switch_active_player(offense, defense):
    offense.active_turn = False
    defense.active_turn = True

def check_game_end():
    # check status of both players, if one player surviving then end the game
    if player_one.active == False:
        exiting = victory(player_two)
        if not exiting:
            reset_game(player_one, player_two)
        return exiting
    elif player_two.active == False:
        exiting = victory(player_one)
        if not exiting:
            reset_game(player_one, player_two)
        return exiting
    return False

def add_to_message(msg, text_add):
    text = textwrap.wrap(text_add, 30)
    for line in text:
        msg += line + "\n"
    return msg
    
def check_cards(player):
    if not player.HAND[player.current_card].alive:
        player.current_card += 1
    if player.current_card > 2: # TODO need to update this logic for other scenarios
        player.active = False

def reset_game(p1, p2):
    # Reset cards
    reset_cards()

    # reshuffle deck
    # default version is that each character gets 3 randomly chosen cards
    # challenge version could be that they program choosing their cards? or each gets half the deck
    random.shuffle(MY.DECK)
    # Deal cards to players
    p1.HAND = MY.DECK[:3]
    p2.HAND = MY.DECK[3:6]

    # Reset turn
    MY.TURN = 0

    # Reset players
    p1.active = True
    p1.active_turn = False
    p2.active = True
    p2.active_turn = False

    # Turn Coin Flip screen - flip a coin to see who goes first
    active = draw_turn_flip_screen(p1.name, p2.name)
    if active == p1_name:
        p1.active_turn = True
    elif active == p2_name:
        p2.active_turn = True
    
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

# TODO add method to add the card objects to player decks for rendering, need new card images first

running = True

# pick cards before game loop? see display_intro_screen() in level 3
# choose_hand()


# Game loop below
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
                
                offense, defense = get_active_player(MY.TURN)
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

                # Switch active player
                switch_active_player(offense, defense)

                if check_game_end():
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
