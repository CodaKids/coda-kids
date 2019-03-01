import pygame, sys
import time
from os import path

def getFile(fileName):
    """Returns the absolute path of a file."""
    return path.join(path.dirname(__file__), fileName)

"""Loads the background and images"""
BACKGROUND = pygame.image.load(getFile('assets/ClassroomBackground.png'))
CHARACTER_1 = pygame.image.load(getFile('assets/Character_1.png'))
ANN = pygame.image.load(getFile("assets/Ann.png"))
BEYO = pygame.image.load(getFile("assets/Beyo.png"))
GRAPHICA = pygame.image.load(getFile("assets/Graphica.png"))
IAN_FIB = pygame.image.load(getFile("assets/IanFib.png"))
INTELL = pygame.image.load(getFile("assets/Intell.png"))
JAVA_LIN = pygame.image.load(getFile("assets/JavaLin.png"))
JAVO = pygame.image.load(getFile("assets/Javo.png"))
JITTER = pygame.image.load(getFile("assets/Jitter.png"))
PAUL_PYTHON = pygame.image.load(getFile("assets/PaulPython.png"))
QUACK = pygame.image.load(getFile("assets/Quack.png"))
RAM_ROM = pygame.image.load(getFile("assets/Ram_Rom.png"))
SBT = pygame.image.load(getFile("assets/SBT.png"))
SIDE_WINDER = pygame.image.load(getFile("assets/SideWinderNEw.png"))
SYNTAX = pygame.image.load(getFile("assets/Syntax.png"))

"""Stores character text into variables"""
TEXT_1  = "I am character 1!"
TEXT_2  = "I am character 2!"
TEXT_3  = "I am character 3!"
TEXT_4  = "I am character 4!"
TEXT_5  = "I am character 5!"
TEXT_6  = "I am character 6!"
TEXT_7  = "I am character 7!"
TEXT_8  = "I am character 8!"
TEXT_9  = "I am character 9!"
TEXT_10 = "I am character 10!"
TEXT_11 = "I am character 11!"
TEXT_12 = "I am character 12!"
TEXT_13 = "I am character 13!"
TEXT_14 = "I am character 14!"
TEXT_15 = "I am character 15!"


"""Initialize Font Object"""
pygame.init()
myfont = pygame.font.SysFont(None, 35)

"""We assign our character and text variables"""
character = CHARACTER_1
text = TEXT_1

"""Displays character to the screen"""
WIDTH = 638
HEIGHT = 825
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
running = True

# """solution using if-statements"""
# while running:
#     SCREEN.blit(BACKGROUND,(0,0))
#     SCREEN.blit(character, (0,0))
#     SCREEN.blit(myfont.render(text, True, (255, 0, 0)), (235,250))
#     pygame.display.flip()
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 character = CHARACTER_1
#                 text = TEXT_1 
#             if event.key == pygame.K_2:
#                 character = ANN
#                 text = TEXT_2 
#             if event.key == pygame.K_3:
#                 character = ANN
#                 text = TEXT_3 
#             if event.key == pygame.K_4:
#                 character = ANN
#                 text = TEXT_4 
#             if event.key == pygame.K_5:
#                 character = ANN
#                 text = TEXT_5
#             if event.key == pygame.K_6:
#                 character = ANN
#                 text = TEXT_6
#             if event.key == pygame.K_7:
#                 character = ANN
#                 text = TEXT_7
#             if event.key == pygame.K_8:
#                 character = ANN
#                 text = TEXT_8
#             if event.key == pygame.K_9:
#                 character = ANN
#                 text = TEXT_9
#             if event.key == pygame.K_0:
#                 character = ANN
#                 text = TEXT_10
#             if event.key == pygame.K_q:
#                 running = False
# pygame.quit()

"""solution using an array"""
#initialize arrays
characters = []
texts = []
#add characters and text to arrays
characters.append(CHARACTER_1)
texts.append(TEXT_1)
characters.append(ANN)
texts.append(TEXT_2)
characters.append(BEYO)
texts.append(TEXT_3)
characters.append(GRAPHICA)
texts.append(TEXT_4)
characters.append(IAN_FIB)
texts.append(TEXT_5)
characters.append(INTELL)
texts.append(TEXT_6)
characters.append(JAVA_LIN)
texts.append(TEXT_7)
characters.append(JAVO)
texts.append(TEXT_8)
characters.append(JITTER)
texts.append(TEXT_9)
characters.append(PAUL_PYTHON)
texts.append(TEXT_10)
characters.append(QUACK)
texts.append(TEXT_11)
characters.append(RAM_ROM)
texts.append(TEXT_12)
characters.append(SBT)
texts.append(TEXT_13)
characters.append(SIDE_WINDER)
texts.append(TEXT_14)
characters.append(SYNTAX)
texts.append(TEXT_15)

running = True
#start at the first character in the array
i = 0
while running:
    character = characters[i]
    text = texts[i]
    SCREEN.blit(BACKGROUND,(0,0))
    SCREEN.blit(character, (0,0))
    SCREEN.blit(myfont.render(text, True, (255, 0, 0)), (235,250))
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            #if pressed 1, go to next character
            if event.key == pygame.K_1:
                i = i+1
            #press q to quit
            if event.key == pygame.K_q:
                running = False
    #if we reach the end of the array, start from the beginning again.
    if i == 15:
        i = 0
pygame.quit()
