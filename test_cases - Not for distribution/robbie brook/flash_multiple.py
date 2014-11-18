import sys

sys.path.append('../../..')
import easygui


choices = ["on", "off", "forward", "backward", "right", "left"] 
inp = ''
while inp != "None": #happens when the user presses ESC
    inp = easygui.buttonbox("controller","robot", choices)
    if inp == "forward":
        pass
    elif inp == "backward":
        pass
    elif inp == "off":
        break
