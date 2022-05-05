import tkinter as tk
from itertools import zip_longest

from easygui.global_state import PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE
from easygui.utilities import AbstractBox


def multpasswordbox(msg="Fill in values for the fields.", title=" ", fields=None, values=None, callback=None, run=True):
    """
    Show dialog box with multiple data entry fields.
    The last of the fields is assumed to be a password, and is masked with asterisks.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :param callback: user specified callback to use when 'ok' is pressed
    :param run: whether to run or not when called
    :return: String
    """
    mb = MultiBox(msg, title, fields, values, mask_last=True, callback=callback)
    return mb.run() if run else mb


def multenterbox(msg="Fill in values for the fields.", title=" ", fields=None, values=None, callback=None, run=True):
    """
    Show dialog box with multiple data entry fields.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :param callback: user specified callback to use when 'ok' is pressed
    :param run: whether to run or not when called
    :return: String
    """
    mb = MultiBox(msg, title, fields, values, mask_last=False, callback=callback)
    return mb.run() if run else mb


class MultiBox(AbstractBox):
    def __init__(self, msg, title, fields=None, values=None, mask_last=False, callback=None):
        super().__init__(title, callback)
        self.msg_widget = self.configure_message_widget(monospace=False)
        self.msg = msg
        self.entry_widgets = []
        self.configure_entry_widgets(fields, values, mask_last)
        self.set_buttons()
        self.entry_widgets[0].focus_force()  # put the focus on the first entry widget

    def configure_entry_widgets(self, fields, values, mask_last):
        assert len(fields) <= len(values), "There are fewer fields than values! Values can be blank but fields cannot."
        for field, value in zip_longest(fields, values, fillvalue=""):

            frame = tk.Frame(master=self.box_root)
            frame.pack(side=tk.TOP, fill=tk.BOTH)

            label_widget = tk.Label(frame, text=field)
            label_widget.pack(side=tk.LEFT)

            entry_widget = tk.Entry(frame, width=40, highlightthickness=2)
            entry_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
            entry_widget.pack(side=tk.RIGHT, padx="3m")
            entry_widget.insert(0, '' if value is None else value)
            if mask_last:
                entry_widget.configure(show="*")
            self.entry_widgets.append(entry_widget)

    def _set_return_value(self):
        self.return_value = [widget.get() for widget in self.entry_widgets]


if __name__ == '__main__':
    result = multenterbox(msg="example message", title="example title", fields=["1", "2", "3"], values=["a", "b", "c"])
    print(f"Return value: {result}")
