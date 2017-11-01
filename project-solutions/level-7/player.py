"""Module containing information on players and how they work."""
import coda_kids as coda
import card

HAND_OFFSET = 10

class Stat:
    """Modifiable stat used by player."""
    def __init__(self, base_value, modified_value):
        """Default constructor."""
        self.base = base_value
        self.modified = modified_value

    def value(self):
        """ Get actual stat value."""
        return self.base + self.modified

    def subtract(self, value):
        """Subtract value from total value, prioritizing mod value."""
        mod = max(0, self.modified - value)
        val = self.value
        if mod == 0:
            val = self.base - abs(self.modified - value)
        self.base = max(0, val)
        self.modified = mod


class Info:
    """Player Container Class."""
    def __init__(self, name, health, attack, shield):
        """Default constructor for player class."""
        self.name = name
        self.health = Stat(health, 0)
        self.attack = Stat(attack, 0)
        self.shield = Stat(shield, 0)
        self.hand = []
        self.effects = []
        self.health_text = coda.TextObject(coda.color.BLACK,
                                           15,
                                           "Health: " + str(self.health.value()))
        self.attack_text = coda.TextObject(coda.color.BLACK,
                                           15,
                                           "Attack: " + str(self.attack.value()))
        self.shield_text = coda.TextObject(coda.color.BLACK,
                                           15,
                                           "shield: " + str(self.shield.value()))

    def start_turn(self, enemy_player, current_turn):
        """Starts the players turn."""
        self.remove_expired_effects(enemy_player, current_turn)

    def end_turn(self, enemy_player, current_turn):
        """End's the players turn."""
        self.remove_expired_effects(enemy_player, current_turn)

    def play_card(self, enemy_player, card_to_play, console=None):
        """Play the given card for the given player."""
        ret = card_to_play.effect.copy()
        if console != None:
            console.write(self.name + " played " + card_to_play.name_text.text)
        ret.play(self, enemy_player)
        self.effects.append(ret)

    def remove_expired_effects(self, enemy_player, current_turn):
        """Cleans all expired effects off the player."""
        for card_effect in self.effects:
            if card_effect.should_be_removed(current_turn):
                card_effect.remove_from_play(self, enemy_player)
                self.effects.remove(card_effect)

    def clear_hand(self):
        """Clears the player hand."""
        self.hand.clear()

    def alive(self):
        """Check if player is alive."""
        return self.health.value() > 0

    def draw(self, location, screen, can_see=True):
        """Draws the player onto the screen."""
        loc = coda.Vector2(location[0], location[1])
        num_cards = len(self.hand)
        num_offsets = num_cards - 1
        length = num_cards * 160 + num_offsets * HAND_OFFSET
        start_loc = coda.Vector2(loc.x - length / 2 + card.WIDTH / 2, loc.y)
        jump = coda.Vector2(card.WIDTH + HAND_OFFSET, 0)
        self.health_text.text = "Health: " + str(self.health.value())
        self.health_text.location = (start_loc.x - card.WIDTH, start_loc.y + 30)
        self.attack_text.text = "Attack: " + str(self.attack.value())
        self.attack_text.location = (start_loc.x - card.WIDTH, start_loc.y)
        self.shield_text.text = "Shield: " + str(self.shield.value())
        self.shield_text.location = (start_loc.x - card.WIDTH, start_loc.y - 30)

        for cards in self.hand:
            cards.location = start_loc
            cards.draw(screen, can_see)
            start_loc += jump

        self.health_text.draw(screen)
        self.attack_text.draw(screen)
        self.shield_text.draw(screen)
