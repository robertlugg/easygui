"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

"""

import os
import sys
import utils as ut
import easygui as eg
import base_boxes as bb

# --------------------------------------------------------------
#
# test/demo easygui
#
# -----------------------------------------------------------------------

package_dir = os.path.dirname(os.path.realpath(__file__))


def egdemo():
    """
    Run the EasyGui demo.
    """
    # clear the console
    ut.writeln("\n" * 100)

    msg = list()
    msg.append("Pick the kind of box that you wish to demo.")
    msg.append(" * Python version {}".format(sys.version))
    msg.append(" * EasyGui version {}".format(eg.eg_version))
    msg.append(" * Tk version {}".format(bb.TkVersion))
    intro_message = "\n".join(msg)

    while True:  # do forever
        choices = [
            "msgbox",
            "buttonbox",
            "buttonbox(image) -- a buttonbox that displays an image",
            "choicebox",
            "multchoicebox",
            "textbox",
            "ynbox",
            "ccbox",
            "enterbox",
            "enterbox(image) -- an enterbox that displays an image",
            "exceptionbox",
            "codebox",
            "integerbox",
            "boolbox",
            "indexbox",
            "filesavebox",
            "fileopenbox",
            "passwordbox",
            "multenterbox",
            "multpasswordbox",
            "diropenbox",
            "About EasyGui",
            " Help"
        ]
        choice = eg.choicebox(
            msg=intro_message, title="EasyGui " + eg.eg_version,
            choices=choices)

        if not choice:
            return

        reply = choice.split()

        if reply[0] == "msgbox":
            reply = eg.msgbox("short msg", "This is a long title")
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "About":
            reply = eg.abouteasygui()

        elif reply[0] == "Help":
            _demo_help()

        elif reply[0] == "buttonbox":
            reply = eg.buttonbox(
                choices=['one', 'two', 'two', 'three'], default_choice='two')
            ut.writeln("Reply was: {!r}".format(reply))

            title = "Demo of Buttonbox with many, many buttons!"
            msg = ("This buttonbox shows what happens when you "
                   "specify too many buttons.")
            reply = eg.buttonbox(
                msg=msg, title=title, choices=choices, cancel_choice='msgbox')
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "buttonbox(image)":
            _demo_buttonbox_with_image()

        elif reply[0] == "boolbox":
            reply = eg.boolbox()
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "enterbox":
            image = os.path.join(package_dir, "python_and_check_logo.gif")
            message = ("Enter the name of your best friend."
                       "\n(Result will be stripped.)")
            reply = eg.enterbox(message, "Love!", "     Suzy Smith     ")
            ut.writeln("Reply was: {!r}".format(reply))

            message = ("Enter the name of your best friend."
                       "\n(Result will NOT be stripped.)")
            reply = eg.enterbox(
                message, "Love!", "     Suzy Smith     ", strip=False)
            ut.writeln("Reply was: {!r}".format(reply))

            reply = eg.enterbox("Enter the name of your worst enemy:", "Hate!")
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "enterbox(image)":
            image = os.path.join(package_dir, "python_and_check_logo.gif")
            message = "What kind of snake is this?"
            reply = eg.enterbox(message, "Quiz", image=image)
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "exceptionbox":
            try:
                thisWillCauseADivideByZeroException = 1 / 0
            except:
                eg.exceptionbox()

        elif reply[0] == "integerbox":
            reply = eg.integerbox(
                "Enter a number between 3 and 333",
                "Demo: integerbox WITH a default value", 222, 3, 333)
            ut.writeln("Reply was: {!r}".format(reply))

            reply = eg.integerbox(
                "Enter a number between 0 and 99",
                "Demo: integerbox WITHOUT a default value"
            )
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "diropenbox":
            _demo_diropenbox()
        elif reply[0] == "fileopenbox":
            _demo_fileopenbox()
        elif reply[0] == "filesavebox":
            _demo_filesavebox()

        elif reply[0] == "indexbox":
            title = reply[0]
            msg = "Demo of " + reply[0]
            choices = ["Choice1", "Choice2", "Choice3", "Choice4"]
            reply = eg.indexbox(msg, title, choices)
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "passwordbox":
            reply = eg.passwordbox("Demo of password box WITHOUT default"
                                   + "\n\nEnter your secret password",
                                   "Member Logon")
            ut.writeln("Reply was: {!s}".format(reply))

            reply = eg.passwordbox("Demo of password box WITH default"
                                   + "\n\nEnter your secret password",
                                   "Member Logon", "alfie")
            ut.writeln("Reply was: {!s}".format(reply))

        elif reply[0] == "multenterbox":
            msg = "Enter your personal information"
            title = "Credit Card Application"
            fieldNames = ["Name", "Street Address", "City", "State", "ZipCode"]
            fieldValues = list()  # we start with blanks for the values
            fieldValues = eg.multenterbox(msg, title, fieldNames)

            # make sure that none of the fields was left blank
            while 1:
                if fieldValues is None:
                    break
                errs = list()
                for n, v in zip(fieldNames, fieldValues):
                    if v.strip() == "":
                        errs.append('"{}" is a required field.'.format(n))
                if not len(errs):
                    break  # no problems found
                fieldValues = eg.multenterbox(
                    "\n".join(errs), title, fieldNames, fieldValues)

            ut.writeln("Reply was: {}".format(fieldValues))

        elif reply[0] == "multpasswordbox":
            msg = "Enter logon information"
            title = "Demo of multpasswordbox"
            fieldNames = ["Server ID", "User ID", "Password"]
            fieldValues = list()  # we start with blanks for the values
            fieldValues = eg.multpasswordbox(msg, title, fieldNames)

            # make sure that none of the fields was left blank
            while 1:
                if fieldValues is None:
                    break
                errs = list()
                for n, v in zip(fieldNames, fieldValues):
                    if v.strip() == "":
                        errs.append('"{}" is a required field.\n\n'.format(n))
                if not len(errs):
                    break  # no problems found
                fieldValues = eg.multpasswordbox(
                    "".join(errs), title, fieldNames, fieldValues)

            ut.writeln("Reply was: {!s}".format(fieldValues))

        elif reply[0] == "ynbox":
            title = "Demo of ynbox"
            msg = "Were you expecting the Spanish Inquisition?"
            reply = eg.ynbox(msg, title)
            ut.writeln("Reply was: {!r}".format(reply))
            if reply:
                eg.msgbox("NOBODY expects the Spanish Inquisition!", "Wrong!")

        elif reply[0] == "ccbox":
            msg = "Insert your favorite message here"
            title = "Demo of ccbox"
            reply = eg.ccbox(msg, title)
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "choicebox":
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
            reply = eg.choicebox(msg=msg, choices=listChoices)
            ut.writeln("Reply was: {!r}".format(reply))

            msg = "Pick something. "
            reply = eg.choicebox(msg=msg, title=title, choices=listChoices)
            ut.writeln("Reply was: {!r}".format(reply))

            msg = "Pick something. "
            reply = eg.choicebox(
                msg="The list of choices is empty!", choices=list())
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "multchoicebox":
            listChoices = ["aaa", "bbb", "ccc", "ggg", "hhh", "iii",
                           "jjj", "kkk", "LLL", "mmm", "nnn", "ooo",
                           "ppp", "qqq", "rrr", "sss", "ttt", "uuu",
                           "vvv"]

            msg = "Pick as many choices as you wish."
            reply = eg.multchoicebox(msg, "Demo of multchoicebox", listChoices)
            ut.writeln("Reply was: {!r}".format(reply))

        elif reply[0] == "textbox":
            _demo_textbox(reply[0])
        elif reply[0] == "codebox":
            _demo_codebox(reply[0])

        else:
            eg.msgbox("Choice\n\n{}\n\nis not recognized".format(
                choice), "Program Logic Error")
            return


def _demo_textbox(reply):
    text_snippet = ((
        "It was the best of times, and it was the worst of times.  The rich "
        "ate cake, and the poor had cake recommended to them, but wished "
        "only for enough cash to buy bread.  The time was ripe for "
        "revolution! "
        * 5) + "\n\n") * 10
    title = "Demo of textbox"
    msg = "Here is some sample text. " * 16
    reply = eg.textbox(msg, title, text_snippet)
    ut.writeln("Reply was: {!s}".format(reply))


def _demo_codebox(reply):
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
    reply = eg.codebox(msg, "Code Sample", code_snippet)
    ut.writeln("Reply was: {!r}".format(reply))


def _demo_buttonbox_with_image():
    msg = "Do you like this picture?\nIt is "
    choices = ["Yes", "No", "No opinion"]

    for image in [
            os.path.join(package_dir, "python_and_check_logo.gif"),
            os.path.join(package_dir, "python_and_check_logo.jpg"),
            os.path.join(package_dir, "python_and_check_logo.png"),
            os.path.join(package_dir, "zzzzz.gif")]:
        reply = eg.buttonbox(msg + image, image=image, choices=choices)
        ut.writeln("Reply was: {!r}".format(reply))


def _demo_help():
    savedStdout = sys.stdout  # save the sys.stdout file object
    sys.stdout = capturedOutput = bb.StringIO()
    print(globals()['__doc__'])  # help("easygui")
    sys.stdout = savedStdout  # restore the sys.stdout file object
    eg.codebox("EasyGui Help", text=capturedOutput.getvalue())


def _demo_filesavebox():
    filename = "myNewFile.txt"
    title = "File SaveAs"
    msg = "Save file as:"

    f = eg.filesavebox(msg, title, default=filename)
    ut.writeln("You chose to save file: {}".format(f))


def _demo_diropenbox():
    title = "Demo of diropenbox"
    msg = "Pick the directory that you wish to open."
    d = eg.diropenbox(msg, title)
    ut.writeln("You chose directory...: {}".format(d))

    d = eg.diropenbox(msg, title, default="./")
    ut.writeln("You chose directory...: {}".format(d))

    d = eg.diropenbox(msg, title, default="c:/")
    ut.writeln("You chose directory...: {}".format(d))


def _demo_fileopenbox():
    msg = "Python files"
    title = "Open files"
    default = "*.py"
    f = eg.fileopenbox(msg, title, default=default)
    ut.writeln("You chose to open file: {}".format(f))

    default = "./*.gif"
    msg = "Some other file types (Multi-select)"
    filetypes = ["*.jpg", ["*.zip", "*.tgs", "*.gz",
                           "Archive files"], ["*.htm", "*.html", "HTML files"]]
    f = eg.fileopenbox(
        msg, title, default=default, filetypes=filetypes, multiple=True)
    ut.writeln("You chose to open file: %s" % f)


if __name__ == '__main__':
    egdemo()
