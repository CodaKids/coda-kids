import pygame
import random
import time
from os import path

"""Initialize Font Objects"""
#We pick our text style and size.
pygame.init()
myfont = pygame.font.SysFont('Arial', 35)
answer_1_text = myfont.render("                        ", True, (0, 0, 0))
answer_1_rect = answer_1_text.get_rect(topleft=(200,230))
answer_2_text = myfont.render("                         ", True, (0, 0, 0))
answer_2_rect = answer_2_text.get_rect(topleft=(200,300))
answer_3_text = myfont.render("                         ", True, (0, 0, 0))
answer_3_rect = answer_3_text.get_rect(topleft=(200,370))
sample_click = myfont.render("Click here to start the game.", True, (0,0,0))
sample_click_rect = sample_click.get_rect(topleft=(200,230))
correct_text = myfont.render("That is correct.", True, (0,128,0))
incorrect_text = myfont.render("That is incorrect.", True, (255,0,0))

def get_file(fileName):
    """Returns the absolute path of a file."""
    #This grabs your files from your folder.
    return path.join(path.dirname(__file__), fileName)

def randomize_answers(answerChoices):
    #This randomly shuffles the answers so the player doesn't know which one is the correct answer.
    random.shuffle(answerChoices)
    return answerChoices

def display_question():
    #This code loads and displays the next question and Mrs. Codala's reaction.
    question_text = myfont.render(question, True, (0, 0, 0))
    question_rect = question_text.get_rect(topleft=(200,150))
    answer_1_text = myfont.render(ANSWER_CHOICES[0], True, (0, 0, 0))
    answer_1_rect = answer_1_text.get_rect(topleft=(200,230))
    answer_2_text = myfont.render(ANSWER_CHOICES[1], True, (0, 0, 0))
    answer_2_rect = answer_2_text.get_rect(topleft=(200,300))
    answer_3_text = myfont.render(ANSWER_CHOICES[2], True, (0, 0, 0))
    answer_3_rect = answer_3_text.get_rect(topleft=(200,370))
    screen.blit(background, (0,0))
    screen.blit(question_text, question_rect)
    screen.blit(answer_1_text, answer_1_rect)
    screen.blit(answer_2_text, answer_2_rect)
    screen.blit(answer_3_text, answer_3_rect)
    pygame.display.update()

def display_intro_screen():
    #This shows the intro text (so we only run it once, at the beginning).
    intro_text = myfont.render("Welcome to the Trivia Game!", True, (0,0,0))
    sample_click = myfont.render("Click here to start.", True, (0,0,0))
    sample_click_rect = sample_click.get_rect(topleft=(200,230))
    screen.blit(background,(0,0))
    screen.blit(intro_text, (200,150))
    screen.blit(sample_click,sample_click_rect)
    pygame.display.update()

def display_end_screen():
    #This shows the image of Mrs. Codala telling you the game is done.
    kodala = end_game
    screen.blit(background, (0,0))
    screen.blit(kodala,(0,0))
    pygame.display.update()

"""Load Sprites"""
#We load the images and put them in variables.
background = pygame.image.load(get_file('Background.png'))
correct_a = pygame.image.load(get_file('CorrectAnswerA.png'))
correct_b = pygame.image.load(get_file('CorrectAnswerB.png'))
incorrect_a = pygame.image.load(get_file('IncorrectAnswerA.png'))
incorrect_b = pygame.image.load(get_file('IncorrectAnswerB.png'))
end_game = pygame.image.load(get_file('EndGame.png'))

"""Set Window Size"""
#We set the window size for our game.
width = 960
height = 540
screen = pygame.display.set_mode((width,height))

#We pull each line of text from the file into a list.
TRIVIA = []
file = open(get_file('trivia.txt'), 'r')
for line in file:
    TRIVIA.append(line.rstrip())

#We now have a list that holds our current question, correct answer,
#and the two wrong answers, in that order. We use these variables to 
#display the text on the screen.
question = TRIVIA[0]
answer = TRIVIA[1]
wrongchoice1 = TRIVIA[2]
wrongchoice2 = TRIVIA[3]

ANSWER_CHOICES = [answer, wrongchoice1, wrongchoice2]

i = 0
number_of_questions = 3
questions_answered = 0
display_intro_screen() #Gets the screen ready.
running = False
while running == False: 
    #We're waiting for the player to click "Click here to start the game."
    events = pygame.event.get()
    for event in events:
        mpos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sample_click_rect.collidepoint(mpos):
                running = True
while running:
    display_question() #Displays the new question and the three answer choices.
    events = pygame.event.get()
    for event in events:
        mpos = pygame.mouse.get_pos() 
        if event.type == pygame.MOUSEBUTTONDOWN: #If the player clicks the mouse.
            if answer_1_rect.collidepoint(mpos): #If the player clicks the first answer on the top.
                if ANSWER_CHOICES[0] == answer: #If it's the correct answer.
                    screen.blit(correct_text,(300,0))
                    kodala = correct_a
                    screen.blit(kodala, (0,0))
                    pygame.display.update()
                    time.sleep(5)
                    if i >= (number_of_questions * 4)-4: #If it's the last question.
                        display_end_screen()
                        time.sleep(5)
                        running = False
                    else: #If it's the not the last question, we display the next question.
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
                else: #If it's an incorrect answer.
                    screen.blit(incorrect_text,(300,0))
                    kodala = incorrect_a
                    screen.blit(kodala, (0,0))
                    pygame.display.update()
                    time.sleep(5)
                    if i >= (number_of_questions * 4)-4: #If it's the last question.
                        display_end_screen()
                        time.sleep(5)
                        running = False
                    else: #If it's the not the last question, we display the next question.
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
            if answer_2_rect.collidepoint(mpos): #If the player clicks the second answer.
                if ANSWER_CHOICES[1] == answer: #If it's the correct answer.
                    screen.blit(correct_text,(300,0))
                    kodala = correct_b
                    screen.blit(kodala, (0,0))
                    pygame.display.update()
                    time.sleep(5)
                    if i >= (number_of_questions * 4)-4: #If it's the last question.
                        display_end_screen()
                        time.sleep(5)
                        running = False
                    #Copy from the book to move to the next question.
                    else: #If it's the not the last question, we display the next question.
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
                else: #If it's an incorrect answer.
                    screen.blit(incorrect_text,(300,0))
                    kodala = incorrect_b
                    screen.blit(kodala,(0,0))
                    pygame.display.update()
                    time.sleep(5)
                    if i >= (number_of_questions * 4)-4: #If it's the last question.
                        display_end_screen()
                        time.sleep(5)
                        running = False
                    #Copy from the book to move to the next question.
                    else: #If it's the not the last question, we display the next question.
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
            if answer_3_rect.collidepoint(mpos): #If the player clicks the third answer.
                if ANSWER_CHOICES[2] == answer: #If it's the correct answer.
                    screen.blit(correct_text,(300,0))
                    kodala = correct_a
                    screen.blit(kodala, (0,0))
                    pygame.display.update()
                    time.sleep(5)
                    if i >= (number_of_questions * 4)-4: #If it's the last question.
                        display_end_screen()
                        time.sleep(5)
                        running = False
                    else: #If it's the not the last question, we display the next question.
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
                else: #If it's an incorrect answer.
                    screen.blit(incorrect_text,(300,0))
                    kodala = incorrect_a
                    screen.blit(kodala, (0,0))
                    pygame.display.update()
                    time.sleep(5)
                    if i >= (number_of_questions * 4)-4: #If it's the last question.
                        display_end_screen()
                        running = False
                    else: #If it's the not the last question, we display the next question.
                        i = i+4
                        question = TRIVIA[i]
                        answer = TRIVIA[i+1]
                        wrong_choice_1 = TRIVIA[i+2]
                        wrong_choice_2 = TRIVIA[i+3]
                        ANSWER_CHOICES = [answer, wrong_choice_1, wrong_choice_2]
                        randomize_answers(ANSWER_CHOICES)
