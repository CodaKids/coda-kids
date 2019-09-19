"""General information on your module and what it does."""
from init import *

# load sprites
IMAGE_GAMEOVER = Image("assets/GameOverBackground.png")
IMAGE_BUTTON = Image("assets/ReplayButton.png")

# modifiable data
class Data:
    """place changable state variables here."""
    gameoverbackground = Object(IMAGE_GAMEOVER)
    restart_button = Object(IMAGE_BUTTON)
    display_text = TextObject(WHITE, 24, "Player 2 wins! Play again?")

MY = Data()

def initialize(window):
    """Initializes the restart menu state."""
    MY.gameoverbackground.location = window / 2
    MY.restart_button.location = window / 2

def update(delta_time):
    """Updates the restart menu state."""
    for event in pygame.event.get():
        if quit_game(event):
            stop()
        if mouse_l_button_down(event):
            if MY.restart_button.collides_with_point(mouse_position()):
                Manager.current = 0

def draw(screen):
    """Draws the restart menu state."""
    MY.gameoverbackground.draw(screen)
    MY.restart_button.draw(screen)
    MY.display_text.draw(screen)
