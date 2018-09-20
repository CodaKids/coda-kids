"""This file is used to set up and register the state machine."""
import coda_kids as coda

# setup
WINDOW = coda.Vector2(632, 825)
SCREEN = coda.start(WINDOW, "Demo Project 3")

# states
import introduction
coda.state.Manager.register(introduction)

coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLACK)

  