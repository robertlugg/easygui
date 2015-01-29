"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

"""

import os
import sys


from . import utils as ut
from .button_box import buttonbox
from .text_box import textbox
from .diropen_box import diropenbox
from .fileopen_box import fileopenbox
from .filesave_box import filesavebox
from .multi_fillable_box import multenterbox
from .multi_fillable_box import multpasswordbox

from .derived_boxes import ynbox
from .derived_boxes import ccbox
from .derived_boxes import boolbox
from .derived_boxes import indexbox
from .derived_boxes import msgbox
from .derived_boxes import integerbox
from .derived_boxes import enterbox
from .derived_boxes import exceptionbox
from .derived_boxes import codebox
from .derived_boxes import passwordbox

from .choice_box import choicebox
from .choice_box import multchoicebox

from . import about
from .about import eg_version
from .about import abouteasygui

# --------------------------------------------------------------
#
# test/demo easygui
#
# -----------------------------------------------------------------------

package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Choices(object):

    """docstring for Choices"""

    def __init__(self):
        self.choices = [
            ("msgbox", demo_msgbox),
            ("buttonbox", demo_buttonbox),
            ("buttonbox that displays an image", demo_buttonbox_with_image),
            ("choicebox", demo_choicebox),
            ("multchoicebox", demo_multichoicebox),
            ("textbox", demo_textbox),
            ("ynbox", demo_ynbox),
            ("ccbox", demo_ccbox),
            ("enterbox", demo_enterbox),
            ("enterbox that displays an image", demo_enterbox_image),
            ("exceptionbox", demo_exceptionbox),
            ("codebox", demo_codebox),
            ("integerbox", demo_integerbox),
            ("boolbox", demo_boolbox),
            ("indexbox", demo_indexbox),
            ("filesavebox", demo_filesavebox),
            ("fileopenbox", demo_fileopenbox),
            ("passwordbox", demo_passwordbox),
            ("multenterbox", demo_multenterbox),
            ("multpasswordbox", demo_multpasswordbox),
            ("diropenbox", demo_diropenbox),
            ("About EasyGui", demo_about),
            ("Help", demo_help),
        ]

    def keys(self):
        keys = [c[0] for c in self.choices]
        return keys

    def find_demo(self, key):
        demo = next((c[1] for c in self.choices if c[0] == key))
        return demo


def easygui_demo():
    """
    Run the EasyGui demo.
    """
    choices = Choices()
    # clear the console
    print('\n' * 100)

    msg = []
    msg.append("Pick the kind of box that you wish to demo.")
    msg.append(" * Python version {}".format(sys.version))
    msg.append(" * EasyGui version {}".format(eg_version))
    msg.append(" * Tk version {}".format(ut.TkVersion))
    intro_message = "\n".join(msg)
    title = "EasyGui " + eg_version
    # Table that relates keys in choicebox with functions to execute

    while True:

        reply = choicebox(msg=intro_message,
                          title=title,
                          choices=choices.keys())
        if not reply:
            break

        print reply
        chosen_demo = reply

        # Execute the chosen demo!
        choices.find_demo(chosen_demo)()


def demo_msgbox():
    reply = msgbox("short msg", "This is a long title")
    print("Reply was: {!r}".format(reply))


def demo_buttonbox():
    reply = buttonbox(choices=['one', 'two', 'two', 'three'],
                      default_choice='two')
    print("Reply was: {!r}".format(reply))

    title = "Demo of Buttonbox with many, many buttons!"
    msg = ("This buttonbox shows what happens when you "
           "specify too many buttons.")
    reply = buttonbox(msg=msg, title=title,
                      choices=['1', '2', '3', '4', '5', '6', '7'],
                      cancel_choice='msgbox')
    print("Reply was: {!r}".format(reply))


def demo_buttonbox_with_image():
    msg = "Do you like this picture?\nIt is "
    choices = ["Yes", "No", "No opinion"]

    for image in [
            os.path.join(package_dir, "python_and_check_logo.gif"),
            os.path.join(package_dir, "python_and_check_logo.jpg"),
            os.path.join(package_dir, "python_and_check_logo.png"),
            os.path.join(package_dir, "zzzzz.gif")]:
        reply = buttonbox(msg + image, image=image, choices=choices)
        print("Reply was: {!r}".format(reply))


def demo_ccbox():
    msg = "Insert your favorite message here"
    title = "Demo of ccbox"
    reply = ccbox(msg, title)
    print("Reply was: {!r}".format(reply))


def demo_multichoicebox():
    listChoices = ["aaa", "bbb", "ccc", "ggg", "hhh", "iii",
                   "jjj", "kkk", "LLL", "mmm", "nnn", "ooo",
                   "ppp", "qqq", "rrr", "sss", "ttt", "uuu",
                   "vvv"]

    msg = "Pick as many choices as you wish."
    reply = multchoicebox(msg, "Demo of multchoicebox", listChoices)
    print("Reply was: {!r}".format(reply))


def demo_ynbox():
    title = "Demo of ynbox"
    msg = "Were you expecting the Spanish Inquisition?"
    reply = ynbox(msg, title)
    print("Reply was: {!r}".format(reply))
    if reply:
        msgbox("NOBODY expects the Spanish Inquisition!", "Wrong!")


def demo_choicebox():
    title = "Demo of choicebox"
    longchoice = (
        "This is an example of a very long option "
        "which you may or may not wish to choose."
        * 2)
    listChoices = ["nnn", "ddd", "eee", "fff", "aaa",
                   longchoice, "aaa", "bbb", "ccc", "ggg", "hhh",
                   "iii", "jjj", "kkk", "LLL", "mmm", "nnn",
                   "ooo", "ppp", "qqq",
                   "rrr", "sss", "ttt", "uuu", "vvv"]

    msg = ("Pick something. " +
           ("A wrapable sentence of text ?! " * 30) +
           "\nA separate line of text." * 6)
    reply = choicebox(msg=msg, choices=listChoices)
    print("Reply was: {!r}".format(reply))

    msg = "Pick something. "
    reply = choicebox(msg=msg, title=title, choices=listChoices)
    print("Reply was: {!r}".format(reply))

    msg = "Pick something. "
    reply = choicebox(
        msg="The list of choices is empty!", choices=list())
    print("Reply was: {!r}".format(reply))


def demo_integerbox():
    reply = integerbox(
        "Enter a number between 3 and 333",
        "Demo: integerbox WITH a default value", 222, 3, 333)
    print("Reply was: {!r}".format(reply))

    reply = integerbox(
        "Enter a number between 0 and 99",
        "Demo: integerbox WITHOUT a default value"
    )
    print("Reply was: {!r}".format(reply))


def demo_about():
    reply = abouteasygui()
    print("Reply was: {!r}".format(reply))


def demo_enterbox():
    image = os.path.join(package_dir, "python_and_check_logo.gif")
    message = ("Enter the name of your best friend."
               "\n(Result will be stripped.)")
    reply = enterbox(message, "Love!", "     Suzy Smith     ")
    print("Reply was: {!r}".format(reply))

    message = ("Enter the name of your best friend."
               "\n(Result will NOT be stripped.)")
    reply = enterbox(
        message, "Love!", "     Suzy Smith     ", strip=False)
    print("Reply was: {!r}".format(reply))

    reply = enterbox("Enter the name of your worst enemy:", "Hate!")
    print("Reply was: {!r}".format(reply))


def demo_multpasswordbox():
    msg = "Enter logon information"
    title = "Demo of multpasswordbox"
    fieldNames = ["Server ID", "User ID", "Password"]
    fieldValues = list()  # we start with blanks for the values
    fieldValues = multpasswordbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while True:
        if fieldValues is None:
            break
        errs = list()
        for n, v in zip(fieldNames, fieldValues):
            if v.strip() == "":
                errs.append('"{}" is a required field.\n\n'.format(n))
        if not len(errs):
            break  # no problems found
        fieldValues = multpasswordbox(
            "".join(errs), title, fieldNames, fieldValues)

    print("Reply was: {!s}".format(fieldValues))


def demo_textbox():
    text_snippet = ((
        "It was the best of times, and it was the worst of times.  The rich "
        "ate cake, and the poor had cake recommended to them, but wished "
        "only for enough cash to buy bread.  The time was ripe for "
        "revolution! "
        * 5) + "\n\n") * 10
    title = "Demo of textbox"
    msg = "Here is some sample text. " * 16
    reply = textbox(msg, title, text_snippet)
    print("Reply was: {!s}".format(reply))


def demo_codebox(reply):
    # TODO RL: Turn this sample code into the code in this module, just for fun
    code_snippet = ("dafsdfa dasflkj pp[oadsij asdfp;ij asdfpjkop asdfpok asdfpok asdfpok" * 3) + "\n" + """# here is some dummy Python code
for someItem in myListOfStuff:
    do something(someItem)
    do something()
    do something()
    if somethingElse(someItem):
        doSomethingEvenMoreInteresting()

""" * 16
    msg = "Here is some sample code. " * 16
    reply = codebox(msg, "Code Sample", code_snippet)
    print("Reply was: {!r}".format(reply))


def demo_boolbox():
    reply = boolbox()
    print("Reply was: {!r}".format(reply))


def demo_enterbox_image():
    image = os.path.join(package_dir, "python_and_check_logo.gif")
    message = "What kind of snake is this?"
    reply = enterbox(message, "Quiz", image=image)
    print("Reply was: {!r}".format(reply))


def demo_passwordbox():
    reply = passwordbox("Demo of password box WITHOUT default"
                        + "\n\nEnter your secret password",
                        "Member Logon")
    print("Reply was: {!s}".format(reply))

    reply = passwordbox("Demo of password box WITH default"
                        + "\n\nEnter your secret password",
                        "Member Logon", "alfie")
    print("Reply was: {!s}".format(reply))


def demo_help():
    codebox("EasyGui Help", text=about.EASYGUI_ABOUT_INFORMATION)


def demo_filesavebox():
    filename = "myNewFile.txt"
    title = "File SaveAs"
    msg = "Save file as:"

    f = filesavebox(msg, title, default=filename)
    print("You chose to save file: {}".format(f))


def demo_diropenbox():
    title = "Demo of diropenbox"
    msg = "Pick the directory that you wish to open."
    d = diropenbox(msg, title)
    print("You chose directory...: {}".format(d))

    d = diropenbox(msg, title, default="./")
    print("You chose directory...: {}".format(d))

    d = diropenbox(msg, title, default="c:/")
    print("You chose directory...: {}".format(d))


def demo_exceptionbox():
    try:
        thisWillCauseADivideByZeroException = 1 / 0
    except:
        exceptionbox()


def demo_indexbox():
    title = "Indexbox"
    msg = "Demo of " + "indexbox"
    choices = ["Choice1", "Choice2", "Choice3", "Choice4"]
    reply = indexbox(msg, title, choices)
    print("Reply was: {!r}".format(reply))


def demo_multenterbox():
    msg = "Enter your personal information"
    title = "Credit Card Application"
    fieldNames = ["Name", "Street Address", "City", "State", "ZipCode"]
    fieldValues = list()  # we start with blanks for the values
    fieldValues = multenterbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while True:
        if fieldValues is None:
            break
        errs = list()
        for n, v in zip(fieldNames, fieldValues):
            if v.strip() == "":
                errs.append('"{}" is a required field.'.format(n))
        if not len(errs):
            break  # no problems found
        fieldValues = multenterbox(
            "\n".join(errs), title, fieldNames, fieldValues)

    print("Reply was: {}".format(fieldValues))


def demo_fileopenbox():
    msg = "Python files"
    title = "Open files"
    default = "*.py"
    f = fileopenbox(msg, title, default=default)
    print("You chose to open file: {}".format(f))

    default = "./*.gif"
    msg = "Some other file types (Multi-select)"
    filetypes = ["*.jpg", ["*.zip", "*.tgs", "*.gz",
                           "Archive files"], ["*.htm", "*.html", "HTML files"]]
    f = fileopenbox(
        msg, title, default=default, filetypes=filetypes, multiple=True)
    print("You chose to open file: %s" % f)
