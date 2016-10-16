"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

try:
    from .button_box_view import GUItk
    from .button_box_choices import Choices
    from .button_box_validations import ValidateImages, validate_msg
    from .button_box_controller import BoxController
except (SystemError, ValueError, ImportError):
    from button_box_view import GUItk
    from button_box_choices import Choices
    from button_box_validations import ValidateImages, validate_msg
    from button_box_controller import BoxController


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
    :param str images: Filename of image or iterable or iterable of iterable to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param function callback: A callback function to be called when a choice button is pressed
    :return: the text of the button that the user selected, or the value if it was a dictionary

    """

    model = BoxModel(msg, title, choices, image, images, default_choice, cancel_choice, callback)

    reply = model.run()

    return reply


class BoxModel(object):
    """ Display various types of button boxes

    This object separates user from ui, also deals with callback if required.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.
    """

    """
    Stores, transforms and validates all data specific to this call
    """
    def __init__(self, msg, title, input_choices, image, images, default_choice, cancel_choice, callback):
        self.title = title
        self.msg = validate_msg(msg)
        self.choices = Choices(input_choices, default_choice, cancel_choice)
        self.images = ValidateImages().run(image, images)

        self.selected_row_column = None
        self.changed_msg = False
        self.stop = False

        self.callback = callback

        # Set the window, don't show it yet
        self.view = GUItk(self)

    def run(self):
        """ Show the window and wait """
        self.view.run()
        # The window is closed
        return self.choices.selected_choice.result

    def check_callback_updated(self):
        # If there is no callback close ui and return choice

        if not self.callback:
            self.stop = True

        else:
            # If there is callback to the main program
            # Prepare the callback
            cb_interface = CallBackInterface(self.choices.selected_choice.result, self.selected_row_column)

            # call back main program
            self.callback(cb_interface)

            # Update model
            self.stop = cb_interface._stop
            if cb_interface._changed_msg:
                self.changed_msg = True
                self.msg = cb_interface._msg

        self.model_updated()

    def model_updated(self):
        self.view.update_view()


class CallBackInterface(object):
    """
    This object is passed to the user with the callback, so the user can
    know the choice selected, the image selected, and also the user can
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




