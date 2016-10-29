"""
.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

try:
    from .button_box_view import ViewTk
    from .button_box_choices import Choices
    from . import button_box_validations as validations
    from . import global_state
except (SystemError, ValueError, ImportError):
    from button_box_view import ViewTk
    from button_box_choices import Choices
    import global_state
    import button_box_validations as validations


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
    :param list, tuple, dict choices: a list or tuple of the choices to be displayed
    :param str image: (Only here for backward compatibility)
    :param str, list images: Filename of image or iterable or iterable of iterable to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: This choice will close the window, justa as Escape key or x
    :param function callback: A callback function to be called when a choice button is pressed
    :return: the text of the button that the user selected, or the value if it was a dictionary

    """

    model = ButtonBoxModel(msg, title, choices, image, images, default_choice, cancel_choice, callback)

    reply = model.run()

    return reply


class ButtonBoxModel(object):
    """
    This object separates user from view, also deals with the callback if required.

    It also calls the view in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.

    First we validate user data, creating a choice abstract data class.
    Then we create the view object.
    The communication is as follows:
        - The view object uses the data in the model to display itself
        - When a defined event fires in the view (eg: a button is pressed), the corresponding method
          **of the model** is called
        - The model calls the following view methods: run, stop, get_position_on_screen and set_msg

    """

    def __init__(self, msg, title, input_choices, image, images, default_choice, cancel_choice, callback):

        # Validation of user data

        # First, create a notification object for errors on validation
        notification = Notification()

        self.title = validations.validate_or_convert_to_string(title, notification)

        self.msg = validations.validate_or_convert_to_string(msg, notification)

        self.choices = Choices(input_choices, default_choice, cancel_choice, notification)

        self.images = validations.validate_images(image, images, notification)

        if notification.errors:
            # Show errors on console
            print(notification.as_string())
            # Show errors on the window.
            self.msg += notification.as_string()

        # Get callback
        self.callback = callback

        # Initialize other
        self.selected_row_column = None

        # Set the window, don't show it yet
        # The view recieves self, the model object,
        # So it can access its data and fire methods on events
        self.view = ViewTk(self)

        # Configure the window, using the initial or saved window position
        # (depending on if this is a first window or not)
        # It also receives global parameters to set the window width
        self.view.configure(global_state.window_position,
                            global_state.fixw_font_line_length,
                            global_state.default_hpad_in_chars)

    def run(self):
        """ This shows the window and waits for events """
        self.view.run()
        # The next line is executed after the window is destroyed
        return self.choices.selected_choice.result

    # Methods executing when a key is pressed in the view -------------------------------
    # If cancel, x, or escape, close ui and return None
    def x_pressed(self):
        self.select_nothing()
        self.stop_view()

    def escape_pressed(self, event):
        self.select_nothing()
        self.stop_view()

    def button_or_hotkey_pressed(self, choice):
        # If cancel, finish and return None
        if choice.is_cancel:
            self.select_nothing()
            self.stop_view()
        else:
            # So there has been a choice selected
            self.select_choice(choice)
            if not self.callback:
                self.stop_view()
            else:
                self.call_callback()

    def image_pressed(self, filename, row, column):
        self.select_nothing()
        self.select_row_column(row, column)
        if not self.callback:
            self.stop_view()
        else:
            self.call_callback()

    # Methods called by the methods defined before
    # They affect choices, call back to user or call View methods
    def select_choice(self, choice):
        self.choices.selected_choice = choice

    def select_row_column(self, row, column):
        self.selected_row_column = (row, column)

    def call_callback(self):
        # Prepare the callback interface
        cb_interface = CallBackInterface(self.choices.selected_choice.result, self.selected_row_column)

        # call back main program
        self.callback(cb_interface)

        # Update view on callback result
        if cb_interface._stop:
            self.stop_view()
        elif cb_interface._changed_msg:
            notification = Notification()
            self.msg = validations.validate_or_convert_to_string(cb_interface._msg, notification)
            print(notification.as_string())
            self.msg += notification.as_string()
            self.view.set_msg(cb_interface._msg)

    def select_nothing(self):
        self.choices.unselect_choice()
        self.selected_row_column = None

    def stop_view(self):
        position = self.view.get_position_on_screen()
        global_state.window_position = position
        self.view.stop()


class CallBackInterface(object):
    """
    This object is passed to the user with the callback, so the user can
    know the choice selected, the image selected. Also the user can
    send a command to stop the gui or change its message.

    This object defines and limits what the user can do in the callback.
    """

    def __init__(self, selected_choice, selected_row_column):
        self._msg = None
        self._changed_msg = False
        self._stop = False
        self._selected_choice = selected_choice
        self._selected_row_column = selected_row_column

    def set_msg(self, msg):
        self._msg = msg
        self._changed_msg = True

    def stop(self):
        self._stop = True

    def get_selected_choice(self):
        return self._selected_choice

    def get_selected_row_column(self):
        return self._selected_row_column


class Notification(object):
    """
    This object holds validation error messages
    """
    def __init__(self):
        self.errors = []

    def add_error(self, error_msg):
        self.errors.append(error_msg)

    def as_string(self):
        string = '\n'.join(self.errors)
        return string