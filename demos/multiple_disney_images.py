"""

From stackoverflow:
http://stackoverflow.com/questions/24754053/multiple-images-in-easygui

Display more than one image at a time

"""

import sys

import easygui.button_box

sys.path.append('..')
import easygui as eg

# A welcome message
reply = easygui.button_box.msgbox("Welcome to the quiz", "Quiz!")
if reply is None:
    exit()

while 1:
    # Question 1
    images = list()
    images.append('images/mickey.gif')
    images.append('images/minnie.gif')
    images.append('images/daffy duck.gif')
    images.append('images/dave.gif')
    image = "mickey.gif"
    choices = ["Mickey", "Minnie", "Daffy Duck", "Dave"]
    reply = easygui.button_box.buttonbox("Click on mickey:", images=images, choices=['Cancel'])
    print(reply)
    if reply is None or reply=='Cancel':
        break

    if reply == images[0]:
        easygui.button_box.msgbox("Well done!", "Correct")
        break
    else:
        easygui.button_box.msgbox("Wrong", "Failure")

