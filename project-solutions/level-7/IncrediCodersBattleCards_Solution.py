import pygame
from os import path


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
cryptic_creeper = Card('bash', 'python', 'turtle', "assets/CrypticCreeper.png")
emily_airheart = Card('turtle', 'bash', 'scratch', "assets/EmilyAirHeart.png")
grafika_turtle = Card('turtle', 'bash', 'scratch', "assets/GrafikaTurtle.png")
intelli_scents = Card('scratch', 'turtle', 'java', "assets/IntelliScents.png")
java_lynn = Card('java', 'scratch', 'python', "assets/JavaLynn.png")
jitter_bug = Card('java', 'scratch', 'python', "assets/JitterBug.png")
justin_timbersnake = Card('python', 'java', 'bash', "assets/JustinTimbersnake.png")
mrs_scratcher = Card('scratch', 'turtle', 'java', "assets/MrsScratcher.png")
paul_python = Card('python', 'java', 'bash', "assets/PaulPython.png")
queen_cobra = Card('python', 'java', 'bash', "assets/QueenCobra.png")
ram_rom = Card('java', 'scratch', 'python', "assets/RAMROM.png")
sidewinder = Card('python', 'java', 'bash', "assets/SideWinder.png")
syntax_turtle = Card('turtle', 'bash', 'scratch', "assets/SyntaxTurtle.png")
viralmuto = Card('bash', 'python', 'scratch', "assets/ViralMuto.png")
virobotica = Card('bash', 'python', 'turtle', "assets/Virobotica.png")
virobots = Card('bash', 'python', 'turtle', "assets/Virobots.png")
woodchuck_norris = Card('scratch', 'turtle', 'java', "assets/WoodchuckNorris.png")
