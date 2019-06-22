"""This file is used to set up and register the state machine."""
import coda_kids as coda

# setup
WINDOW = coda.Vector2(900, 600)
SCREEN = coda.start(WINDOW, "Space Wars Tournament")

# states
import shooter
coda.state.Manager.register(shooter)
import restarter1
coda.state.Manager.register(restarter1)
import restarter2
coda.state.Manager.register(restarter2)

# run the game!
coda.state.Manager.run(SCREEN, WINDOW, coda.color.BLACK)

  