"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

from easygui.boxes.button_box_guitk import GUItk
from easygui.boxes.button_box_validations import Validations


def buttonbox(msg="",
              title=" ",
              choices=("Button[1]", "Button[2]", "Button[3]"),
              image=None,
              images=None,
              default_choice=None,
              cancel_choice=None,
              callback=None,
              run=True):
    """
    Display a msg, a title, an image, and a set of buttons.
    The buttons are defined by the members of the choices global_state.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: (Only here for backward compatibility)
    :param str images: Filename of image or iterable or iterable of iterable to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :return: the text of the button that the user selected



    """
    validations = Validations()
    images = validations.validate_images(image, images)
    images = validations.images_to_matrix(images)
    bb = ButtonBox(
            msg=msg,
            title=title,
            choices=choices,
            images=images,
            default_choice=default_choice,
            cancel_choice=cancel_choice,
            callback=callback,
            validations=validations)

    reply = bb.run()

    return reply


class ButtonBox(object):
    """ Display various types of button boxes

    This object separates user from ui, defines which methods can
    the user invoke and which properties can he change.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.
    """

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback, validations):
        """ Create box object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        choices : iterable of strings
            build a button for each string in choices
        images : iterable of filenames, or an iterable of iterables of filenames
            displays each image
        default_choice : string
            one of the strings in choices to be the default selection
        cancel_choice : string
            if X or <esc> is pressed, it appears as if this button was pressed.
        callback: function
            if set, this function will be called when any button is pressed.

        Returns
        -------
        object
            The box object
        """

        self.callback = callback
        self.cancel_choice = cancel_choice
        self.choices_dict, choices_list = validations.convert_choices_to_dict(choices)
        self.choice_selected = None

        # Set the window, don't show it
        self.cb_interface = CallBackInterface()
        self.ui = GUItk(msg, title, choices_list, images, default_choice, cancel_choice, self.update)

    def run(self):
        """ Show the window and wait """
        self.ui.run()
        # The window is closed
        self.ui = None
        return self.choice_selected


    def update(self, command, choice_selected, row_column_selected):
        """ This method is executed when any buttons or x are pressed in the ui.
        """
        self.select_choice(choice_selected)

        self.row_column_selected = row_column_selected

        self.cb_interface.row_column_selected = self.row_column_selected
        self.cb_interface.choice_selected = self.choice_selected
        self.cb_interface.msg = None

        if command == 'update':  # Any button was pressed
            if self.callback:
                # If a callback was set, call main process
                self.callback(self.cb_interface)
            else:
                self.cb_interface.stop = True
        elif command == 'x':
            self.choice_selected = None
            self.cb_interface.stop = True
        elif command == 'cancel':
            self.choice_selected = None
            self.cb_interface.stop = True

        return self.cb_interface.stop, self.cb_interface.msg

    def select_choice(self, choice_selected):
        try:
            self.choice_selected = self.choices_dict[choice_selected]
        except:
            self.choice_selected = None


class CallBackInterface(object):
    choice_selected = None
    row_column_selected = None
    stop = False
    msg = None


