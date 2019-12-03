"""General information on your module and what it does."""
from init import *
import pygame

import BossFight
Manager.register(BossFight)
Manager.run(SCREEN, WINDOW, BLACK)