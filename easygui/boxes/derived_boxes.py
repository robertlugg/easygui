"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

"""

from . import base_boxes as bb
from . import text_box as tb
from . import utils as ut

# -------------------------------------------------------------------
# various boxes built on top of the basic buttonbox
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# ynbox
# -----------------------------------------------------------------------


def ynbox(msg="Shall I continue?", title=" ",
          choices=("[<F1>]Yes", "[<F2>]No"), image=None,
          default_choice='[<F1>]Yes', cancel_choice='[<F2>]No'):
    """
    Display a msgbox with choices of Yes and No.

    The returned value is calculated this way::

        if the first choice ("Yes") is chosen, or if the dialog is cancelled:
            return True
        else:
            return False

    If invoked without a msg argument, displays a generic
    request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ynbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    :param msg: the msg to be displayed
    :type msg: str
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted
        when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which
      button should be pressed

    :return: True if 'Yes' or dialog is cancelled, False if 'No'
    """
    return boolbox(msg=msg,
                   title=title,
                   choices=choices,
                   image=image,
                   default_choice=default_choice,
                   cancel_choice=cancel_choice)

# -----------------------------------------------------------------------
# ccbox
# -----------------------------------------------------------------------


def ccbox(msg="Shall I continue?", title=" ",
          choices=("C[o]ntinue", "C[a]ncel"), image=None,
          default_choice='Continue', cancel_choice='Cancel'):
    """
    Display a msgbox with choices of Continue and Cancel.

    The returned value is calculated this way::

        if the first choice ("Continue") is chosen,
          or if the dialog is cancelled:
            return True
        else:
            return False

    If invoked without a msg argument, displays a generic
        request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ccbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted
      when the gui appears
    :param str cancel_choice: If the user presses the 'X' close,
      which button should be pressed

    :return: True if 'Continue' or dialog is cancelled, False if 'Cancel'
    """
    return boolbox(msg=msg,
                   title=title,
                   choices=choices,
                   image=image,
                   default_choice=default_choice,
                   cancel_choice=cancel_choice)

# -----------------------------------------------------------------------
# boolbox
# -----------------------------------------------------------------------


def boolbox(msg="Shall I continue?", title=" ",
            choices=("[Y]es", "[N]o"), image=None,
            default_choice='Yes', cancel_choice='No'):
    """
    Display a boolean msgbox.

    The returned value is calculated this way::

        if the first choice is chosen, or if the dialog is cancelled:
            returns True
        else:
            returns False

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted
      when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button
      should be pressed
    :return: True if first button pressed or dialog is cancelled, False if
      second button is pressed
    """
    if len(choices) != 2:
        raise AssertionError(
            'boolbox takes exactly 2 choices!  Consider using indexbox instead'
        )

    reply = bb.buttonbox(msg=msg,
                         title=title,
                         choices=choices,
                         image=image,
                         default_choice=default_choice,
                         cancel_choice=cancel_choice)
    if reply == choices[0]:
        return True
    else:
        return False


# -----------------------------------------------------------------------
# indexbox
# -----------------------------------------------------------------------
def indexbox(msg="Shall I continue?", title=" ",
             choices=("Yes", "No"), image=None,
             default_choice='Yes', cancel_choice='No'):
    """
    Display a buttonbox with the specified choices.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted
      when the gui appears
    :param str cancel_choice: If the user presses the 'X' close,
      which button should be pressed
    :return: the index of the choice selected, starting from 0
    """
    reply = bb.buttonbox(msg=msg,
                         title=title,
                         choices=choices,
                         image=image,
                         default_choice=default_choice,
                         cancel_choice=cancel_choice)
    if reply is None:
        return None
    for i, choice in enumerate(choices):
        if reply == choice:
            return i
    msg = ("There is a program logic error in the EasyGui code "
           "for indexbox.\nreply={0}, choices={1}".format(
               reply, choices))
    raise AssertionError(msg)


# -----------------------------------------------------------------------
# msgbox
# -----------------------------------------------------------------------
def msgbox(msg="(Your message goes here)", title=" ",
           ok_button="OK", image=None, root=None):
    """
    Display a message box

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str ok_button: text to show in the button
    :param str image: Filename of image to display
    :param tk_widget root: Top-level Tk widget
    :return: the text of the ok_button
    """
    if not isinstance(ok_button, ut.basestring):
        raise AssertionError(
            "The 'ok_button' argument to msgbox must be a string.")

    return bb.buttonbox(msg=msg,
                        title=title,
                        choices=[ok_button],
                        image=image,
                        root=root,
                        default_choice=ok_button,
                        cancel_choice=ok_button)


# -------------------------------------------------------------------
# integerbox
# -------------------------------------------------------------------
def integerbox(msg="", title=" ", default="",
               lowerbound=0, upperbound=99, image=None, root=None):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default argument may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str default: The default value to return
    :param int lowerbound: The lower-most value allowed
    :param int upperbound: The upper-most value allowed
    :param str image: Filename of image to display
    :param tk_widget root: Top-level Tk widget
    :return: the integer value entered by the user

    """

    if not msg:
        msg = "Enter an integer between {0} and {1}".format(
            lowerbound, upperbound)

    # Validate the arguments for default, lowerbound and upperbound and
    # convert to integers
    exception_string = (
        'integerbox "{0}" must be an integer.  It is >{1}< of type {2}')
    if default:
        try:
            default = int(default)
        except ValueError:
            raise ValueError(
                exception_string.format('default', default, type(default)))
    try:
        lowerbound = int(lowerbound)
    except ValueError:
        raise ValueError(
            exception_string.format('lowerbound',
                                    lowerbound, type(lowerbound)))
    try:
        upperbound = int(upperbound)
    except ValueError:
        raise ValueError(
            exception_string.format('upperbound',
                                    upperbound, type(upperbound)))

    while True:
        reply = enterbox(msg, title, str(default), image=image, root=root)
        if reply is None:
            return None
        try:
            reply = int(reply)
        except:
            msgbox('The value that you entered:\n\t"{}"\nis not an integer.'
                   .format(reply), "Error")
            continue
        if reply < lowerbound:
            msgbox('The value that you entered is less than the lower '
                   'bound of {}.'.format(lowerbound), "Error")
            continue
        if reply > upperbound:
            msgbox('The value that you entered is greater than the upper bound'
                   ' of {}.'.format(
                       upperbound), "Error")
            continue
        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
        return reply


# -------------------------------------------------------------------
# multenterbox
# -------------------------------------------------------------------
# TODO RL: Should defaults be list constructors.
# i think after multiple calls, the value is retained.
# TODO RL: Rename/alias to multienterbox?
# default should be None and then in the logic create an empty list.
def multenterbox(msg="Fill in values for the fields.", title=" ",
                 fields=(), values=()):
    r"""
    Show screen with multiple data entry fields.

    If there are fewer values than names, the list of values is padded with
    empty strings until the number of values is the same as the number
    of names.

    If there are more values than names, the list of values
    is truncated so that there are as many values as names.

    Returns a list of the values of the fields,
    or None if the user cancels the operation.

    Here is some example code, that shows how values returned from
    multenterbox can be checked for validity before they are accepted::

        msg = "Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues is None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "":
                break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        print("Reply was: %s" % str(fieldValues))

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :return: String
    """
    return bb.__multfillablebox(msg, title, fields, values, None)


# -----------------------------------------------------------------------
# multpasswordbox
# -----------------------------------------------------------------------
def multpasswordbox(msg="Fill in values for the fields.",
                    title=" ", fields=tuple(), values=tuple()):
    r"""
    Same interface as multenterbox.  But in multpassword box,
    the last of the fields is assumed to be a password, and
    is masked with asterisks.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :return: String

    **Example**

    Here is some example code, that shows how values returned from
    multpasswordbox can be checked for validity before they are accepted::

        msg = "Enter logon information"
        title = "Demo of multpasswordbox"
        fieldNames = ["Server ID", "User ID", "Password"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multpasswordbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues is None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' %
                     fieldNames[i])
                if errmsg == "": break # no problems found
            fieldValues = multpasswordbox(errmsg, title,
              fieldNames, fieldValues)

        print("Reply was: %s" % str(fieldValues))

    """
    return bb.__multfillablebox(msg, title, fields, values, "*")


# -------------------------------------------------------------------
# enterbox
# -------------------------------------------------------------------
def enterbox(msg="Enter something.", title=" ", default="",
             strip=True, image=None, root=None):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Example::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :param bool strip: If True, the return value will have
      its whitespace stripped before being returned
    :return: the text that the user entered, or None if he cancels
      the operation.
    """
    result = bb.__fillablebox(
        msg, title, default=default, mask=None, image=image, root=root)
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password.", title=" ", default="",
                image=None, root=None):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :return: the text that the user entered, or None if he cancels
      the operation.
    """
    return bb.__fillablebox(msg, title, default, mask="*",
                            image=image, root=root)


# -------------------------------------------------------------------
# multchoicebox
# -------------------------------------------------------------------
def multchoicebox(msg="Pick as many items as you like.", title=" ",
                  choices=(), **kwargs):
    """
    Present the user with a list of choices.
    allow him to select multiple items and return them in a list.
    if the user doesn't choose anything from the list, return the empty list.
    return None if he cancelled selection.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :return: List containing choice selected or None if cancelled

    """
    if len(choices) == 0:
        choices = ["Program logic error - no choices were specified."]

    global __choiceboxMultipleSelect
    __choiceboxMultipleSelect = 1
    return bb.__choicebox(msg, title, choices)


# -----------------------------------------------------------------------
# choicebox
# -----------------------------------------------------------------------
def choicebox(msg="Pick something.", title=" ", choices=()):
    """
    Present the user with a list of choices.
    return the choice that he selects.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :return: List containing choice selected or None if cancelled
    """
    if len(choices) == 0:
        choices = ["Program logic error - no choices were specified."]

    global __choiceboxMultipleSelect
    __choiceboxMultipleSelect = 0
    return bb.__choicebox(msg, title, choices)


# -----------------------------------------------------------------------
# exceptionbox
# -----------------------------------------------------------------------
def exceptionbox(msg=None, title=None):
    """
    Display a box that gives information about
    an exception that has just been raised.

    The caller may optionally pass in a title for the window, or a
    msg to accompany the error information.

    Note that you do not need to (and cannot) pass an exception object
    as an argument.  The latest exception will automatically be used.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :return: None

    """
    if title is None:
        title = "Error Report"
    if msg is None:
        msg = "An error (exception) has occurred in the program."

    codebox(msg, title, ut.exception_format())


# -------------------------------------------------------------------
# codebox
# -------------------------------------------------------------------

def codebox(msg="", title=" ", text=""):
    """
    Display some text in a monospaced font, with no line wrapping.
    This function is suitable for displaying code and text that is
    formatted using spaces.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    """
    return tb.textbox(msg, title, text, codebox=1)
