import tkinter as tk

from easygui import msgbox
from easygui.global_state import PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE, \
    TEXT_ENTRY_FONT_SIZE
from easygui.utilities import load_tk_image, MouseClickHandler, AbstractBox, get_width_and_padding


def integerbox(msg=None, title=" ", default=None, lowerbound=0, upperbound=99, image=None):
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
    msg = "Enter an integer between {0} and {1}".format(lowerbound, upperbound) if msg is None else msg

    while True:
        result = FillableBox(msg, default, title, image=image).run()
        if result is None:
            return None

        try:
            result = int(result)
        except ValueError:
            msgbox('The value that you entered:\n\t"{}"\nis not an integer.'.format(result), "Error")
            continue

        if lowerbound and result < int(lowerbound):
            msgbox('The value that you entered is less than the lower bound of {}.'.format(lowerbound), "Error")
        elif upperbound and result > int(upperbound):
            msgbox('The value that you entered is greater than the upper bound of {}.'.format(upperbound), "Error")
        else:
            return result  # validation passed!


def enterbox(msg="Enter something.", title=" ", default="", strip=True, image=None):
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
    result = FillableBox(msg, default, title, image=image).run()
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password.", title="", default="", image=None):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :return: the text that the user entered, or None if they cancel
      the operation.
    """
    return FillableBox(msg, default, title, mask="*", image=image).run()


def fillablebox(msg, title="", default=None, mask=None, image=None):
    """
    Show a box in which a user can enter some text.
    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: default value populated, returned if user does not change it
    :return: the text that the user entered, or None if he cancels the operation.
    """
    return FillableBox(msg, default, title, mask, image).run()


class FillableBox(AbstractBox):
    def __init__(self, msg, title, default, mask=None, image=None):
        super().__init__(title, callback=None)
        self.return_value = default

        self.configure_image(image)

        self.msg_widget = self.configure_message_widget(monospace=False)
        self.msg = msg

        self.entry_widget = self.conigure_entry_widget(mask)
        self.entry_widget.focus_force()  # put the focus on the self.entry_widget

        self.set_buttons()
        self.box_root.deiconify()

    def conigure_entry_widget(self, mask):
        padding, width_in_chars = get_width_and_padding(monospace=False)
        entry_frame = tk.Frame(master=self.box_root)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH)
        entry_widget = tk.Entry(entry_frame, width=width_in_chars)
        entry_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        if mask:
            entry_widget.configure(show=mask)
        entry_widget.pack(side=tk.LEFT, padx=padding)
        entry_widget.insert(0, self.return_value)  # put text into the entry_widget
        return entry_widget

    def configure_image(self, image):
        image_frame = tk.Frame(master=self.box_root)
        image_frame.pack(side=tk.TOP, fill=tk.BOTH)
        tk_image = load_tk_image(image)
        label = tk.Label(image_frame, image=tk_image)
        label.image = tk_image  # keep a reference!
        label.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1m', pady='1m')

    def _set_return_value(self):
        self.return_value = self.entry_widget.get()


if __name__ == '__main__':
    fillablebox(
        msg="message",
        title="title",
        default="blah",
        mask="*",
        image=".\\..\\demos\\images\\dave.gif"
    )