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

    # def primary_attack(): # attack from init
    #def attack2():
        #something here also that's implemented in init file

#Creating all the Cards
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

#Adding all the Cards to DECK
DECK.append(annie_conda)
DECK.append(bayo_wolf)
DECK.append(captain_javo)
DECK.append(cryptic_creeper)
DECK.append(emily_airheart)
DECK.append(grafika_turtle)
DECK.append(intelli_scents)
DECK.append(java_lynn)
DECK.append(jitter_bug)
DECK.append(justin_timbersnake)
DECK.append(mrs_scratcher)
DECK.append(paul_python)
DECK.append(queen_cobra)
DECK.append(ram_rom)
DECK.append(sidewinder)
DECK.append(syntax_turtle)
DECK.append(viralmuto)
DECK.append(virobotica)
DECK.append(virobots)
DECK.append(woodchuck_norris)

#Game loop below:
#while running: 
    #If turn one, Player1 and 2 pick their starting card. It is shown to each 
    # other. Then, coin toss to establish who get's to go first. 
    #Next, player picks an attack from one card
    #Player then picks card they would like to attack.
    #Player flips coin
    #Depending on results of coin, damage is dealt to that card.
    #TODO: implement specific attacks based on the cards
    #If card health < 1, card is killed
    #If player has no cards left, player loses
    #Change player turn to the other player