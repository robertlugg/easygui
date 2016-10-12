"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

try:
    from .button_box_guitk import GUItk
    from .button_box_validations import validate_images, images_to_matrix, convert_choices_to_dict, validate_msg
except (SystemError, ValueError, ImportError):
    from button_box_guitk import GUItk
    from button_box_validations import validate_images, images_to_matrix, convert_choices_to_dict, validate_msg


def buttonbox(msg="",
              title=" ",
              choices=("Button[1]", "Button[2]", "Button[3]"),
              image=None,
              images=None,
              default_choice=None,
              cancel_choice=None,
              callback=None
              ):
    """
    Display a msg, a title, an image, and a set of buttons.
    The buttons are defined by the members of the choices global_state.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: (Only here for backward compatibility)
    :param str images: Filename of image or iterable or iterable of iterable to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param function callback: A callback function to be called when a choice button ois pressed
    :return: the text of the button that the user selected

    """

    images = validate_images(image, images)
    images = images_to_matrix(images)
    choices_dict = convert_choices_to_dict(choices)
    msg = validate_msg(msg)
    cb_interface = CallBackInterface()

    bb = ButtonBox(
            msg=msg,
            title=title,
            choices=choices_dict,
            images=images,
            default_choice=default_choice,
            cancel_choice=cancel_choice,
            callback=callback,
            cb_interface = cb_interface)

    reply = bb.run()

    return reply


class ButtonBox(object):
    """ Display various types of button boxes

    This object separates user from ui, also dealss with callback if required.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.
    """

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback, cb_interface):
        """ Create box object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        choices : dictionary
            build a button for each key in choices
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

        self.cancel_choice = cancel_choice
        self.choice_selected = None
        self.choices = choices
        choices_list = choices.keys()

        self.callback = callback
        self.cb_interface = cb_interface

        # Set the window, don't show it yet
        self.ui = GUItk(msg, title, choices_list, images, default_choice, cancel_choice, self.update)

    def run(self):
        """ Show the window and wait """
        self.ui.run()
        # The window is closed
        self.ui = None
        return self.choice_selected


    def update(self, command, choice_selected, row_column_selected):
        """
        This method is executed when any buttons or x are pressed in the ui.

        It decides weheter or not terminate the ui, what return values should be given to the caller of buttonbox,
        and it calls the callback if necessary.
        """
        ui_stop_command = False
        ui_change_message = False

        try:
            self.choice_selected = self.choices[choice_selected]
        except:
            self.choice_selected = None

        self.row_column_selected = row_column_selected

        if command == 'update':  # Any button was pressed

            # Cancel pressed
            if choice_selected == self.cancel_choice:
                self.choice_selected = None
                ui_stop_command = True

            # Any other button with callback
            else:
                if self.callback:
                    self.cb_interface._selected_row_column = self.row_column_selected
                    self.cb_interface._selected_choice = self.choice_selected
                    self.cb_interface._msg = None
                    # If a callback was set, call main process
                    self.callback(self.cb_interface)
                    ui_stop_command = self.cb_interface._stop
                    ui_change_message = self.cb_interface._msg

                # Any other button without callback
                else:
                    ui_stop_command = True

        # The x button on the window was pressed
        elif command == 'x':
            self.choice_selected = None
            ui_stop_command = True

        # The escape key was pressed
        elif command == 'escape':
            self.choice_selected = None
            ui_stop_command = True

        # Returns to the ui, with feedback from the main program
        return ui_stop_command, ui_change_message



class CallBackInterface(object):
    """
    This object is passed to the user with the callback, so the user can
    know the choice selected, the image selected, and also the user can
    send a message to stop the gui or change its message

    This object defines and limits what the user can do in the callback.
    """

    def __init__(self):
        self._msg = None
        self._stop = False
        self._selected_choice = None
        self._selected_row_column = None

    def set_msg(self, msg):
        self._msg = msg

    def stop(self):
        self._stop = True

    def get_selected_choice(self):
        return self._selected_choice

    def get_selected_row_column(self):
        return self._selected_row_column