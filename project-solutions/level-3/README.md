# Level 3

## Overview

The third project in the book focuses on file io, arrays, random number generation, and reinforces concepts from other lessons such as conditional branching and variables.

## The Game

The goal of the project is to create a simple multiple choice quiz game based on information about characters given in the previous game.

## Implementation

Users must:

1. Select a random question (index).
2. Select corresponding answer (same index).
3. Select a random location for the right answer.
4. Fill remaining answers with fake answers.
2. Track a user input answer.
3. Check against current question correct answer.
4. Tally questions answer
5. Tally correct answers
6. rise and repeat until quiz is done.

### questions.txt

Questions available for selection. Each line is a question, and each line gets stored as an element of an array of strings upon running the game.

### answers.txt

Answers to the questions. Each line should correspond 1 to 1 with the questions file. For example: the question on line 1 of questions.txt should correspond to the answer on line 1 of answers.txt. For the game to function properly, answers.txt should have the same number of lines as questions.txt.

### quiz.py

This is the game's main playable state. 

users will use ANSWERS, QUESTIONS, and FAKE_ANSWER arrays to implement the set_up_question() function by setting up question_text, correct_answer_index, and button_text array.

