import tkinter as tk
from tkinter import font

from easygui.utilities import get_width_and_padding, AbstractBox, bind_to_mouse


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
        :param monospace: bool (if true) don't wrap, set width to 80 witdh_in_chars, use monospace font
        :param callback: optional function to be called when OK is pressed
        """
        super().__init__(msg, title, callback, monospace=monospace)
        self.text_area = self.configure_text_widget(monospace)
        self.text = text
        self.set_buttons()

    def configure_text_widget(self, monospace):
        padding, width_in_chars = get_width_and_padding(monospace=monospace)

        text_frame = tk.Frame(self.box_root, padx=padding)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        text_area = tk.Text(
            text_frame,
            padx=padding,
            pady=padding,
            height=25,
            width=width_in_chars,
            wrap=tk.NONE if monospace else tk.WORD,
        )
        vertical_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=vertical_scrollbar.set)
        horizontal_scrollbar = tk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=text_area.xview)
        text_area.configure(xscrollcommand=horizontal_scrollbar.set)

        if monospace:
            monospace_font = font.Font(family='Courier')
            text_area.configure(font=monospace_font)
            # no word-wrapping for code, so we may need a horizontal scroll bar
            horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # pack textArea last so bottom scrollbar displays properly
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.box_root.bind("<Next>", text_area.yview_scroll(1, tk.PAGES))
        self.box_root.bind("<Prior>", text_area.yview_scroll(-1, tk.PAGES))
        self.box_root.bind("<Right>", text_area.xview_scroll(1, tk.PAGES))
        self.box_root.bind("<Left>", text_area.xview_scroll(-1, tk.PAGES))
        self.box_root.bind("<Down>", text_area.yview_scroll(1, tk.UNITS))
        self.box_root.bind("<Up>", text_area.yview_scroll(-1, tk.UNITS))
        return text_area

    @property
    def text(self):
        """ Get _text which may be None if cancel was pressed"""
        return self.text_area.get(1.0, 'end-1c')

    @text.setter
    def text(self, text):
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text, "normal")
        self.text_area.focus()

    def _set_return_value(self):
        self.return_value = self.text_area.get(1.0, 'end-1c')


if __name__ == '__main__':
    result = textbox("some message text for a textbox")
    print("textbox() return value was: {}".format(result))

    code_result = codebox("some message text for a codebox")
    print("textbox() return value was: {}".format(result))
