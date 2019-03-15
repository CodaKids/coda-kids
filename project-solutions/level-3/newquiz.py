import pygame
import random
from os import path

def getFile(fileName):
    """Returns the absolute path of a file."""
    return path.join(path.dirname(__file__), fileName)

def randomize_answers(answerChoices):
    random.shuffle(answerChoices)
    return answerChoices

# Load Sprites
IMAGE_BUTTON = pygame.image.load(getFile('Button.png'))
BACKGROUND = pygame.image.load(getFile('ClassroomBackground.png'))

# Read file into an array
TRIVIA = []
file = open(getFile('trivia.txt'), 'r')
for line in file:
    TRIVIA.append(line.rstrip())

#We now have an array that holds our questions, 
#correct answers, and wrong answers, in that order. Let's 
#create a variable for each of those characters to print
#to the screen.
question = TRIVIA[0]
answer = TRIVIA[1]
wrongchoice1 = TRIVIA[2]
wrongchoice2 = TRIVIA[3]

answerChoices = [answer, wrongchoice1, wrongchoice2]

#TODO: need to print to screen
"""Initialize Font Object"""
pygame.init()
myfont = pygame.font.SysFont(None, 35)

"""Displays background to the screen"""
WIDTH = 638
HEIGHT = 825
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
running = True
#TODO: function that registers clicks

i = 0
numberOfQuestions = 3
questionsAnswered = 0
while running:
    SCREEN.blit(BACKGROUND, (0,0))
    questionText = myfont.render(question, True, (255, 0, 0))
    questionRect = questionText.get_rect(topleft=(250,250))
    answer1Text = myfont.render(answerChoices[0], True, (255, 0, 0))
    answer1Rect = answer1Text.get_rect(topleft=(250,300))
    answer2Text = myfont.render(answerChoices[1], True, (255, 0, 0))
    answer2Rect = answer2Text.get_rect(topleft=(250,350))
    answer3Text = myfont.render(answerChoices[2], True, (255, 0, 0))
    answer3Rect = answer3Text.get_rect(topleft=(250,400))
    SCREEN.blit(questionText, questionRect)
    SCREEN.blit(answer1Text, answer1Rect)
    SCREEN.blit(answer2Text, answer2Rect)
    SCREEN.blit(answer3Text, answer3Rect)
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        mpos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if answer1Rect.collidepoint(mpos):
                if answerChoices[0] == answer:
                    print("Nice work! :)")
                    if i >= (numberOfQuestions * 4)-4:
                        running = False
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrongchoice1 = TRIVIA[i+2]
                        wrongchoice2 = TRIVIA[i+3]
                        answerChoices = [answer, wrongchoice1, wrongchoice2]
                        randomize_answers(answerChoices)
                else:
                    print("Not exactly... :(")
                    if i >= (numberOfQuestions * 4)-4:
                        running = False
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrongchoice1 = TRIVIA[i+2]
                        wrongchoice2 = TRIVIA[i+3]
                        answerChoices = [answer, wrongchoice1, wrongchoice2]
                        randomize_answers(answerChoices)
            if answer2Rect.collidepoint(mpos):
                if answerChoices[1] == answer:
                    print("Nice work! :)")
                    if i >= (numberOfQuestions * 4)-4:
                        running = False
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrongchoice1 = TRIVIA[i+2]
                        wrongchoice2 = TRIVIA[i+3]
                        answerChoices = [answer, wrongchoice1, wrongchoice2]
                        randomize_answers(answerChoices)
                else:
                    print("Not exactly... :(")
                    if i >= (numberOfQuestions * 4)-4:
                        running = False
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrongchoice1 = TRIVIA[i+2]
                        wrongchoice2 = TRIVIA[i+3]
                        answerChoices = [answer, wrongchoice1, wrongchoice2]
                        randomize_answers(answerChoices)
            if answer3Rect.collidepoint(mpos):
                if answerChoices[2] == answer:
                    print("Nice work! :)")
                    if i >= (numberOfQuestions * 4)-4:
                        running = False
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrongchoice1 = TRIVIA[i+2]
                        wrongchoice2 = TRIVIA[i+3]
                        answerChoices = [answer, wrongchoice1, wrongchoice2]
                        randomize_answers(answerChoices)
                else:
                    print("Not exactly... :(")
                    if i >= (numberOfQuestions * 4)-4:
                        running = False
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrongchoice1 = TRIVIA[i+2]
                        wrongchoice2 = TRIVIA[i+3]
                        answerChoices = [answer, wrongchoice1, wrongchoice2]
                        randomize_answers(answerChoices)


