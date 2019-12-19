"""General information on your module and what it does."""
from init import *
import pygame

import BossBattle
Manager.register(BossBattle)
Manager.run(SCREEN, WINDOW, BLACK)