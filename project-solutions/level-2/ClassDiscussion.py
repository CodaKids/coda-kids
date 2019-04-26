import pygame #Gives us our gaming functions
from os import path

"""Initialize Font Object"""
#We pick our text style and size.
pygame.init()
myfont = pygame.font.SysFont('Arial', 20)

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs your files from your folder.
    return path.join(path.dirname(__file__), fileName)

"""Loads the background and images"""
background = pygame.image.load(get_file('assets/Background.png'))
annie_conda = pygame.image.load(get_file("assets/Annie.png"))
bayo_wolf = pygame.image.load(get_file("assets/Bayo.png"))
grafika_turtle = pygame.image.load(get_file("assets/Grafika.png"))
amphib_ian = pygame.image.load(get_file("assets/Ian.png"))
intelli_scents = pygame.image.load(get_file("assets/Intelli.png"))
java_lynn = pygame.image.load(get_file("assets/Java.png"))
captain_javo = pygame.image.load(get_file("assets/Javo.png"))
jitter_bug = pygame.image.load(get_file("assets/Jitter.png"))
paul_python = pygame.image.load(get_file("assets/Paul.png"))
quackintosh = pygame.image.load(get_file("assets/Quack.png"))
ram_rom = pygame.image.load(get_file("assets/RamRom.png"))
sb_turtle = pygame.image.load(get_file("assets/SBTurtle.png"))
sidewinder = pygame.image.load(get_file("assets/Sidewinder.png"))
syntax_turtle = pygame.image.load(get_file("assets/Syntax.png"))

"""Stores character text into variables"""
text_annie_conda  = "I am Annie Conda!"
text_bayo_wolf  = "I am Bayo Wolf!"
text_grafika_turtle  = "I am Grafika Turtle!"
text_amphib_ian  = "I am Amphib Ian!"
text_intelli_scents  = "I am Intelli-Scents!"
text_java_lynn  = "I am Java Lynn!"
text_captain_javo  = "I am Captain Javo!"
text_jitter_bug  = "I am Jitter Bug!"
text_paul_python  = "I am Paul Python!"
text_quackintosh = "I am Quackintosh!"
text_ram_rom = "We are RAM & ROM!"
text_sb_turtle = "I am SB Turtle!"
text_sidewinder = "I am SideWinder!"
text_syntax_turtle = "I am Syntax Turtle!"

"""We assign our character and text variables"""
#current_character = annie_conda
#current_text = text_annie_conda

"""Displays character to the screen"""
width = 600
height = 800
screen = pygame.display.set_mode((width,height))
running = True

"""
#solution using if-statements
while running:
    screen.blit(background,(0,0))
    screen.blit(current_character, (0,0))
    screen.blit(myfont.render(current_text, True, (255, 0, 0)), (235,250))
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_character = annie_conda
                current_text = text_annie_conda
            if event.key == pygame.K_2:
                current_character = bayo_wolf
                current_text = text_bayo_wolf
            if event.key == pygame.K_3:
                current_character = grafika_turtle
                current_text = text_grafika
            if event.key == pygame.K_4:
                current_character = amphib_ian
                current_text = text_amphib_ian 
            if event.key == pygame.K_5:
                current_character = intelli_scents
                current_text = text_intelli_scents
            if event.key == pygame.K_6:
                current_character = java_lynn
                current_text = text_java_lynn
            if event.key == pygame.K_7:
                current_character = captain_javo
                current_text = text_captain_javo
            if event.key == pygame.K_8:
                current_character = jitter_bug
                current_text = text_jitter_bug
            if event.key == pygame.K_9:
                current_character = paul_python
                current_text = text_paul_python
            if event.key == pygame.K_0:
                current_character = quackintosh
                current_text = text_quackintosh
            if event.key == pygame.K_q:
                running = False
pygame.quit()"""

"""solution using an array"""
#initialize arrays
CHARACTERS = []
TEXT = []
#add characters and text to arrays
CHARACTERS.append(annie_conda)
TEXT.append(text_annie_conda)
CHARACTERS.append(bayo_wolf)
TEXT.append(text_bayo_wolf)
CHARACTERS.append(grafika_turtle)
TEXT.append(text_grafika_turtle)
CHARACTERS.append(amphib_ian)
TEXT.append(text_amphib_ian)
CHARACTERS.append(intelli_scents)
TEXT.append(text_intelli_scents)
CHARACTERS.append(java_lynn)
TEXT.append(text_java_lynn)
CHARACTERS.append(captain_javo)
TEXT.append(text_captain_javo)
CHARACTERS.append(jitter_bug)
TEXT.append(text_jitter_bug)
CHARACTERS.append(paul_python)
TEXT.append(text_paul_python)
CHARACTERS.append(quackintosh)
TEXT.append(text_quackintosh)
CHARACTERS.append(ram_rom)
TEXT.append(text_ram_rom)
CHARACTERS.append(sb_turtle)
TEXT.append(text_sb_turtle)
CHARACTERS.append(sidewinder)
TEXT.append(text_sidewinder)
CHARACTERS.append(syntax_turtle)
TEXT.append(text_syntax_turtle)

running = True
#start at the first character in the array
i = 0
while running:
    current_character = CHARACTERS[i]
    current_text = TEXT[i]
    screen.blit(background,(0,0))
    screen.blit(current_character, (0,0))
    screen.blit(myfont.render(current_text, True, (0, 0, 0)), (235,250))
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            #if pressed 1, go to next character
            if event.key == pygame.K_RIGHT:
                i = i+1
            #press q to quit
            if event.key == pygame.K_q:
                running = False
    #if we reach the end of the array, start from the beginning again.
    if i == 14:
        i = 0
pygame.quit()
