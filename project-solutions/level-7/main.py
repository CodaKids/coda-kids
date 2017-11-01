"""This file is used to set up and register the state machine. Always run the project from here!"""

import coda_kids as coda

# global data
WINDOW = coda.Vector2(1600, 800)
SCREEN = coda.start(WINDOW, "Demo Project 7")

# states
import card_game
coda.state.Manager.register(card_game)

# run the game!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLUE)
