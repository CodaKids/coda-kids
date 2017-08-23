coda_kids
=========

coda_kids is a partial wrapper package around pygame. It's purpose is to
make game development more accessible to a younger audiences
of students. It provides inline documentation, wrappers for linter 
unfriendly features, and provides utility functionality/classes such 
as game objects and constants for common colors.

It is currently being designed for and tested with a series of
game programming exercises for an educational book Coda Kids.

The package was designed and implemented with and for the
following toolset:

Python 3.5.2 with latest Pygame and Pylint.
Visual Studio Code 1.11+ with the Python extension installed.

Simple Example
--------------
::

    import coda_kids as coda

    WINDOW = coda.Vector2(800, 600)
    SCREEN = coda.start(WINDOW, "Hello World!")
    TEXT = coda.TextObject(coda.color.BLACK, 48, "Hello World!")
    TEXT.location = WINDOW / 2 # center of window
    TEXT.centered = True

    while True:
        for event in coda.event.listing():
            if coda.event.quit_game(event):
                coda.stop()
        coda.start_draw(SCREEN, coda.color.WHITE)
        TEXT.draw(SCREEN)
        coda.end_draw()


To Do
=====

1) Add a 2D animation class supportable by objects.
2) Runtime type checking for coda_kids class constructors and function arguments.
3) Provide additional example code and documentation.
4) Clean up object interface methods.
5) Refactor finite state machine tools.

Change Log
==========

0.2.3
-----

- Added an output console utility for in window output text. 
  It can be found in coda_kids.utilities.
- Added support functions and documentation for starting and ending a frame.
- Cleaned up and added documentation to the .rst file.

0.2.2
-----

- Updated git repo and setup/url information.
- Added action system to coda for python class members. [Feature in Alpha]
- Updated object class to properly scale objects with it's scale member.
- Moved standard library imports to coda_kids.utilities


0.2.1
-----

- Reformatted some of the library utilities.

0.2.0
-----
- Fixed some formatting issues with the setup.py file.