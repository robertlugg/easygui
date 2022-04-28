import tkinter as tk

from easygui import msgbox
from easygui.global_state import PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE, \
    TEXT_ENTRY_FONT_SIZE
from easygui.utilities import load_tk_image, MouseClickHandler, AbstractBox


def integerbox(msg=None, title=" ", default=None, lowerbound=0, upperbound=99, image=None, root=None):
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
        result = FillableBox(msg, default, title, image=image, root=root).run()
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


def enterbox(msg="Enter something.", title=" ", default="", strip=True, image=None, root=None):
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
    result = FillableBox(msg, default, title, image=image, root=root).run()
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password.", title="", default="", image=None, root=None):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :return: the text that the user entered, or None if they cancel
      the operation.
    """
    return FillableBox(msg, default, title, mask="*", image=image, root=root).run()


def fillablebox(msg, title="", default=None, mask=None, image=None, root=None):
    """
    Show a box in which a user can enter some text.
    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: default value populated, returned if user does not change it
    :return: the text that the user entered, or None if he cancels the operation.
    """
    return FillableBox(msg, default, title, mask, image, root).run()


class FillableBox(AbstractBox):
    def __init__(self, msg, title, default, mask=None, image=None, root=None):
        if root:
            root.withdraw()
            self.box_root = tk.Toplevel(master=root)
            self.box_root.withdraw()
        super().__init__(msg, title)
        self.return_value = '' if default is None else default
        self.pre_existing_root = root
        self.entry_widget = None

        message_frame = tk.Frame(master=self.box_root)
        message_frame.pack(side=tk.TOP, fill=tk.BOTH)

        try:
            tk_image = load_tk_image(image)
        except Exception as e:
            print(e)
            tk_image = None
        if tk_image:
            image_frame = tk.Frame(master=self.box_root)
            image_frame.pack(side=tk.TOP, fill=tk.BOTH)
            label = tk.Label(image_frame, image=tk_image)
            label.image = tk_image  # keep a reference!
            label.pack(side=tk.TOP, expand=tk.YES, fill=tk.X, padx='1m', pady='1m')

        buttons_frame = tk.Frame(master=self.box_root)
        buttons_frame.pack(side=tk.TOP, fill=tk.BOTH)

        entry_frame = tk.Frame(master=self.box_root)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH)

        buttons_frame = tk.Frame(master=self.box_root)
        buttons_frame.pack(side=tk.TOP, fill=tk.BOTH)

        message_widget = tk.Message(message_frame, width="4.5i", text=msg)
        message_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        message_widget.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH, padx='3m', pady='3m')

        entry_widget = tk.Entry(entry_frame, width=40)
        entry_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
        if mask:
            entry_widget.configure(show=mask)
        entry_widget.pack(side=tk.LEFT, padx="3m")
        entry_widget.bind("<Return>", self._ok_pressed)
        entry_widget.bind("<Escape>", self.cancel_button_pressed)
        entry_widget.insert(0, self.return_value)  # put text into the entry_widget
        self.entry_widget = entry_widget  # save a reference - we need to get text from this widget later

        ok_button = tk.Button(buttons_frame, takefocus=1, text="OK")
        ok_button.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        ok_button.bind("<Return>", self._ok_pressed)
        ok_click_handler = MouseClickHandler(callback=self._ok_pressed)
        ok_button.bind("<Enter>", ok_click_handler.enter)
        ok_button.bind("<Leave>", ok_click_handler.leave)
        ok_button.bind("<ButtonRelease-1>", ok_click_handler.release)

        cancel_button = tk.Button(buttons_frame, takefocus=1, text="Cancel")
        cancel_button.pack(expand=1, side=tk.RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        cancel_button.bind("<Escape>", self.cancel_button_pressed)
        cancel_click_handler = MouseClickHandler(callback=self.cancel_button_pressed)
        cancel_button.bind("<Enter>", cancel_click_handler.enter)
        cancel_button.bind("<Leave>", cancel_click_handler.leave)
        cancel_button.bind("<ButtonRelease-1>", cancel_click_handler.release)

        self.entry_widget.focus_force()  # put the focus on the self.entry_widget
        self.box_root.deiconify()

    def _ok_pressed(self, *args):
        self.return_value = self.entry_widget.get()
        self.box_root.quit()

    def run(self):
        self.box_root.mainloop()  # run it!

        # -------- after the run has completed ----------------------------------
        if self.pre_existing_root:
            self.pre_existing_root.deiconify()
        self.box_root.destroy()  # button_click didn't destroy self.boxRoot, so we do it now
        return self.return_value
