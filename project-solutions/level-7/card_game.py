"""General information on your module and what it does."""
import coda_kids as coda
import player
import card
import deck

#load sprites constants

#constants

#Game Phase Constants
DRAW_PHASE = 0
PLAY_PHASE = 1
ATTACK_PHASE = 2
RESOLVE_PHASE = 3
GAME_OVER = 4

#Player Init Constants
DEFAULT_HEALTH = 10
DEFAULT_ATTACK = 1
DEFAULT_SHIELD = 0

#Console Constants
CONSOLE_LOCATION = (0, 0)
CONSOLE_LINES = 20
CONSOLE_SIZE = 20

class Data:
    """Modifiable data"""
    player1 = player.Info("Player 1", DEFAULT_HEALTH, DEFAULT_ATTACK, DEFAULT_SHIELD)
    player2 = player.Info("Player 2", DEFAULT_HEALTH, DEFAULT_ATTACK, DEFAULT_SHIELD)
    current_player = player1
    current_phase = DRAW_PHASE
    curent_turn = 0
    test = 0

CONSOLE = coda.utilities.OutputConsole(CONSOLE_LOCATION,
                                       CONSOLE_LINES,
                                       CONSOLE_SIZE,
                                       coda.color.BLACK)
DECK = deck.new()
GRAVEYARD = deck.new()
MY = Data()

def add_inital_deck():
    """Add all initial cards to deck."""
    attack1 = card.new("Baseball Bat", card.IMAGE_DEFAULT, card.effect.Attack(0, 1))
    attack2 = card.new("Sword", card.IMAGE_DEFAULT, card.effect.Attack(0, 2))
    attack3 = card.new("Axe", card.IMAGE_DEFAULT, card.effect.Attack(0, 5))
    damage1 = card.new("Smack", card.IMAGE_DEFAULT, card.effect.Damage(0, 2))
    damage2 = card.new("punch", card.IMAGE_DEFAULT, card.effect.Damage(0, 3))
    damage3 = card.new("Kick", card.IMAGE_DEFAULT, card.effect.Damage(0, 4))
    shield1 = card.new("Wooden Shield", card.IMAGE_DEFAULT, card.effect.Sheild(0, 2))
    shield2 = card.new("Chainmail", card.IMAGE_DEFAULT, card.effect.Sheild(0, 3))
    shield3 = card.new("Half Plate", card.IMAGE_DEFAULT, card.effect.Sheild(0, 4))
    steal = card.new("Pickpocket", card.IMAGE_DEFAULT, card.effect.Steal(0, 0))

    DECK.add_card(attack1.copy()) # attack cards
    DECK.add_card(attack1.copy())
    DECK.add_card(attack1.copy())
    DECK.add_card(attack1.copy())
    DECK.add_card(attack2.copy())
    DECK.add_card(attack2.copy())
    DECK.add_card(attack2.copy())
    DECK.add_card(attack2.copy())
    DECK.add_card(attack3.copy()) # more powerful cards are rarer
    DECK.add_card(attack3.copy())

    DECK.add_card(damage1.copy()) # damage cards
    DECK.add_card(damage1.copy())
    DECK.add_card(damage1.copy())
    DECK.add_card(damage1.copy())
    DECK.add_card(damage2.copy())
    DECK.add_card(damage2.copy())
    DECK.add_card(damage2.copy())
    DECK.add_card(damage2.copy())
    DECK.add_card(damage3.copy())
    DECK.add_card(damage3.copy())

    DECK.add_card(shield1.copy()) # sheild cards
    DECK.add_card(shield1.copy())
    DECK.add_card(shield1.copy())
    DECK.add_card(shield1.copy())
    DECK.add_card(shield2.copy())
    DECK.add_card(shield2.copy())
    DECK.add_card(shield2.copy())
    DECK.add_card(shield2.copy())
    DECK.add_card(shield3.copy())
    DECK.add_card(shield3.copy())

    DECK.add_card(steal.copy()) # Add a bunch of steal cards
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())
    DECK.add_card(steal.copy())

def init_deck():
    """Initialize the deck."""
    DECK.combine_with(GRAVEYARD)
    DECK.combine_with(MY.player1.hand)
    DECK.combine_with(MY.player2.hand)

    if DECK.size() == 0: # first time use, add cards to deck.
        add_inital_deck()

    DECK.shuffle()

def get_enemy_player():
    """Gets the enemy player based on the current player."""
    if MY.current_player == MY.player1:
        return MY.player2
    return MY.player1

def resolve_turn():
    """Resolve enemy turn"""
    num = coda.utilities.rand(0, len(MY.player2.hand) - 1)
    MY.player2.play_card(MY.player1, MY.player2.hand[num], CONSOLE)
    MY.player2.hand.remove(MY.player2.hand[num])

def initialize(window):
    """Initializes the Introduction class."""
    init_deck()
    MY.player1.hand.append(DECK.draw_card())
    MY.player2.hand.append(DECK.draw_card())
    MY.player1.hand.append(DECK.draw_card())
    MY.player2.hand.append(DECK.draw_card())
    MY.player1.hand.append(DECK.draw_card())
    MY.player2.hand.append(DECK.draw_card())

def update(delta_time):
    """Update method for boss battle state."""
    enemy_player = get_enemy_player()

    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.key_down(event, 'a'):
            MY.test += 1
            CONSOLE.write(str(MY.test))
        elif (coda.event.mouse_l_button_down(event) and
              MY.current_phase == PLAY_PHASE and
              MY.current_player == MY.player1):
            for item in MY.player1.hand:
                if item.object.collides_with_point(coda.event.mouse_position()):
                    MY.current_player.play_card(enemy_player, item, CONSOLE)
                    MY.player1.hand.remove(item)
                    MY.current_phase += 1
                    break

    for item in MY.player1.hand:
        if item.object.collides_with_point(coda.event.mouse_position()):
            coda.actions.clear(item.object)
            coda.actions.add(item.object, "scale", 1.2, 0.2)
        else:
            coda.actions.clear(item.object)
            coda.actions.add(item.object, "scale", 1, 0.2)

    if MY.current_phase == DRAW_PHASE:
        MY.current_player.hand.append(DECK.draw_card())
        MY.current_phase += 1
        CONSOLE.write(MY.current_player.name + " has drawn a card")
    elif MY.current_phase == PLAY_PHASE and MY.current_player == MY.player2:
        resolve_turn()
        MY.current_phase += 1
    elif MY.current_phase == ATTACK_PHASE:
        enemy_player.health.base -= MY.current_player.attack.value()
        MY.current_phase += 1
        CONSOLE.write(MY.current_player.name + " dealt " + str(MY.current_player.attack.value()) + " to " + get_enemy_player().name)
    elif MY.current_phase == RESOLVE_PHASE:
        if MY.current_player.health.value() <= 0:
            CONSOLE.write(enemy_player.name + " has won the game!")
            MY.current_phase = GAME_OVER
            return
        elif enemy_player.health.value() <= 0:
            CONSOLE.write(MY.current_player.name + " has won the game!")
            MY.current_phase = GAME_OVER
            return

        MY.current_player.remove_expired_effects(MY.curent_turn, enemy_player)
        enemy_player.remove_expired_effects(MY.curent_turn, MY.current_player)
        MY.current_player = enemy_player
        MY.current_phase = DRAW_PHASE
        MY.curent_turn += 1
        CONSOLE.write("It is now " + MY.current_player.name + "'s turn")

def draw(screen):
    """Draws the state to the given screen."""
    MY.player1.draw(coda.Vector2(800, 700), screen, True)
    MY.player2.draw(coda.Vector2(800, 100), screen, False)
    CONSOLE.draw(screen)

def cleanup():
    """Cleans up the Intro State."""
