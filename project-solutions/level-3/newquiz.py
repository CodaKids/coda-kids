import pygame
from os import path

def getFile(fileName):
    """Returns the absolute path of a file."""
    return path.join(path.dirname(__file__), fileName)

def randomize_answers(answerChoices):
    random.shuffle(answerChoices)
    return answerChoices

# Load Sprites
IMAGE_BUTTON = pygame.image.load(getFile('assets/Button.png'))

# Read file into an array
TRIVIA = []
file = open(getFile('assets/trivia.txt'), 'r')
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
wrongchoice3 = TRIVIA[4]

answerChoices = {answer, wrongchoice1, wrongchoice2, wrongchoice3}

#TODO: need to print to screen
#TODO: function that registers clicks

running = True
i = 0
score = 0
numberOfQuestions = 3
while i <=(numberOfQuestions*5):
    randomize_answers(answerChoices)
    #TODO: register click to chosen_answer
    #Have player write two if-statements:
    if chosen_answer == answer:
        print("Nice work! :)")
        score += 1
    else:
        print("Not exactly :(")
    #go to next question, and update our variables and array.
    i = i+5
    question = TRIVIA[i]
    answer = TRIVIA[i+1]
    wrongchoice1 = TRIVIA[i+2]
    wrongchoice2 = TRIVIA[i+3]
    wrongchoice3 = TRIVIA[i+4]
    answerChoices = {answer, wrongchoice1, wrongchoice2, wrongchoice3}

