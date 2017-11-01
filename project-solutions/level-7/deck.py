"""Info on the deck."""
import random

def new():
    """Creates and returns a new deck."""
    return Deck()

class Deck:
    """wrapper deck class around a python list."""

    def __init__(self):
        self._deck = []

    def add_card(self, card):
        """Adds a given card or list of cards to the deck."""
        self._deck.append(card)

    def combine_with(self, cards):
        """adds the given list or deck of cards to the deck."""
        if isinstance(cards, list):
            self._deck = self._deck + cards
            cards = []
        elif isinstance(cards, Deck):
            self._deck = self._deck + cards._deck
        else: #assume its a single card.
            self._deck.append(cards)


    def size(self):
        """Return the number of cards in the deck."""
        return len(self._deck) # returns length of deck

    def draw_card(self):
        """Draw the top most card from the deck."""
        return self._deck.pop() #pops the last item off the list

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self._deck)
