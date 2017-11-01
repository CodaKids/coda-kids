"""This file is used to set up and register the state machine."""
import coda_kids as coda

# setup
WINDOW = coda.Vector2(800, 608)
SCREEN = coda.start(WINDOW, "Demo Project 2")

# states
import quiz
coda.state.Manager.register(quiz)

# main game loop!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLACK)
  