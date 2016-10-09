__author__ = 'Juanjo'
"""
Test cases
"""

import sys
sys.path.append('..')
import easygui as eg
import collections

def test_ordering():

    value = eg.buttonbox(
        msg="Sorting of buttons demo, choose a name",
        choices=["Alice", "Bob", "Charlie"],
        default_choice="Bob")
    print("Return: {}".format(value))


    choices = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    choices = collections.OrderedDict(choices)
    value = eg.buttonbox(
        msg="Sorting of buttons demo, choose a day",
        choices=choices,
        default_choice="Bob")
    print("Return: {}".format(value))


    choices = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    value = eg.buttonbox(
        msg="Sorting of buttons demo, choose a day",
        choices=choices,
        default_choice="Monday")
    print("Return: {}".format(value))


    choices=["Alice", "Bob", "Charlie"]
    eg.buttonbox(msg="Choose a name", choices=choices)

if __name__ == '__main__':
    test_ordering()
