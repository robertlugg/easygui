import tkinter as tk

from easygui.utilities import AbstractBox, bind_to_mouse


def choicebox(msg="Pick an item", title="", choices=('Choice 1', 'Choice 2'), preselect=(), callback=None, run=True):
    """
    Present the user with a list of choices.
    return the choice that he selects.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param preselect: optional list of pre-selected choices, a subset of the choices argument
    :param callback: user defined callback to be performed when selection is complete
    :param run: whether to call .run() on the box immediately or return an instance
    :return: List containing choice selected or None if cancelled
    """
    cb = ChoiceBox(msg, title, choices, preselect=preselect, multiple_select=False, callback=callback)
    return cb.run() if run else cb


def multchoicebox(msg="Pick an item", title="", choices=('Choice 1', 'Choice 2'), preselect=(), callback=None,
                  run=True):
    """
    The ``multchoicebox()`` function provides a way for a user to select
    from a list of choices. The interface looks just like the ``choicebox()``
    function's dialog box, but the user may select zero, one, or multiple choices.

    The choices are specified in a sequence (a tuple or a list).

        import easygui
        msg ="What is your favorite flavor?"
        title = "Ice Cream Survey"
        choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
        choice = easygui.multchoicebox(msg, title, choices)


    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param preselect: Which item, if any are preselected when dialog appears
    :param callback: user defined callback to be performed when selection is complete
    :param run: whether to call .run() on the box immediately or return an instance
    :return: A list of strings of the selected choices or None if cancelled.
    """
    mcb = ChoiceBox(msg, title, choices, preselect=preselect, multiple_select=True, callback=callback)
    if run:
        reply = mcb.run()
        return reply
    else:
        return mcb


class ChoiceBox(AbstractBox):

    def __init__(self, msg, title, choices, preselect, multiple_select, callback):
        super().__init__(title, callback)
        assert multiple_select or len(preselect) <= 1, "multiple_select needs to be True for multiple preselect use "

        self.msg_widget = self.configure_message_widget(monospace=False)
        self.msg = msg

        self._multiple_select = multiple_select
        self.choices = [str(c) for c in choices]

        self.choicebox_widget = self.create_choice_area()

        self.buttonsFrame = tk.Frame(self.box_root)
        self.buttonsFrame.pack(side=tk.TOP, expand=tk.YES, pady=0)
        self.create_ok_button()
        self.create_cancel_button()
        if self._multiple_select:
            self.create_special_buttons()

        self.preselect_choice(preselect)
        self.choicebox_widget.focus_force()

    def preselect_choice(self, preselect):
        for v in preselect:
            self.choicebox_widget.select_set(v)
            self.choicebox_widget.activate(v)

    def _set_return_value(self):
        choices_index = self.choicebox_widget.curselection()
        if self._multiple_select:
            self.return_value = [self.choicebox_widget.get(index) for index in choices_index]
        else:
            self.return_value = self.choicebox_widget.get(choices_index)

    def create_choice_area(self):
        choicebox_frame = tk.Frame(master=self.box_root)
        choicebox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        choicebox_widget = tk.Listbox(
            master=choicebox_frame,
            height=(min(len(self.choices), 20)),
            borderwidth="1m", relief="flat",
            bg="white",
            selectmode=tk.MULTIPLE if self._multiple_select else tk.SINGLE,
        )

        # add a vertical scrollbar to the frame
        vertical_scrollbar = tk.Scrollbar(choicebox_frame, orient=tk.VERTICAL, command=choicebox_widget.yview)
        choicebox_widget.configure(yscrollcommand=vertical_scrollbar.set)

        # add a horizontal scrollbar to the frame
        horizontal_scrollbar = tk.Scrollbar(choicebox_frame, orient=tk.HORIZONTAL, command=choicebox_widget.xview)
        choicebox_widget.configure(xscrollcommand=horizontal_scrollbar.set)

        # pack everything - order is important so that horizontal scrollbar displays correctly
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        choicebox_widget.pack(side=tk.LEFT, padx="1m", pady="1m", expand=tk.YES, fill=tk.BOTH)

        # Insert choices widgets
        for choice in self.choices:
            choicebox_widget.insert(tk.END, choice)

        # Bind the keyboard events
        choicebox_widget.bind("<Double-Button-1>", self.ok_button_pressed)
        return choicebox_widget

    def create_ok_button(self):
        ok_button = tk.Button(self.buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
        ok_button.pack(expand=tk.NO, side=tk.RIGHT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        ok_button.bind("<Return>", self.ok_button_pressed)
        ok_button.bind("<space>", self.ok_button_pressed)
        bind_to_mouse(ok_button, self.ok_button_pressed)

    def create_cancel_button(self):
        cancel_button = tk.Button(self.buttonsFrame, takefocus=tk.YES, text="Cancel", height=1, width=6)
        cancel_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        cancel_button.bind("<Escape>", self.cancel_button_pressed)
        bind_to_mouse(cancel_button, self.cancel_button_pressed)

    def create_special_buttons(self):
        # add special buttons for multiple select features
        select_all_button = tk.Button(self.buttonsFrame, text="Select All", height=1, width=6)
        select_all_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        bind_to_mouse(select_all_button, self.select_all)

        clear_all_button = tk.Button(self.buttonsFrame, text="Clear All", height=1, width=6)
        clear_all_button.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m", ipadx="2m")
        bind_to_mouse(clear_all_button, self.clear_all)

    def clear_all(self, event):
        self.choicebox_widget.selection_clear(0, len(self.choices) - 1)

    def select_all(self, event):
        self.choicebox_widget.selection_set(0, len(self.choices) - 1)


if __name__ == '__main__':
    users_choice = multchoicebox(choices=['choice1', 'choice2'])
    print("User's choice is: {}".format(users_choice))
    users_choice = choicebox(msg="pick only one", choices=['live', 'let_die'])
    print("User's choice is: {}".format(users_choice))
