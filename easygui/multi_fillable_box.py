import tkinter as tk

from easygui.global_state import PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE, \
    TEXT_ENTRY_FONT_SIZE
from easygui.utilities import MouseClickHandler, AbstractBox


def multpasswordbox(msg="Fill in values for the fields.", title=" ", fields=None, values=None, callback=None, run=True):
    """
    Show dialog box with multiple data entry fields.
    The last of the fields is assumed to be a password, and is masked with asterisks.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
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
    :return: String
    """
    mb = MultiBox(msg, title, fields, values, mask_last=False, callback=callback)
    return mb.run() if run else mb


class MultiBox(AbstractBox):
    def __init__(self, msg, title, fields=None, values=None, mask_last=False, callback=None):
        super().__init__(msg, title)

        self.fields, self.values = self._process_fields_and_values(fields, values)
        self.user_defined_callback = callback

        message_widget = tk.Message(self.box_root, width="4.5i", text=msg)
        message_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        message_widget.pack(side=tk.TOP, expand=1, fill=tk.BOTH, padx='3m', pady='3m')

        self.entry_widgets = []
        for field, value in zip(self.fields, self.values):
            entry_frame = tk.Frame(master=self.box_root)
            entry_frame.pack(side=tk.TOP, fill=tk.BOTH)

            label_widget = tk.Label(entry_frame, text=field)
            label_widget.pack(side=tk.LEFT)

            entry_widget = tk.Entry(entry_frame, width=40, highlightthickness=2)
            self.entry_widgets.append(entry_widget)
            entry_widget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
            entry_widget.pack(side=tk.RIGHT, padx="3m")
            entry_widget.bind("<Return>", self._ok_pressed)
            entry_widget.bind("<Escape>", self._cancel_pressed)
            entry_widget.insert(0, '' if value is None else value)

        if mask_last:
            self.entry_widgets[-1].configure(show="*")

        buttons_frame = tk.Frame(master=self.box_root)
        buttons_frame.pack(side=tk.BOTTOM)

        cancel_button = tk.Button(buttons_frame, takefocus=1, text="Cancel")
        cancel_button.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        cancel_button.bind("<Escape>", self._cancel_pressed)
        cancel_click_handler = MouseClickHandler(callback=self._cancel_pressed)
        cancel_button.bind("<Enter>", cancel_click_handler.enter)
        cancel_button.bind("<Leave>", cancel_click_handler.leave)
        cancel_button.bind("<ButtonRelease-1>", cancel_click_handler.release)

        ok_button = tk.Button(buttons_frame, takefocus=1, text="OK")
        ok_button.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        ok_button.bind("<Return>", self._ok_pressed)
        ok_click_handler = MouseClickHandler(callback=self._ok_pressed)
        ok_button.bind("<Enter>", ok_click_handler.enter)
        ok_button.bind("<Leave>", ok_click_handler.leave)
        ok_button.bind("<ButtonRelease-1>", ok_click_handler.release)

        self.entry_widgets[0].focus_force()  # put the focus on the entry_widget

    def run(self):
        self.box_root.mainloop()  # run it!
        self.box_root.destroy()   # Close the window
        return self.values

    def _cancel_pressed(self, *args):
        self.values = None
        self.box_root.quit()

    def _ok_pressed(self, _):
        self.values = self._get_values()
        if self.user_defined_callback:
            self.user_defined_callback(self)
        self.box_root.quit()

    def _get_values(self):
        return [widget.get() for widget in self.entry_widgets]

    @staticmethod
    def _process_fields_and_values(fields, values):
        fields = [] if fields is None else list(fields)
        values = [] if values is None else list(values)
        padding_required = len(fields) - len(values)
        if padding_required > 0:
            values.extend([""] * padding_required)
        return fields, values
