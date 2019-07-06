"""General information on your module and what it does."""
import coda_kids as coda

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
    for event in coda.event.listing():
        if coda.event.quit_game(event):
            coda.stop()
        elif coda.event.mouse_l_button_down(event):
            if MY.Button.collides_with_point(coda.event.mouse_position()):
                coda.state.change(0)

def draw(screen):
    """Draws the lose menu state."""
    MY.Button.draw(screen)

def cleanup():
    """Cleans up the lose menu state."""
