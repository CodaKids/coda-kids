import pygame
import random
from os import path

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs your files from your folder.
    return path.join(path.dirname(__file__), fileName)

def randomize_answers(answerChoices):
    #This randomly shuffles the answers so it's not easy to tell which is the right answer.
    random.shuffle(answerChoices)
    return answerChoices

def display_screen():
    #This is all of the code that loads the next question and Mrs. Kodala's reaction
    #and loads it to your screen.
    question_text = myfont.render(question, True, (255, 0, 0))
    question_rect = question_text.get_rect(topleft=(250,250))
    answer_1_text = myfont.render(ANSWER_CHOICES[0], True, (255, 0, 0))
    answer_1_rect = answer_1_text.get_rect(topleft=(250,300))
    answer_2_text = myfont.render(ANSWER_CHOICES[1], True, (255, 0, 0))
    answer_2_rect = answer_2_text.get_rect(topleft=(250,350))
    answer_3_text = myfont.render(ANSWER_CHOICES[2], True, (255, 0, 0))
    answer_3_rect = answer_3_text.get_rect(topleft=(250,400))
    screen.blit(background, (0,0))
    screen.blit(kodala, (0,0))
    screen.blit(question_text, question_rect)
    screen.blit(answer_1_text, answer_1_rect)
    screen.blit(answer_2_text, answer_2_rect)
    screen.blit(answer_3_text, answer_3_rect)
    pygame.display.update()

# Load Sprites
background = pygame.image.load(get_file('Background.png'))
correct_a = pygame.image.load(get_file('CorrectAnswerA.png'))
correct_b = pygame.image.load(get_file('CorrectAnswerB.png'))
incorrect_a = pygame.image.load(get_file('IncorrectAnswerA.png'))
incorrect_b = pygame.image.load(get_file('IncorrectAnswerB.png'))
end_game = pygame.image.load(get_file('EndGame.png'))

"""Displays background to the screen"""
#We set the background image of Mrs. Codala's classroom.
width = 960
height = 540
screen = pygame.display.set_mode((width,height))
running = True

#scaling the images to fit the screen size
background = pygame.transform.scale(background, (960, 540))
correct_a = pygame.transform.scale(correct_a, (480, 270))
correct_b = pygame.transform.scale(correct_b, (480, 270))
incorrect_a = pygame.transform.scale(incorrect_a, (480, 270))
incorrect_b = pygame.transform.scale(incorrect_b, (480, 270))
end_game = pygame.transform.scale(end_game, (480, 270))

# Read file into an array
TRIVIA = []
file = open(get_file('trivia.txt'), 'r')
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

ANSWER_CHOICES = [answer, wrongchoice1, wrongchoice2]

"""Initialize Font Object"""
#We pick our text style and size.
pygame.init()
myfont = pygame.font.SysFont(None, 35)

"""Initializing Question and Answer Text Globally"""
question_text = myfont.render(question, True, (255, 0, 0))
question_rect = question_text.get_rect(topleft=(250,250))
answer_1_text = myfont.render(ANSWER_CHOICES[0], True, (255, 0, 0))
answer_1_rect = answer_1_text.get_rect(topleft=(250,300))
answer_2_text = myfont.render(ANSWER_CHOICES[1], True, (255, 0, 0))
answer_2_rect = answer_2_text.get_rect(topleft=(250,350))
answer_3_text = myfont.render(ANSWER_CHOICES[2], True, (255, 0, 0))
answer_3_rect = answer_3_text.get_rect(topleft=(250,400))


i = 0
number_of_questions = 3
questions_answered = 0
kodala = correct_a
while running:
    display_screen()
    events = pygame.event.get()
    for event in events:
        mpos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if answer_1_rect.collidepoint(mpos):
                if ANSWER_CHOICES[0] == answer:
                    print("That's correct!")
                    kodala = correct_a
                    if i >= (number_of_questions * 4)-4:
                        kodala = end_game
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
                else:
                    print("That's wrong.")
                    kodala = incorrect_a
                    if i >= (number_of_questions * 4)-4:
                        kodala = end_game
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
            if answer_2_rect.collidepoint(mpos):
                if ANSWER_CHOICES[1] == answer:
                    print("That's correct!")
                    kodala = correct_b
                    if i >= (number_of_questions * 4)-4:
                        kodala = end_game
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
                else:
                    print("That's wrong.")
                    kodala = incorrect_b
                    if i >= (number_of_questions * 4)-4:
                        kodala = end_game
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
            if answer_3_rect.collidepoint(mpos):
                if ANSWER_CHOICES[2] == answer:
                    print("That's correct!")
                    kodala = correct_a
                    if i >= (number_of_questions * 4)-4:
                        kodala = end_game
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
                else:
                    print("That's wrong.")
                    kodala = incorrect_a
                    if i >= (number_of_questions * 4)-4:
                        kodala = end_game
                    else:
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
