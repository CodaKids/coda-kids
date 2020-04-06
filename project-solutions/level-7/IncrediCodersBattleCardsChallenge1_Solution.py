import pygame
from os import path


DECK = []

class Player:
    hand = []

class Card:
    def __init__(self, techtype, weakness, resistance, image_path):
        self.techtype = techtype
        self.weakness = weakness
        self.resistance = resistance
        self.image_path = image_path
        self.HP = 5
    
    def attack1():
        #something here that's implemented in init file
    
    def attack2():
        #something here also that's implemented in init file

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

#add all cards to deck
#deal half of the cards to each player, randomly
#initialize Player1 and Player2 (is this a computer?) with 0 cards each
#turn = Player1's turn

#Game loop below:
#while running: 
    #if less than 3 cards, player may draw a card
    #Next, player picks an attack from one card
    #Player then picks card they would like to attack. 
    #Player flips coin
    #Depending on results of coin, damage is dealt to that card.
    #TODO: implement specific attacks based on the cards
    #If card health < 1, card is killed
    #If player has no cards left, player loses
    #Change player turn to the other player