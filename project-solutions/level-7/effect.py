"""Module containing information on card effects and how they work."""
import enum
import copy
import random

class Type(enum.Enum):
    """Card effect type enum."""
    Nothing = 0, """ Enum for Nothing effect."""
    Attack = 1, """ Enum for Attack effect."""
    Damage = 2, """ Enum for Damage effect."""
    Shield = 3, """ Enum for Shield effect."""
    Dodge = 4, """ Enum for dodge chance effect."""
    Steal = 5, """ Enum for steal card effect."""

class Duration(enum.Enum):
    """Card effect duration enum."""
    Instant = 0, """Enum for card effects that happen instantly."""
    Single_Turn = 1, """Enum for card effects that occur over a whole turn."""
    Permanent = 2, """Enum for card effects last forever."""

class Base:
    """Card effect base class. To create a new type create a subclass with all of these methods."""
    def __init__(self, effect_type, duration_type, turn_created, value):
        """Initializer for card creation."""
        self.type = effect_type
        self.duration = duration_type
        self.turn_created = turn_created
        self.value = value

    def description(self):
        """Get's the description of the card as a string."""
        print("Default description function called on Effect base class. with effect type: " + type)
        return "ERROR TYPE"

    def play(self, owner_player, enemy_player):
        """Add the effect to the given player."""
        print("Warning: play function for effect " + self.type + "Not set.")
        return

    def remove_from_play(self, owner_player, enemy_player):
        """Remove the effect from the given player."""
        print("Warning: remove_from_play function for effect " + self.type + "Not set.")
        return

    def should_be_removed(self, current_turn):
        """Check if the effect should be removed."""
        if self.duration == Duration.Instant:
            return True
        elif self.duration == Duration.Permanent:
            return False

        return not self.turn_created == current_turn

    def copy(self):
        """Creates a fresh copy of the card effect."""
        return copy.deepcopy(self)


class Attack(Base):
    """Attack Effect."""
    def __init__(self, turn_created, value):
        """Attack effect initializer"""
        super(Attack, self).__init__(Type.Attack,
                                     Duration.Single_Turn,
                                     turn_created, value)

    def description(self):
        """Get's the description of the attack effect."""
        return "Adds  " + str(self.value) + " attack until next turn."

    def play(self, owner_player, enemy_player):
        """Add Attack."""
        owner_player.attack.modified += self.value
        return

    def remove_from_play(self, owner_player, enemy_player):
        """Remove Attack."""
        owner_player.attack.modified -= self.value
        return

class Damage(Base):
    """Damage Effect."""
    def __init__(self, turn_created, value):
        """Damage effect initializer"""
        super(Damage, self).__init__(Type.Damage,
                                     Duration.Instant,
                                     turn_created, value)

    def description(self):
        """Get's the description of the damage effect."""
        return "Deals " + str(self.value) + " damage."

    def play(self, owner_player, enemy_player):
        """Deals damge"""
        enemy_player.health.base -= self.value
        return

    def remove_from_play(self, owner_player, enemy_player):
        """Do Nothing."""
        return

class Sheild(Base):
    """Sheild Effect."""
    def __init__(self, turn_created, value):
        """Damage effect initializer"""
        super(Sheild, self).__init__(Type.Shield,
                                     Duration.Permanent,
                                     turn_created, value)

    def description(self):
        """Get's the description of the sheild effect."""
        return "Adds " + str(self.value) + " sheild."

    def play(self, owner_player, enemy_player):
        """Adds sheild"""
        owner_player.shield.modified += self.value
        return

    def remove_from_play(self, owner_player, enemy_player):
        """Do Nothing."""
        owner_player.shield.modified -= self.value
        return

class Steal(Base):
    """Sheild Effect."""
    def __init__(self, turn_created, value):
        """Steal effect initializer"""
        super(Steal, self).__init__(Type.Steal,
                                    Duration.Instant,
                                    turn_created, value)

    def description(self):
        """Get's the description of the steal effect."""
        return "Steals a card at random."

    def play(self, owner_player, enemy_player):
        """steal card."""
        size = len(enemy_player.hand) - 1
        owner_player.hand.append(enemy_player.hand.pop(random.randint(0, size)))
        return

    def remove_from_play(self, owner_player, enemy_player):
        """Do Nothing."""
        return
