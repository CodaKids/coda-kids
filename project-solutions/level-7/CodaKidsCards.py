import pygame
from os import path

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs the image files from your folder.
    return path.join(path.dirname(__file__), fileName)

DECK = []

class Player:
    health = 20
    hand = []

class Card:
    def __init__(self, techtype, weakness, resistance, image_path):
        self.techtype = techtype
        self.weakness = weakness
        self.resistance = resistance
        self.image_path = image_path

annie_conda = Card('python', 'java', 'bash', "assets/AnnieConda.png")
bayo_wolf = Card('scratch', 'turtle', 'java', "assets/BayoWolf.png")
captain_javo = Card('java', 'scratch', 'python', "assets/CaptainJavo.png")



