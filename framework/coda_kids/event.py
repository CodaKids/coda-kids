"""This module contains a simple wrapper for pygame's event system.

coda kid's assignments rely on pylint to help catch potential errors, 
but some of the constants in pygame give false positives.

This event wrapper is meant to quiet some of those false positives,
while providing a function interface for keyboard and mouse input.
"""
import pygame
import coda_kids.dir

def listing():
    """
    Returns a list of all events currently in the event system.

        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop();
    """
    return pygame.event.get()

def quit_game(event):
    """
    Checks for quit game event.

        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop();
    """
    return event.type == pygame.QUIT

def mouse_l_button_up(event):
    """
    Checks if the left mouse button was released.

        for event in coda.event.listing():
            if coda.event.mouse_l_button_up(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONUP and event.button == 1

def mouse_l_button_down(event):
    """
    Checks if the left mouse button was clicked.

        for event in coda.event.listing():
            if coda.event.mouse_l_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def mouse_m_button_up(event):
    """
    Checks if the middle mouse button was released.

        for event in coda.event.listing():
            if coda.event.mouse_m_button_up(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONUP and event.button == 2

def mouse_m_button_down(event):
    """
    Checks if the middle mouse button was clicked.

        for event in coda.event.listing():
            if coda.event.mouse_m_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 2

def mouse_r_button_up(event):
    """
    Checks if the right mouse button was released.

        for event in coda.event.listing():
            if coda.event.mouse_r_button_up(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONUP and event.button == 3

def mouse_r_button_down(event):
    """
    Checks if the right mouse button was clicked.

        for event in coda.event.listing():
            if coda.event.mouse_r_button_down(event):
                do_things();
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 3

def mouse_down(event, button):
    """
    Checks if the left/right mouse button is being held down.

        for event in coda.event.listing():
            if coda.event.mouse_down(coda.dir.LEFT):
                do_things();
    """
    return pygame.mouse.get_pressed()[button]

def mouse_position():
    """
    Returns the position of the mouse as a tuple.

        data = coda.event.mouse_position();
    """
    pos = pygame.mouse.get_pos()
    return coda_kids.Vector2(pos[0], pos[1])

def key_down(event, key):
    """
    Checks if the keyboard key is pressed.

        for ev in coda.event.listing():
            # Space key pressed.
            if coda.event.key_down(ev, " "):
                do_things();
    """
    if isinstance(key, str):
        return event.type == pygame.KEYDOWN and event.key == ord(key)
    return event.type == pygame.KEYDOWN and event.key == key

def key_up(event, key):
    """
    Checks if the keyboard key is released.

        for ev in coda.event.listing():
            # Space key released.
            if coda.event.key_up(ev, " "):
                do_things();
    """
    if isinstance(key, str):
        return event.type == pygame.KEYUP and event.key == ord(key)
    return event.type == pygame.KEYUP and event.key == key

def key_held_down(key):
    """
    Checks if a key is being held down over multiple frames.

        # 'a' key held down.
        if coda.key_held_down("a"):
            do_things();
    """
    if isinstance(key, str):
        return pygame.key.get_pressed()[ord(key)]
    return pygame.key.get_pressed()[key]
