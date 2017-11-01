"""Module for describing a card and how it works."""
import coda_kids as coda
import effect

#constants
IMAGE_DEFAULT = coda.Image("card.png")
IMAGE_BACK = coda.Image("card_back.png")

FONT_SIZE = 12
WIDTH = 160
HEIGHT = 160

def new(name, sprite=IMAGE_DEFAULT, card_effect=effect.Base(effect.Type.Nothing,
                                                            effect.Duration.Instant,
                                                            -1,
                                                            0)):
    """Creates a new card with the given name, sprite, and effect."""
    return Card(name, sprite, card_effect)

class Card:
    """Individual Card class."""
    def __init__(self, name, sprite, card_effect):
        """Initializer for cards"""
        self.name_text = coda.TextObject(coda.color.BLACK, FONT_SIZE, name)
        self.front_sprite = sprite
        self.desc_text = coda.TextObject(coda.color.BLACK,
                                         FONT_SIZE,
                                         card_effect.description())
        self.desc_text.centered = True
        self.object = coda.Object(sprite)
        self.effect = card_effect
        self.location = coda.Vector2(0, 0)

    def copy(self):
        """Makes a copy of the card."""
        return Card(self.name_text.text, self.front_sprite, self.effect.copy())

    def draw(self, screen, show_front=True):
        """Draw's the card onto the screen."""
        # first update positions.
        self.object.location = self.location
        if show_front is True:
            self.object.sprite = self.front_sprite
            loc_x = self.location.x
            loc_y = self.location.y
            self.name_text.location = (loc_x - WIDTH / 2 * self.object.scale,
                                       loc_y - HEIGHT / 2 * self.object.scale)
            self.name_text.font_size = FONT_SIZE * self.object.scale
            self.desc_text.location = (loc_x, loc_y - 2)
            self.desc_text.font_size = FONT_SIZE * self.object.scale
            self.object.draw(screen)
            self.name_text.draw(screen)
            self.desc_text.draw(screen)
        else:
            self.object.sprite = IMAGE_BACK
            self.object.draw(screen)
