"""General information on your module and what it does."""
import coda

#load sprites
BUTTON_IMAGE = coda.Image("assets/LoseButton.png")

class Data:
    Button = coda.Object(BUTTON_IMAGE)

MY = Data()

def initialize(window):
    """Initializes the lose menu state."""
    MY.Button.location = window / 2

def update(delta_time):
    """Updates the lose menu state."""
    for event in coda.listing():
        if coda.quit_game(event):
            coda.stop()
        elif coda.mouse_l_button_down(event):
            if MY.Button.collides_with_point(coda.mouse_position()):
                coda.change(0)

def draw(screen):
    """Draws the lose menu state."""
    MY.Button.draw(screen)

def cleanup():
    """Cleans up the lose menu state."""
