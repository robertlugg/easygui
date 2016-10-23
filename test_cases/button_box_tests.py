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
        msg="Sorting of buttons test, choices as a list: choices=['Alice', 'Bob', 'Charlie']",
        choices=['Alice', 'Bob', 'Charlie'],
        default_choice="Bob")
    print("Return: {}".format(value))

    value = eg.buttonbox(
        msg="Sorting of buttons test, choices as a dict (the choices can be mangled): choices={'Alice':1, 'Bob':2, 'Charlie':3}",
        choices={'Alice':1, 'Bob':2, 'Charlie':3},
        default_choice="Bob")
    print("Return: {}".format(value))


    choices = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    choices = collections.OrderedDict(choices)
    value = eg.buttonbox(
        msg="Sorting of buttons demo, choices passed as an ordered dict",
        choices=choices,
        default_choice="Bob")
    print("Return: {}".format(value))

    value = eg.buttonbox(
        msg='Sorting of buttons test, choices as list of pairs = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]',
        choices=[("Alice", 1), ("Bob", 2), ("Charlie", 3)],
        default_choice="Bob")
    print("Return: {}".format(value))

    eg.buttonbox(msg='Simple use test: \nbuttonbox(msg="Simple call test", choices=["Alice", "Bob", "Charlie"], default_choice="Bob")', choices=["Alice", "Bob", "Charlie"], default_choice="Bob")


def test_same_choices():

    value = eg.buttonbox(
        msg="Number choices test: \nchoices=[1, 2, 3]",
        choices=[1, 2, 3],
        default_choice=1)

    print("Return: {}".format(value))
    value = eg.buttonbox(
        msg='Repeating choices test (The first instance will be ignored): \nchoices=["Alice", "Alice", "Charlie"]',
        choices=["Alice", "Alice", "Charlie"],
        default_choice="Alice")

    print("Return: {}".format(value))

    value = eg.buttonbox(
        msg="Test of wrong default choice: \ndefault_choice='Daniel'",
        choices=['Alice', 'Bob', 'Charlie'],
        default_choice='Daniel')

    print("Return: {}".format(value))

    value = eg.buttonbox(
        msg="Test of wrong cancel choice: \ncancel_choice='Daniel'",
        choices=['Alice', 'Bob', 'Charlie'],
        default_choice='Alice',
        cancel_choice='Daniel')

    print("Return: {}".format(value))


if __name__ == '__main__':
    test_same_choices()
    test_ordering()
