import tkinter as tk

from easygui.utilities import load_tk_image, get_width_and_padding, parse_hotkey, AbstractBox


def buttonbox(msg="buttonbox options", title=" ", choices=("Button[1]", "Button[2]", "Button[3]"),
              image=None, images=None, default_choice=None, cancel_choice=None,
              callback=None, run=True):
    """ Display a message, a title, an image, and a set of buttons.
    The buttons are defined by the members of the choices argument.
    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: (Only here for backward compatibility)
    :param str images: Filename of image or iterable or iteratable of iterable to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param cancel_choice:
    :param callback:
    :param run:
    :return: the text of the button that the user selected OR the buttonbox object if run was False
    """
    if image and images:
        raise ValueError("Cannot run buttonbox() with both 'image' and 'images' - pick one!")
    if image:
        images = image
    bb = ButtonBox(
        msg=msg,
        title=title,
        choices=choices,
        images=images,
        default_choice=default_choice,
        cancel_choice=cancel_choice,
        callback=callback)
    return bb.run() if run else bb


def boolbox(msg="[T]rue or [F]alse?", title=" ", choices=("[T]rue", "[F]alse"), image=None,
            default_choice='[T]rue', cancel_choice='[F]alse'):
    """
    Display a boolean dialog window with True/False options.

    The function returns `True` if the first button is selected, and returns
    `False` if the second button is selected. The function returns `None`
    if the user closes the dialog window.

    :param str msg: The message shown in the center of the dialog window.
    :param str title: The window title text.
    :param list choices: A list or tuple of strings for the buttons' text.
    :param str image: The filename of an image to display in the dialog window.
    :param str default_choice: The text of the default selected button.
    :param str cancel_choice: If the user presses the 'X' close, which button
      should be pressed
    :return: `True` if first button pressed, `False` if second button is pressed, or None if the window was cancelled.
    """

    if len(choices) != 2:
        raise AssertionError('boolbox takes exactly 2 choices!  Consider using indexbox instead')

    reply = buttonbox(msg, title, choices, image, default_choice=default_choice, cancel_choice=cancel_choice)
    if reply == choices[0]:
        return True  # The first button (True) was selected.
    elif reply == choices[1]:
        return False  # The second button (False) was selected.
    elif reply is None:
        return None  # The window was closed.


def ynbox(msg="Yes <F1> or No <F2>?", title=" ", choices=("[<F1>]Yes", "[<F2>]No"), image=None,
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
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: True if 'Yes', False if 'No', None if dialog was cancelled
    """
    return boolbox(msg, title, choices, image, default_choice=default_choice, cancel_choice=cancel_choice)


def ccbox(msg="C[o]ntinue or C[a]ncel?", title=" ", choices=("C[o]ntinue", "C[a]ncel"), image=None,
          default_choice='C[o]ntinue', cancel_choice='C[a]ncel'):
    """
    The ``ccbox()`` function offers a choice of Continue (returns True) and Cancel (returns False)

        import easygui
        if easygui.ccbox("Do you want to continue?", "Please Confirm"):
            pass  # User chose Continue.
        else:  # User chose Cancel.
            sys.exit()

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: True if 'Continue' or dialog is cancelled, False if 'Cancel'
    """
    return boolbox(msg, title, choices, image, default_choice=default_choice, cancel_choice=cancel_choice)


def indexbox(msg="Options: ", title=" ", choices=("Door 1", "Door 2", "Door 3"), image=None,
             default_choice='Door 1', cancel_choice='Door 3'):
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
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: the index of the choice selected, starting from 0
    """
    reply = buttonbox(msg, title, choices, image, default_choice=default_choice, cancel_choice=cancel_choice)
    try:
        return list(choices).index(reply)
    except ValueError:
        msg = ("EasyGui indexbox could not determine the index of choice {} in choices {}.".format(reply, choices))
        raise AssertionError(msg)


def msgbox(msg="(Your message goes here)", title=" ", ok_button="OK", image=None):
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
    :return: the text of the ok_button
    """
    return buttonbox(msg, title, choices=[ok_button], image=image, default_choice=ok_button, cancel_choice=ok_button)


class ButtonBox(AbstractBox):
    """ Display various types of button boxes

    This object separates user from ui, defines which methods can
    the user invoke and which properties can he change.
    """

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback):
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

        """

        super().__init__(msg, title, callback)
        self._text_to_return_on_cancel = cancel_choice
        self.return_value = None
        self._images = []
        self._buttons = []

        self.message_area = self._configure_message_area(box_root=self.box_root)
        self._set_msg_area('' if msg is None else msg)
        self.images_frame = self._create_images_frame(images)
        self.buttons_frame = self._create_buttons_frame(choices, default_choice)

    @staticmethod
    def _configure_message_area(box_root):
        padding, width_in_chars = get_width_and_padding(monospace=False)
        message_frame = tk.Frame(box_root, padx=padding)
        message_frame.grid()
        message_area = tk.Text(master=message_frame, width=width_in_chars, padx=padding, pady=padding, wrap=tk.WORD)
        message_area.grid()
        return message_area

    @staticmethod
    def _convert_to_a_list_of_lists(filenames):
        """ return a list of lists, handling all of the different allowed types of 'filenames' input """
        if type(filenames) is str:
            return [[filenames, ], ]
        elif type(filenames[0]) is str:
            return [filenames, ]
        elif type(filenames[0][0]) is str:
            return filenames
        raise ValueError("Incorrect images argument.")

    def _create_images_frame(self, filenames):
        images_frame = tk.Frame(self.box_root)
        row = 1
        images_frame.grid(row=row)
        self.box_root.rowconfigure(row, weight=10, minsize='10m')

        if filenames is None:
            return

        filename_array = self._convert_to_a_list_of_lists(filenames)
        for row, list_of_filenames in enumerate(filename_array):
            for column, filename in enumerate(list_of_filenames):
                try:
                    tk_image = load_tk_image(filename, tk_master=images_frame)
                except Exception as e:
                    print(e)
                    tk_image = None
                widget = tk.Button(
                    master=images_frame,
                    takefocus=1,
                    compound=tk.TOP,
                    image=tk_image,
                    command=lambda text=filename: self._button_pressed(text)
                )
                widget.grid(row=row, column=column, sticky=tk.NSEW, padx='1m', pady='1m', ipadx='2m', ipady='1m')

                image = {'tk_image': tk_image, 'widget': widget}
                images_frame.rowconfigure(row, weight=10, minsize='10m')
                images_frame.columnconfigure(column, weight=10)
                self._images.append(image)  # Prevent image deletion by keeping them on self
        return images_frame

    def _create_buttons_frame(self, choices, default_choice):
        buttons_frame = tk.Frame(self.box_root)
        buttons_frame.grid(row=2)

        for column, button_text in enumerate(choices):
            clean_text, hotkey, hotkey_position = parse_hotkey(button_text)
            widget = tk.Button(
                master=buttons_frame,
                takefocus=1,
                text=clean_text,
                underline=hotkey_position,
                command=lambda text=button_text: self._button_pressed(text)
            )
            widget.grid(row=0, column=column, padx='1m', pady='1m', ipadx='2m', ipady='1m')
            button = {
                'original_text': button_text,
                'clean_text': clean_text,
                'hotkey': hotkey,
                'widget': widget
            }
            buttons_frame.columnconfigure(column, weight=10)
            self._buttons.append(button)

            for button in self._buttons:
                if button['original_text'] == default_choice:
                    button['widget'].focus_force()

                if button['hotkey'] is not None:
                    self.box_root.bind_all(button['hotkey'], lambda e: self._hotkey_pressed(e), add=True)

        return buttons_frame

    # Methods executing when a key is pressed
    def cancel_button_pressed(self, _):
        self.return_value = self._text_to_return_on_cancel
        self.stop()

    def _button_pressed(self, button_text):
        if self._user_specified_callback:
            # If a callback was set, call main process
            self._user_specified_callback()
        else:
            self.stop()
        self.return_value = button_text

    def _hotkey_pressed(self, event=None):
        """ Handle an event that is generated by a person interacting with a button """
        if event.keysym != event.char:  # A special character
            hotkey_pressed = '<{}>'.format(event.keysym)
        else:
            hotkey_pressed = event.keysym

        for button in self._buttons:
            if button['hotkey'] == hotkey_pressed:
                self._callback(command='update')
                self.return_value = button['original_text']

        return  # some key was pressed, but no hotkey registered to it


if __name__ == '__main__':
    buttonbox()
    boolbox()
    ynbox()
    ccbox()
    indexbox()
    msgbox()
