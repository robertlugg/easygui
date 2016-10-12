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

    model = BoxModel(msg, title, choices, image, images, default_choice, cancel_choice)

    cb_interface = CallBackInterface()

    # Set the window, don't show it yet
    view = GUItk(model.msg, model.title, model.choices_list, model.images, model.default_choice, model.cancel_choice)

    controller = BoxController(model, callback, cb_interface, view)

    view.callback_on_update = controller.on_view_event

    reply = controller.run()

    return reply


class BoxModel(object):
    """
    Stores, transforms and validates all data specific to this call
    """
    def __init__(self, msg, title, choices, image, images, default_choice, cancel_choice):
        self.title = title
        self.msg = validate_msg(msg)
        self.choices_dict = convert_choices_to_dict(choices)
        self.choices_list = self.choices_dict.keys()
        imgs = validate_images(image, images)
        self.images = images_to_matrix(imgs)
        self.default_choice = default_choice
        self.cancel_choice = cancel_choice

        self.selected_choice = None
        self.selected_row_column = None

    def select_choice(self, choice):
        try:
            self.selected_choice = self.choices_dict[choice]
        except:
            self.selected_choice = None


class BoxController(object):
    """ Display various types of button boxes

    This object separates user from ui, also deals with callback if required.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.
    """

    def __init__(self, model, callback, cb_interface, view):
        """
        :param object model: holds the data of this call
        :param function callback: if set, this function will be called when any button is pressed.
        """

        self.model = model
        self.callback = callback
        self.cb_interface = cb_interface
        self.view = view

    def run(self):
        """ Show the window and wait """
        self.view.run()
        # The window is closed
        self.view = None
        return self.model.selected_choice

    def on_view_event(self, received):
        """
        This method is executed when any buttons, keys or x are pressed in the view.

        It decides whether or not terminate the ui, what return values should be given to the caller of buttonbox,
        and it calls the callback if necessary.
        """
        response_to_view = ResponseToView()

        # If cancel, x, or escape, close ui and return None
        cancel_presed = (received.event == 'update' and received.selected_choice_as_text == self.model.cancel_choice)
        x_pressed = (received.event == 'x')
        escape_pressed = (received.event == 'escape')

        if cancel_presed or x_pressed or escape_pressed:
            self.model.select_choice(None)
            self.model.row_column_selected = None
            response_to_view.stop = True
            return response_to_view

        # Else, a button different from escape was pressed

        # So there has been a choice selected
        self.model.select_choice(received.selected_choice_as_text)
        self.model.row_column_selected = received.selected_choice_row_column

        # If there is no callback close ui and return choice
        if not self.callback:
            response_to_view.stop = True
            return response_to_view

        # If there is callback to the main program

        # Prepare the callback

        self.cb_interface._selected_row_column = self.model.row_column_selected
        self.cb_interface._selected_choice = self.model.selected_choice
        self.cb_interface._msg = None

        # call back main program
        self.callback(self.cb_interface)

        response_to_view.stop = self.cb_interface._stop
        response_to_view.msg = self.cb_interface._msg

        return response_to_view


class CallBackInterface(object):
    """
    This object is passed to the user with the callback, so the user can
    know the choice selected, the image selected, and also the user can
    send a command to stop the gui or change its message.

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


class ResponseToView(object):
    """ Object passed from controller to view after each update"""
    def __init__(self):
        self.stop = None
        self.msg = None

