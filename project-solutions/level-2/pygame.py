import pygame
from os import path

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs your files from your folder.
    return path.join(path.dirname(__file__), fileName)

"""Loads the background and images"""
background = pygame.image.load(get_file('assets/ClassroomBackground.png'))
ann = pygame.image.load(get_file("assets/Ann.png"))
beyo = pygame.image.load(get_file("assets/Beyo.png"))
graphica = pygame.image.load(get_file("assets/Graphica.png"))
ian_fib = pygame.image.load(get_file("assets/IanFib.png"))
intell = pygame.image.load(get_file("assets/Intell.png"))
java_lin = pygame.image.load(get_file("assets/JavaLin.png"))
javo = pygame.image.load(get_file("assets/Javo.png"))
jitter = pygame.image.load(get_file("assets/Jitter.png"))
paul_python = pygame.image.load(get_file("assets/PaulPython.png"))
quack = pygame.image.load(get_file("assets/Quack.png"))
ram_rom = pygame.image.load(get_file("assets/Ram_Rom.png"))
sbt = pygame.image.load(get_file("assets/SBT.png"))
side_winder = pygame.image.load(get_file("assets/SideWinder.png"))
syntax = pygame.image.load(get_file("assets/Syntax.png"))

"""Stores character text into variables"""
text_ann  = "I am character 1!"
text_beyo  = "I am character 2!"
text_graphica  = "I am character 3!"
text_ian_fib  = "I am character 4!"
text_intell  = "I am character 5!"
text_java_lin  = "I am character 6!"
text_javo  = "I am character 7!"
text_jitter  = "I am character 8!"
text_paul_python  = "I am character 9!"
text_quack = "I am character 10!"
text_ram_rom = "I am character 11!"
text_sbt = "I am character 12!"
text_side_winder = "I am character 13!"
text_syntax = "I am character 14!"

"""Initialize Font Object"""
pygame.init()
myfont = pygame.font.SysFont(None, 35)

"""We assign our character and text variables"""
current_character = ann
current_text = text_ann

"""Displays character to the screen"""
width = 638
height = 825
screen = pygame.display.set_mode((width,height))
running = True

# """solution using if-statements"""
# while running:
#     screen.blit(background,(0,0))
#     screen.blit(current_character, (0,0))
#     screen.blit(myfont.render(current_text, True, (255, 0, 0)), (235,250))
#     pygame.display.flip()
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_1:
#                 character = ann
#                 text = text_ann
#             if event.key == pygame.K_2:
#                 character = beyo
#                 text = text_beyo 
#             if event.key == pygame.K_3:
#                 character = graphica
#                 text = text_graphica 
#             if event.key == pygame.K_4:
#                 character = ian_fib
#                 text = text_ian_fib 
#             if event.key == pygame.K_5:
#                 character = intell
#                 text = text_intell
#             if event.key == pygame.K_6:
#                 character = java_lin
#                 text = text_java_lin
#             if event.key == pygame.K_7:
#                 character = javo
#                 text = text_javo
#             if event.key == pygame.K_8:
#                 character = jitter
#                 text = text_jitter
#             if event.key == pygame.K_9:
#                 character = paul_python
#                 text = text_paul_python
#             if event.key == pygame.K_0:
#                 character = quack
#                 text = text_quack
#             if event.key == pygame.K_q:
#                 running = False
# pygame.quit()

"""solution using an array"""
#initialize arrays
CHARACTERS = []
TEXT = []
#add characters and text to arrays
CHARACTERS.append(ann)
TEXT.append(text_ann)
CHARACTERS.append(beyo)
TEXT.append(text_beyo)
CHARACTERS.append(graphica)
TEXT.append(text_graphica)
CHARACTERS.append(ian_fib)
TEXT.append(text_ian_fib)
CHARACTERS.append(intell)
TEXT.append(text_intell)
CHARACTERS.append(java_lin)
TEXT.append(text_java_lin)
CHARACTERS.append(javo)
TEXT.append(text_javo)
CHARACTERS.append(jitter)
TEXT.append(text_jitter)
CHARACTERS.append(paul_python)
TEXT.append(text_paul_python)
CHARACTERS.append(quack)
TEXT.append(text_quack)
CHARACTERS.append(ram_rom)
TEXT.append(text_ram_rom)
CHARACTERS.append(sbt)
TEXT.append(text_sbt)
CHARACTERS.append(side_winder)
TEXT.append(text_side_winder)
CHARACTERS.append(syntax)
TEXT.append(text_syntax)

running = True
#start at the first character in the array
i = 0
while running:
    current_character = CHARACTERS[i]
    current_text = TEXT[i]
    screen.blit(background,(0,0))
    screen.blit(current_character, (0,0))
    screen.blit(myfont.render(current_text, True, (255, 0, 0)), (235,250))
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
    if i == 1:
        i = 0
pygame.quit()
