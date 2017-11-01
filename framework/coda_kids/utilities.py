"""This file contains a list of helper or utility functions."""
import sys
import time
import math
import random

import coda_kids

def read_file(filename):
    """Read a file line by line and return it as an array of strings."""
    # Create an empty array.
    array = []
    # Open our file for read.
    file = open(filename, 'r')

    # put all the lines in an array
    for line in file:
        array.append(line.rstrip())

    return array

def rand(minimum, maximum):
    """Generates a random whole number."""
    return random.randint(minimum, maximum)

def rand_location(minimum, maximum):
    """Generates a random location from the given min and max."""
    return coda_kids.Vector2(rand(minimum, maximum), rand(minimum, maximum))

class OutputConsole:
    """Class that displays strings in a console."""
    def __init__(self, location, num_of_lines, font_size, color):
        self.strings = []
        self.text = coda_kids.TextObject(color, font_size, "")
        self.location = location
        self.lines = num_of_lines
        self.font_size = font_size
        self.color = color
        self.decending = True

    def __setattr__(self, name, value):
        if name == "location":
            self.__dict__[name] = coda_kids.Vector2(value[0], value[1])
        elif name == "font_size":
            self.__dict__[name] = value
            self.text.font_size = value
        else:
            self.__dict__[name] = value

    def write(self, string):
        """Appends a string to the given console."""
        if len(self.strings) < self.lines:
            self.strings.append(string)
        else:
            i = 1
            while i < self.lines:
                self.strings[i - 1] = self.strings[i]
                i += 1
            self.strings[self.lines - 1] = string

    def clear(self):
        """Clears the console."""
        del self.strings[:]

    def draw(self, screen):
        """Draws the console strings to the screen"""
        def_loc = self.location
        string_num = 0
        offset = self.font_size

        if self.decending:
            for string in self.strings:
                loc = coda_kids.Vector2(def_loc.x, def_loc.y + string_num * offset)
                self.text.location = loc
                self.text.text = string
                self.text.draw(screen)
                string_num += 1
        else:
            for string in reversed(self.strings):
                loc = coda_kids.Vector2(def_loc.x, def_loc.y + string_num * offset)
                self.text.location = loc
                self.text.text = string
                self.text.draw(screen)
                string_num += 1
