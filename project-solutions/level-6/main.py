"""This file is used to set up and register the state machine. Always run the project from here!"""
import coda_kids as coda

# global data
WINDOW = coda.Vector2(800, 608)
SCREEN = coda.start(WINDOW, "Demo Project 5")

# states
import boss_fight
coda.state.Manager.register(boss_fight)

# run the game!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLACK)
  