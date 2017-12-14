# Level 2

## Overview

This second project in the book focuses on expressions and conditional branching, as well as introduces students to the coda kids framework code they will be using to implement game projects throughout the rest of the book. This readme will go over some of the basics of the project structure, as well as describe what parts of the game students will be implementing.

## The Game

The game itself is an introductary menu, in which the user can press forward and back buttons to display different states and text onto the screen. Each state represents a different character from the book, and toggling to it should display an image of the character, some bio text, and an associative sound effect.

## Implementation

The implementation of the game involves determining what to display based on a current selection, which can be adjusted inside of the update function through a button object.

## coda_kids Framework

Each coda kids project is broken down into two different files: The main.py file, and any individual states you would like coda kids to run.

for the sake of simplicity, most of the game projects themselves import coda_kids as coda, which is a form of aliasing.

### main.py

This file represents the entry point for the application. It contains the SDL window context initialization, as well as other configuration info such as the screen size. Through main, you also include and register any game states (files) you'd like the game state machine to know about. Finally, main.py also starts the game state machine, which begins the game's main loop.

### introduction.py

This file represents a game state. Each part of each game represents a state, such as menus, title screens, etc that you can toggle between based on player actions and other conditions. For the purpose of this assignment there is only 1 state. Each Game state users make should have 1 of each of the following functions described below:

#### def initialize(window)
This is a state that is called when the game first changes over to this state from another (or none at all). Users can use this to initialize global data they want reset every time they transition back and forth between 1 or more states. The window size as a vector (x,y) is provided to allow users to align object positions with respect to the window.

#### def update(delta_time)
This function is called every frame (~60 times a second) and represents the bulk of how the state behaves. In this state, users can listen for input events, perform collision detection, update objects, increment score, etc. delta_time is provided in order to allow users to increment variables with respect to time (as a scalar).

#### def draw(screen)
This function is called after update in the main game loop, and is where users can draw backgrounds, objects, and text to the screen. The screen surface for the game is provided and passed to the object calling method like so:

obj.draw(screen)

#### def cleanup()
This function should be provided for when the user wants to transition out of the state. Because python is whats called a garbage collected language, it's seldom necessary to use it to clean up variable data, however it can be useful for serializing information or other tasks necessary upon leaving a gameplay state (such as recording score to a file.)



