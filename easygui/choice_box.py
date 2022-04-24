import string
import tkinter as tk

from easygui.utilities import get_num_lines, get_width_and_padding, bindArrows, MouseClickHandler


def choicebox(msg="Pick an item", title="", choices=None, preselect=[], callback=None, run=True):
    """
    Present the user with a list of choices.
    return the choice that he selects.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param preselect: optional list of pre-selected choices, a subset of the choices argument
    :param callback:
    :param run:
    :return: List containing choice selected or None if cancelled
    """
    cb = ChoiceBox(msg, title, choices, preselect=preselect, multiple_select=False, callback=callback)
    if run:
        reply = cb.run()
        return reply
    else:
        return cb


def multchoicebox(msg="Pick an item", title="", choices=None, preselect=[], callback=None, run=True):
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
    :return: A list of strings of the selected choices or None if cancelled.
    """
    mcb = ChoiceBox(msg, title, choices, preselect=preselect, multiple_select=True, callback=callback)
    if run:
        reply = mcb.run()
        return reply
    else:
        return mcb


class ChoiceBox(object):

    def __init__(self, msg, title, choices, preselect, multiple_select, callback):

        if not multiple_select and len(preselect)>1:
            raise ValueError("Multiple selections not allowed, yet preselect has multiple values:{}".format(preselect))

        self._multiple_select = multiple_select
        self._user_specified_callback = callback
        if choices is None:
            # Use default choice selections if none were specified:
            choices = ('Choice 1', 'Choice 2')
        self.choices = [str(c) for c in choices]

        self.box_root = self._configure_box_root(title)

        self.message_area = self._configure_message_area(self.box_root)
        self._set_msg_area("" if msg is None else msg)

        self.create_choice_area()

        self.create_ok_button()
        self.create_cancel_button()
        self.create_special_buttons()
        self.preselect_choice(preselect)
        self.choiceboxWidget.focus_force()

    def run(self):
        self.box_root.mainloop()  # run it!
        self.box_root.destroy()   # close the window
        return self.choices

    def stop(self):
        self.box_root.quit()

    def x_pressed(self):
        self.stop()
        self.choices = None

    def cancel_button_pressed(self, event):
        self.stop()
        self.choices = None

    def ok_button_pressed(self, event):
        self.choices = self.get_choices()
        if self._user_specified_callback:
            # If a _user_specified_callback was set, call main process
            self._user_specified_callback(self)
        else:
            self.stop()

    def _set_msg_area(self, msg):
        self.message_area.config(state=tk.NORMAL)  # necessary but I don't know why
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, msg)
        numlines = get_num_lines(self.message_area)
        self.message_area.configure(height=numlines)
        self.message_area.update()

    def preselect_choice(self, preselect):
        if preselect != None:
            for v in preselect:
                self.choiceboxWidget.select_set(v)
                self.choiceboxWidget.activate(v)

    def get_choices(self):
        choices_index = self.choiceboxWidget.curselection()
        if not choices_index:
            return None
        if self._multiple_select:
            selected_choices = [self.choiceboxWidget.get(index)
                                for index in choices_index]
        else:
            selected_choices = self.choiceboxWidget.get(choices_index)

        return selected_choices

    def _configure_box_root(self, title):
        box_root = tk.Tk()
        box_root.title(title)
        box_root.iconname('Dialog')
        box_root.protocol('WM_DELETE_WINDOW', self.x_pressed)
        box_root.bind('<Any-Key>', self.KeyboardListener)
        box_root.bind("<Escape>", self.cancel_button_pressed)
        return box_root

    @staticmethod
    def _configure_message_area(box_root):
        padding, width_in_chars = get_width_and_padding(monospace=False)

        message_frame = tk.Frame(box_root, padx=padding)
        message_frame.pack(side=tk.TOP, expand=1, fill='both')

        message_area = tk.Text(master=message_frame,
                               width=width_in_chars,
                               state=tk.DISABLED,
                               background=box_root.config()["background"][-1],
                               relief='flat',
                               padx=padding,
                               pady=padding,
                               wrap=tk.WORD)
        message_area.pack(side=tk.TOP, expand=1, fill='both')
        return message_area

    def create_choice_area(self):

        self.choiceboxFrame = tk.Frame(master=self.box_root)
        self.choiceboxFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        lines_to_show = min(len(self.choices), 20)

        # --------  put the self.choiceboxWidget in the self.choiceboxFrame ---
        self.choiceboxWidget = tk.Listbox(self.choiceboxFrame,
                                          height=lines_to_show,
                                          borderwidth="1m", relief="flat",
                                          bg="white"
                                          )

        if self._multiple_select:
            self.choiceboxWidget.configure(selectmode=tk.MULTIPLE)

        # self.choiceboxWidget.configure(font=(global_state.PROPORTIONAL_FONT_FAMILY,
        #                                      global_state.PROPORTIONAL_FONT_SIZE))

        # add a vertical scrollbar to the frame
        rightScrollbar = tk.Scrollbar(self.choiceboxFrame, orient=tk.VERTICAL,
                                      command=self.choiceboxWidget.yview)
        self.choiceboxWidget.configure(yscrollcommand=rightScrollbar.set)

        # add a horizontal scrollbar to the frame
        bottomScrollbar = tk.Scrollbar(self.choiceboxFrame,
                                       orient=tk.HORIZONTAL,
                                       command=self.choiceboxWidget.xview)
        self.choiceboxWidget.configure(xscrollcommand=bottomScrollbar.set)

        # pack the Listbox and the scrollbars.
        # Note that although we must define
        # the textArea first, we must pack it last,
        # so that the bottomScrollbar will
        # be located properly.

        bottomScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        rightScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.choiceboxWidget.pack(
            side=tk.LEFT, padx="1m", pady="1m", expand=tk.YES, fill=tk.BOTH)

        # Insert choices widgets
        for choice in self.choices:
            self.choiceboxWidget.insert(tk.END, choice)

        # Bind the keyboard events
        self.choiceboxWidget.bind("<Return>", self.ok_button_pressed)
        self.choiceboxWidget.bind("<Double-Button-1>",
                                  self.ok_button_pressed)

    def create_ok_button(self):

        self.buttonsFrame = tk.Frame(self.box_root)
        self.buttonsFrame.pack(side=tk.TOP, expand=tk.YES, pady=0)

        # put the buttons in the self.buttonsFrame
        okButton = tk.Button(self.buttonsFrame, takefocus=tk.YES,
                             text="OK", height=1, width=6)
        bindArrows(okButton)
        okButton.pack(expand=tk.NO, side=tk.RIGHT, padx='2m', pady='1m',
                      ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events
        okButton.bind("<Return>", self.ok_button_pressed)
        okButton.bind("<space>", self.ok_button_pressed)

        ok_click_handler = MouseClickHandler(callback=self.ok_button_pressed)
        okButton.bind("<Enter>", ok_click_handler.enter)
        okButton.bind("<Leave>", ok_click_handler.leave)
        okButton.bind("<ButtonRelease-1>", ok_click_handler.release)

    def create_cancel_button(self):
        cancelButton = tk.Button(self.buttonsFrame, takefocus=tk.YES,
                                 text="Cancel", height=1, width=6)
        bindArrows(cancelButton)
        cancelButton.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m',
                          ipady="1m", ipadx="2m")
        cancelButton.bind("<Escape>", self.cancel_button_pressed)

        cancel_click_handler = MouseClickHandler(callback=self.cancel_button_pressed)
        cancelButton.bind("<Enter>", cancel_click_handler.enter)
        cancelButton.bind("<Leave>", cancel_click_handler.leave)
        cancelButton.bind("<ButtonRelease-1>", cancel_click_handler.release)

    def create_special_buttons(self):
        # add special buttons for multiple select features
        if not self._multiple_select:
            return

        selectAllButton = tk.Button(
            self.buttonsFrame, text="Select All", height=1, width=6)
        selectAllButton.pack(expand=tk.NO, side=tk.LEFT, padx='2m',
                             pady='1m',
                             ipady="1m", ipadx="2m")

        clearAllButton = tk.Button(self.buttonsFrame, text="Clear All",
                                   height=1, width=6)
        clearAllButton.pack(expand=tk.NO, side=tk.LEFT,
                            padx='2m', pady='1m',
                            ipady="1m", ipadx="2m")

        selectAllButton.bind("<Button-1>", self.choiceboxSelectAll)
        bindArrows(selectAllButton)
        clearAllButton.bind("<Button-1>", self.choiceboxClearAll)
        bindArrows(clearAllButton)

    def KeyboardListener(self, event):
        key = event.keysym
        if len(key) <= 1:
            if key in string.printable:
                # Find the key in the liglobal_state.
                # before we clear the list, remember the selected member
                try:
                    start_n = int(self.choiceboxWidget.curselection()[0])
                except IndexError:
                    start_n = -1

                # clear the selection.
                self.choiceboxWidget.selection_clear(0, 'end')

                # start from previous selection +1
                for n in range(start_n + 1, len(self.choices)):
                    item = self.choices[n]
                    if item[0].lower() == key.lower():
                        self.choiceboxWidget.selection_set(first=n)
                        self.choiceboxWidget.see(n)
                        return
                else:
                    # has not found it so loop from top
                    for n, item in enumerate(self.choices):
                        if item[0].lower() == key.lower():
                            self.choiceboxWidget.selection_set(first=n)
                            self.choiceboxWidget.see(n)
                            return

                    # nothing matched -- we'll look for the next logical choice
                    for n, item in enumerate(self.choices):
                        if item[0].lower() > key.lower():
                            if n > 0:
                                self.choiceboxWidget.selection_set(
                                    first=(n - 1))
                            else:
                                self.choiceboxWidget.selection_set(first=0)
                            self.choiceboxWidget.see(n)
                            return

                    # still no match (nothing was greater than the key)
                    # we set the selection to the first item in the list
                    lastIndex = len(self.choices) - 1
                    self.choiceboxWidget.selection_set(first=lastIndex)
                    self.choiceboxWidget.see(lastIndex)
                    return

    def choiceboxClearAll(self, event):
        self.choiceboxWidget.selection_clear(0, len(self.choices) - 1)

    def choiceboxSelectAll(self, event):
        self.choiceboxWidget.selection_set(0, len(self.choices) - 1)

if __name__ == '__main__':
    users_choice = multchoicebox(choices=['choice1', 'choice2'])
    print("User's choice is: {}".format(users_choice))
