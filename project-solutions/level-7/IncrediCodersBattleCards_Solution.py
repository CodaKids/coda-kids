from init import *
import random

DECK = []

class Player:
    def __init__(self):
        self.HAND = []

class Card:
    def __init__(self, techtype, weakness, resistance, image_path):
        self.techtype = techtype
        self.weakness = weakness
        self.resistance = resistance
        self.image_path = image_path
        self.HP = 15
    
    #def attack1():
        #something here that's implemented in init file
    
    #def attack2():
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

#create player
player_one = Player()
player_two = Player()

#add all cards to deck
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

#deal half of the cards to each player, randomly
random.shuffle(DECK)
player_one.HAND = DECK[:int(len(DECK)/2)]
player_two.HAND = DECK[int(len(DECK)/2):]

turn = 1

#Player flips coin to see who goes first

import IncrediCodersBattleCards_Solution
Manager.register(IncrediCodersBattleCards_Solution)

# Run the game
Manager.run(SCREEN, WINDOW, BLACK)


#running = True
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