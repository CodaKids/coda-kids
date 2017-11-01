"""This file is used to set up and register the state machine."""
import coda_kids as coda

# global data
WINDOW = coda.Vector2(800, 608)
SCREEN = coda.start(WINDOW, "Demo Project 4")

# states
import platformer
coda.state.Manager.register(platformer)
import lose
coda.state.Manager.register(lose)
import win
coda.state.Manager.register(win)

# run the game!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLUE)
  