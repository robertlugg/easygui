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
    The ``ynbox()`` offers a choice of Yes and No, and returns either ``True`` or ``False``.

        import easygui
        result = easygui.ynbox('Is a hot dog a sandwich?', 'Hot Dog Question')
        if result == True:
            easygui.msgbox('That is an interesting answer.')
        else:
            easygui.msgbox('Well, that is your opinion.')

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
    The ``ccbox()`` function offers a choice of Continue and Cancel, and returns either True (for continue) or False (for cancel).

        import easygui
        msg = "Do you want to continue?"
        title = "Please Confirm"
        if easygui.ccbox(msg, title):  # Show a Continue/Cancel dialog.
            pass  # User chose Continue.
        else:  # User chose Cancel.
            sys.exit()

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
            choices=("[T]rue", "[F]alse"), image=None,
            default_choice='[T]rue', cancel_choice='[F]alse'):
    """
    The ``boolbox()`` (boolean box) displays two buttons. Returns returns
    ``True`` if the first button is chosen. Otherwise returns ``False``.

        import easygui
        message = "What do they say?"
        title = "Romantic Question"
        if easygui.boolbox(message, title, ["They love me", "They love me not"]):
            easygui.msgbox('You should send them flowers.')
        else:
            easygui.msgbox('It was not meant to be.')

    :param str msg: The message shown in the center of the dialog window.
    :param str title: The window title text.
    :param list choices: A list or tuple of strings for the buttons' text.
    :param str image: The filename of an image to display in the dialog window.
    :param str default_choice: The text of the default selected button.
    :param str cancel_choice: If the user presses the 'X' close, which button
      should be pressed
    :return: `True` if first button pressed or dialog is cancelled, `False`
      if second button is pressed.
    """
    if len(choices) != 2:
        raise AssertionError(
            'boolbox() takes exactly 2 choices!  Consider using indexbox() instead.'
        )

    reply = buttonbox(msg=msg,
                      title=title,
                      choices=choices,
                      image=image,
                      default_choice=default_choice,
                      cancel_choice=cancel_choice)

    if reply == choices[0]:
        return True  # The first button (True) was selected.
    elif reply == choices[1]:
        return False  # The second button (False) was selected.
    elif reply is None:
        return None  # The window was closed.

    assert False, "The user selected an unexpected response."


# -----------------------------------------------------------------------
# indexbox
# -----------------------------------------------------------------------
def indexbox(msg="Shall I continue?", title=" ",
             choices=("Yes", "No"), image=None,
             default_choice='Yes', cancel_choice='No'):
    """
    The ``indexbox()`` function displays a set of buttons, and returns the
    index of the selected button. For example, if you invoked index box with
    three choices (A, B, C), indexbox would return 0 if the user picked A, 1
    if he picked B, and 2 if he picked C.

        import easygui
        result = easygui.indexbox('Which door do you choose?', 'Win Prizes!', choices=['Door 1', 'Door 2', 'Door 3'])
        if result == 2:
            easygui.msgbox('You win a new car!')
        else:
            easygui.msgbox('Better luck next time.')

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
    The ``msgbox()`` function displays a text message and offers an OK
    button. The message text appears in the center of the window, the title
    text appears in the title bar, and you can replace the "OK" default text
    on the button. Here is the signature::

        def msgbox(msg="(Your message goes here)", title="", ok_button="OK"):
            ....

    The clearest way to override the button text is to do it with a keyword
    argument, like this::

        easygui.msgbox("Backup complete!", ok_button="Good job!")

    Here are a couple of examples::

        easygui.msgbox("Hello, world!")

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

        import easygui
        reply = easygui.enterbox('Enter your life story:')
        if reply:
            easygui.msgbox('Thank you for your response.')
        else:
            easygui.msgbox('Your response has been discarded.')

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :param bool strip: If True, the return value will have
      its whitespace stripped before being returned
    :return: the text that the user entered, or None if they cancel
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
    :return: the text that the user entered, or None if they cancel
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
