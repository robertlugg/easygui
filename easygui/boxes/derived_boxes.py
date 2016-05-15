"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

"""

try:
    from .fillable_box import __fillablebox
    from .button_box import buttonbox
    from . import text_box as tb
    from . import utils as ut
except (SystemError, ValueError, ImportError):
    from fillable_box import __fillablebox
    from button_box import buttonbox
    import text_box as tb
    import utils as ut

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

    reply = buttonbox(msg=msg,
                      title=title,
                      choices=choices,
                      image=image,
                      default_choice=default_choice,
                      cancel_choice=cancel_choice)
    if reply is None:
        return None
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
    reply = buttonbox(msg=msg,
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

    return buttonbox(msg=msg,
                     title=title,
                     choices=[ok_button],
                     image=image,
                     default_choice=ok_button,
                     cancel_choice=ok_button)


def convert_to_type(input_value, new_type, input_value_name=None):
    """
    Attempts to convert input_value to type new_type and throws error if it can't.

    If input_value is None, None is returned
    If new_type is None, input_value is returned unchanged
    :param input_value: Value to be converted
    :param new_type: Type to convert to
    :param input_value_name: If not None, used in error message if input_value cannot be converted
    :return: input_value converted to new_type, or None
    """
    if input_value is None or new_type is None:
        return input_value

    exception_string = (
        'value {0}:{1} must be of type {2}.')
    ret_value = new_type(input_value)
#        except ValueError:
#            raise ValueError(
#                exception_string.format('default', default, type(default)))
    return ret_value


# -------------------------------------------------------------------
# integerbox
# -------------------------------------------------------------------
def integerbox(msg="", title=" ", default=None,
               lowerbound=0, upperbound=99, image=None, root=None):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default, lowerbound, or upperbound may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param int default: The default value to return
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
    default = convert_to_type(default, int, "default")
    lowerbound = convert_to_type(lowerbound, int, "lowerbound")
    upperbound = convert_to_type(upperbound, int, "upperbound")

    while True:
        reply = enterbox(msg, title, default, image=image, root=root)
        if reply is None:
            return None
        try:
            reply = convert_to_type(reply, int)
        except ValueError:
            msgbox('The value that you entered:\n\t"{}"\nis not an integer.'.format(reply), "Error")
            continue
        if lowerbound is not None:
            if reply < lowerbound:
                msgbox('The value that you entered is less than the lower bound of {}.'.format(lowerbound), "Error")
                continue
        if upperbound is not None:
            if reply > upperbound:
                msgbox('The value that you entered is greater than the upper bound of {}.'.format(upperbound), "Error")
                continue
        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
        break
    return reply







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
    result = __fillablebox(
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
    return __fillablebox(msg, title, default, mask="*",
                         image=image, root=root)


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
    return tb.textbox(msg, title, text, codebox=True)
