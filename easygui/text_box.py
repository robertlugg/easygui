import sys
import traceback

import tkinter as tk
from tkinter import font

from easygui.global_state import GLOBAL_WINDOW_POSITION
from easygui.utilities import get_width_and_padding, MouseClickHandler


def textbox(msg='', title='', text='', codebox=False, callback=None, run=True):
    """
    Displays a dialog box with a large, multi-line text box, and returns
    the entered text as a string. The message text is displayed in a
    proportional font and wraps.

    Parameters
    ----------
    msg : string
        text displayed in the message area (instructions...)
    title : str
        the window title
    text: str, list or tuple
        text displayed in textAreas (editable)
    codebox: bool
        if True, don't wrap and width is set to 80 chars
    callback: function
        if set, this function will be called when OK is pressed
    run: bool
        if True, a box object will be created and returned, but not run

    Returns
    -------
    None
        If cancel is pressed
    str
        If OK is pressed returns the contents of textArea.
    TextBox
        If the 'run' argument was False
    """
    tb = TextBox(msg=msg, title=title, text=text, codebox=codebox, callback=callback)
    if run:
        text = tb.run()
        return text
    return tb


def codebox(msg='', title='', text=''):
    """
    Helper method similar to textbox, displays text in a monospaced font which is useful for code.

    The text parameter should be a string, or a list or tuple of lines to be displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    """
    return textbox(msg, title, text, codebox=True)


def exceptionbox(msg='An error (exception) has occurred in the program.', title='Error Report'):
    """ Display a box that gives information about the latest exception that has been raised.

    Display a box that gives information about the latest exception that has been raised.

    The caller may optionally pass in a title for the window, or a msg to accompany the error information.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :return: None"""

    def format_exception_for_display():
        return "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))

    codebox(msg, title, format_exception_for_display())


class TextBox(object):
    """ Display a message, and an editable text field pre-populated with 'text' """

    def __init__(self, msg, title, text, codebox, callback):
        """
        :param msg: str displayed in the message area (instructions...)
        :param title: str used as the window title
        :param text: str displayed in textArea (editable)
        :param codebox: bool (if true) don't wrap, set width to 80 chars, use monospace font
        :param callback: optional function to be called when OK is pressed
        """
        self._user_specified_callback = callback
        self._text = text
        self.msg = msg

        self.box_root = self._configure_box_root(title)
        self.message_area = self._configure_message_area(box_root=self.box_root, code_box=codebox)
        self._set_msg_area("" if msg is None else msg)

        self.MONOSPACE_FONT = font.Font(family='Courier')
        self.text_area = self._configure_text_area(box_root=self.box_root, code_box=codebox)
        self._set_text()
        self._configure_buttons()


    def _configure_box_root(self, title):
        box_root = tk.Tk()
        box_root.title(title)
        box_root.iconname('Dialog')
        box_root.geometry(GLOBAL_WINDOW_POSITION)
        box_root.protocol('WM_DELETE_WINDOW', self.x_pressed)  # Quit when x button pressed
        box_root.bind("<Escape>", self.cancel_button_pressed)
        return box_root

    @staticmethod
    def _configure_message_area(box_root, code_box):
        padding, width_in_chars = get_width_and_padding(code_box)

        message_frame = tk.Frame(box_root, padx=padding)
        message_frame.pack(side=tk.TOP, expand=1, fill='both')

        message_area = tk.Text(master=message_frame,
                               width=width_in_chars,
                               padx=padding,
                               pady=padding,
                               wrap=tk.WORD)
        message_area.pack(side=tk.TOP, expand=1, fill='both')
        return message_area

    def _configure_text_area(self, box_root, code_box):
        padding, width_in_chars = get_width_and_padding(code_box)

        text_frame = tk.Frame(box_root, padx=padding, )
        text_frame.pack(side=tk.TOP)

        text_area = tk.Text(text_frame, padx=padding, pady=padding, height=25, width=width_in_chars)
        text_area.configure(wrap=tk.NONE if code_box else tk.WORD)

        vertical_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_area.xview)
        text_area.configure(xscrollcommand=horizontal_scrollbar.set)

        if code_box:
            text_area.configure(font=self.MONOSPACE_FONT)
            # no word-wrapping for code so we need a horizontal scroll bar
            horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # pack textArea last so bottom scrollbar displays properly
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        box_root.bind("<Next>", text_area.yview_scroll(1, tk.PAGES))
        box_root.bind("<Prior>", text_area.yview_scroll(-1, tk.PAGES))

        box_root.bind("<Right>", text_area.xview_scroll(1, tk.PAGES))
        box_root.bind("<Left>", text_area.xview_scroll(-1, tk.PAGES))

        box_root.bind("<Down>", text_area.yview_scroll(1, tk.UNITS))
        box_root.bind("<Up>", text_area.yview_scroll(-1, tk.UNITS))

        return text_area

    def _set_msg_area(self, msg):
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, msg)
        line, char = self.message_area.index(tk.END).split('.')
        self.message_area.configure(height=int(line))
        self.message_area.update()

    def run(self):
        self.box_root.mainloop()
        self.box_root.destroy()
        return self.text

    def stop(self):
        self.box_root.quit()

    def _configure_buttons(self):
        buttons_frame = tk.Frame(self.box_root)
        buttons_frame.pack(side=tk.TOP)

        cancel_button = tk.Button(buttons_frame, takefocus=tk.YES, text="Cancel", height=1, width=6)
        cancel_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        cancel_button.bind("<Escape>", self.cancel_button_pressed)
        cancel_click_handler = MouseClickHandler(callback=self.cancel_button_pressed)
        cancel_button.bind("<Enter>", cancel_click_handler.enter)
        cancel_button.bind("<Leave>", cancel_click_handler.leave)
        cancel_button.bind("<ButtonRelease-1>", cancel_click_handler.release)

        ok_button = tk.Button(buttons_frame, takefocus=tk.YES, text="OK", height=1, width=6)
        ok_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        ok_button.bind("<Return>", self.ok_button_pressed)
        ok_click_handler = MouseClickHandler(callback=self.ok_button_pressed)
        ok_button.bind("<Enter>", ok_click_handler.enter)
        ok_button.bind("<Leave>", ok_click_handler.leave)
        ok_button.bind("<ButtonRelease-1>", ok_click_handler.release)

    @property
    def text(self):
        """ Get _text which may be None if cancel was pressed"""
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        if text is not None:  # cancel sets text=None but this is meaningless to the tk box content
            self._set_text()

    def _get_text(self):
        """ Used by the callback to get the text_area content"""
        return self.text_area.get(1.0, 'end-1c')

    def _set_text(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self._text, "normal")
        self.text_area.focus()

    # Methods executing when a key is pressed
    def x_pressed(self, _):
        self.callback(command='x')

    def cancel_button_pressed(self, _):
        self.callback(command='cancel')

    def ok_button_pressed(self, _):
        self.callback(command='update')

    def callback(self, command):
        if command == 'update':  # OK was pressed
            self.text = self._get_text()
            if self._user_specified_callback:
                # If a callback was set, call main process
                self._user_specified_callback(self)
            else:
                self.stop()
        elif command in ('x', 'cancel'):
            self.stop()
            self.text = None
