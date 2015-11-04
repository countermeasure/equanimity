import os

import config

from utils import print_in_color


def print_screen_header():
    """
    Clears the terminal and prints the program's heading.
    """
    os.system('clear')

    print_in_color('*' * 60, 'bold')
    print_in_color('%s  %s  %s' % ('*' * 23, 'EQUANIMITY', '*' * 23), 'bold')
    print_in_color('*' * 60, 'bold')

    print '\nDevice detected: %s\n' % config.DEVICE['name']


def print_header(header):
    """
    Prints a header with a line of asterisks above and below it.
    """
    print ''
    print_in_color('*' * 60, 'bold')
    padding = '*' * ((60 - len(header) - 4) / 2)
    padded_header = '%s  %s  %s' % (padding, header, padding)
    # If the header has an odd number of characters, the padded header will be
    # one asterisk too short, so correct for this.
    if len(padded_header) == 59:
        padded_header += '*'
    print_in_color(padded_header, 'bold')
    print_in_color('*' * 60, 'bold')
    print ''
