__author__ = 'Robert'
__version__ = 'prototype D'
import sys

sys.path.append('..')
import easygui as eg

# This works just like before
reply = eg.buttonbox()  # This blocks until the user presses a button or closes the window.
print reply

# *** This is the new stuff ***
# Horst, I am trying to make the old and new things use exactly the same functions (like buttonbox).  Is this a
#        mistake?  Should I create a new API?

my_box2 = eg.buttonbox(run=False)  # Create a new button box.  Immediately returns.
"""
    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :param bool run: If True, dialog opens, blocks, and then returns information pressed.  Default is True
                     If False, dialog opens and immediately returns with a pointer to that dialog
    :param bool visible: If True, dialog is immediately visible.  Only matters if run is False.  default == True
    :return: if run==True: Returns the text of the button that the user selected
             if run==False: Returns a button box dialog that can be used later
"""

# Change to have four buttons
my_box2.choices = ['Yes', 'No', 'Maybe', "I don't care"]

# Disable fourth option
my_box2.choices[3].enabled = False

# Put these images on the four buttons
my_box2.choices.images = ['check.jpg', 'x.jpg', 'question.jpg', 'XXXX.jpg']

# Change the text of the first two buttons
my_box2.choices[0].text = "Yup"
my_box2.choices[1].text = "Nope"
my_box2.msg = "Start pressing buttons!!!!"
my_box2.images = ['foo.jpg', 'bar.jpg', 'baz.jpg', 'bog.jpg']
my_box2.timeout = 10  # Timeout after 10 seconds
my_box2.timeout_return_value = None  # If timeout is reached, return this value

# Display my_box2 and count the number of times a button is pressed.  if the user does not press a button
# with 10 seconds of previously pressing a button, time out and exit.
press_count = 0
while True:
    reply = my_box2.run()
    if reply is None:
        break
    press_count += 1
    my_box2.msg = "You have pressed a button {0} time(s)".format(press_count)
    print reply

# User has either hit cancel, or the timeout has triggered
my_box2.hide()


# Let's show that dialog again and create another one.  Then "run" them both.  The return 'reply' is a special
# instance which sort of acts like a string and sort of acts like a complex object, so if you say 'print reply',
# you get a simple return string.  But you can also say reply.widget and potentially other things such as type
# of event thrown.
my_box2.show()
my_box3 = eg.buttonbox(run=False)
my_box3.choices = ['Yup', 'Nope']
press_count = 0
while True:
    reply = eg.run_all()
    if reply is None:
        break
    press_count += 1
    if reply == "Yup":
        if reply.widget == my_box2:
            print("my_box2 said Yup")
        if reply.widget == my_box3:
            print("my_box3 said Yup")
my_box2.hide()
my_box3.hide()



