__author__ = 'Robert'
"""
from:
http://stackoverflow.com/questions/20317314/python-function-in-a-while-loop-ruining-it-for-me

"""
import sys
sys.path.append('..')
import easygui as eg



def get_user_input(target_value, dice_rolls):

    operator_choices = ['+', '-', '*', '/']
    operator_choices.extend(['OK', 'Del', 'Reroll'])
    dice_choices = [str(r) for r in dice_rolls]
    dice_choices.extend(['Del', 'Reroll'])

    raw_user_input = list()
    mode = 'tick'
    while True:
        if mode == 'tick':
            choices = dice_choices
        else:
            choices = operator_choices
        var = eg.indexbox(''.join(raw_user_input), "Target value: {}".format(target_value), choices)
        if var is None:
            raise ValueError("Dialog closed with invalid entry")
        choice = choices[var]
        if choice == 'OK':
            return ''.join(raw_user_input)
        if choice == 'Del':
            raw_user_input = list()
            dice_choices = [str(r) for r in dice_rolls]
            dice_choices.extend(['Del', 'Reroll'])
            mode = 'tick'
            continue
        if choice == 'Reroll':
            return None
        raw_user_input.append(choice)
        if mode == 'tick': # Remove the dice from the list of dice
            del dice_choices[dice_choices.index(choices[var])]
        if mode == 'tick':
            mode = 'tock'
        else:
            mode = 'tick'


br_value = 12 # Sample value
dice_value_list = [4, 2, 1, 1, 5] # Sample rolls

try:
    user_input = get_user_input(br_value, dice_value_list)
except:
    print("Your data entry was cancelled by the user")
    exit()

if user_input is None:
    print("Exiting program because you cancelled the dialog")
    exit()

print("User entered: {}".format(user_input))
####
# Now, put code here to process your user_input
# ....
#
####