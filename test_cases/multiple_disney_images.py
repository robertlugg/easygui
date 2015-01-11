
"""

From stackoverflow:
http://stackoverflow.com/questions/24754053/multiple-images-in-easygui

Display more than one image at a time

"""

import sys

sys.path.append('..')
import easygui as eg

# A welcome message
eg.msgbox ("Welcome to the quiz", "Quiz!")
# A short splash screen this could be looped
Finish = "Start"
while Finish  == "Start":

    Finish = eg.buttonbox("Do you want to start the quiz or quit?","Welcome",["Start","Quit"])
    if Finish == "Quit":
        break
    #Question 1
    image = "mickey.gif"
    choices = ["Mickey","Minnie","Daffy Duck","Dave"]
    reply=eg.buttonbox("Who is this?",image = image,choices = choices)

    if reply == "Mickey":
        eg.msgbox("Well done!","Correct")
    else:
        eg.msgbox("Wrong","Failure")

# This works, but if I change the line

# reply=eg.buttonbox("Who is this?",image=[image,image2,image3,image4],choices = choices)

# But that doesn't seem to work, does anyone know if you can have more than one image per buttonbox?