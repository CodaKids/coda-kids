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
