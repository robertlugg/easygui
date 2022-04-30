import tkinter as tk
from tkinter import font

from easygui.utilities import get_width_and_padding, MouseClickHandler, AbstractBox


def textbox(msg='', title='', text='', callback=None, run=True):
    """
    Displays a dialog box with a large, multi-line text box, and returns the entered text as a string.
    The message text is displayed in a proportional font and wraps.
    :param str msg: text displayed in the message area (instructions...)
    :param str title: the window title
    :param text: text displayed in textAreas (editable)
    :param function callback: if set, this function will be called when OK is pressed
    :param bool run: if True, a box object will be created and returned, but not run
    :return:
        if 'run' is True then the box is run AND Ok is pressed -> returns the content of the TextArea
        if 'run' is True then the box is run AND Cancel is pressed -> returns None
        else 'run' is False then the box is not run -> returns an instance TextBox
    """
    tb = TextBox(msg=msg, title=title, text=text, monospace=False, callback=callback)
    return tb.run() if run else tb


def codebox(msg='', title='', text='', callback=None, run=True):
    """
    Helper method similar to textbox, displays text in a monospaced font which is useful for code.
    The text parameter should be a string, or a list or tuple of lines to be displayed in the textbox.
    :param str msg: text displayed in the message area (instructions...)
    :param str title: the window title
    :param str text: text displayed in textAreas (editable)
    :param function callback: if set, this function will be called when OK is pressed
    :param bool run: if True, a box object will be created and returned, but not run
    :return:
        if 'run' is True then the box is run AND Ok is pressed -> returns the content of the TextArea
        if 'run' is True then the box is run AND Cancel is pressed -> returns None
        else 'run' is False then the box is not run -> returns an instance TextBox
    """
    cb = TextBox(msg, title, text, monospace=True, callback=callback)
    return cb.run() if run else cb


def exceptionbox(msg='An error (exception) has occurred in the program.', title='Error Report'):
    """
    Display a box that gives information about the latest exception that has been raised.
    :param str msg: [optional] msg to be displayed above exception
    :param str title: [optional] the window title
    :return: None
    """
    import sys
    import traceback
    text = "".join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
    TextBox(msg, title, text=text, monospace=True).run()


class TextBox(AbstractBox):
    """ Display a message, and an editable text field pre-populated with 'text' """

    def __init__(self, msg, title, text, monospace, callback=None):
        """
        :param msg: str displayed in the message area (instructions...)
        :param title: str used as the window title
        :param text: str displayed in textArea (editable)
        :param monospace: bool (if true) don't wrap, set width to 80 chars, use monospace font
        :param callback: optional function to be called when OK is pressed
        """
        super().__init__(msg, title, callback)
        self._text = text

        self.message_area = self._configure_message_area(box_root=self.box_root, monospace=monospace)
        self._set_msg_area("" if msg is None else msg)

        self.MONOSPACE_FONT = font.Font(family='Courier')
        self.text_area = self._configure_text_area(box_root=self.box_root, code_box=monospace)
        self._set_text()
        self._configure_buttons()

    @staticmethod
    def _configure_message_area(box_root, monospace):
        padding, width_in_chars = get_width_and_padding(monospace)

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
            # no word-wrapping for code, so we need a horizontal scroll bar
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

    @property
    def return_value(self):
        """ In order to work like all the other boxes, need to define 'return value'"""
        return self._text

    @return_value.setter
    def return_value(self, text):
        self.text = text

    def _get_text(self):
        """ Used by the callback to get the text_area content"""
        return self.text_area.get(1.0, 'end-1c')

    def _set_text(self):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self._text, "normal")
        self.text_area.focus()

    def ok_button_pressed(self, _):
        self.text = self._get_text()
        if self._user_specified_callback:
            # If a callback was set, call main process
            self._user_specified_callback(self)
        else:
            self.stop()


if __name__ == '__main__':
    result = textbox("test message here")
    print("textbox() return value was: {}".format(result))
