import string
import sys

if sys.version_info < (3, 10):
    from collections import Sequence
else:
    from collections.abc import Sequence

try:
    from . import global_state
    from .base_boxes import bindArrows
except (SystemError, ValueError, ImportError):
    import global_state
    from base_boxes import bindArrows

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font


def choicebox(msg="Pick an item", title="", choices=None, preselect=0,
              callback=None,
              run=True):
    """
    The ``choicebox()`` provides a list of choices in a list box to choose
    from. The choices are specified in a sequence (a tuple or a list).

        import easygui
        msg ="What is your favorite flavor?"
        title = "Ice Cream Survey"
        choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
        choice = easygui.choicebox(msg, title, choices)  # choice is a string

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param preselect: Which item, if any are preselected when dialog appears
    :return: A string of the selected choice or None if cancelled
    """
    mb = ChoiceBox(msg, title, choices, preselect=preselect,
                   multiple_select=False,
                   callback=callback)
    if run:
        reply = mb.run()
        return reply
    else:
        return mb


def multchoicebox(msg="Pick an item", title="", choices=None,
                  preselect=0, callback=None,
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
    :return: A list of strings of the selected choices or None if cancelled.
    """
    mb = ChoiceBox(msg, title, choices, preselect=preselect,
                   multiple_select=True,
                   callback=callback)
    if run:
        reply = mb.run()
        return reply
    else:
        return mb


# Utility function.  But, is it generic enough to be moved out of here?
def make_list_or_none(obj, cast_type=None):
    # -------------------------------------------------------------------
    # for an object passed in, put it in standardized form.
    # It may be None.  Just return None
    # If it is a scalar, attempt to cast it into cast_type.  Raise error
    # if not possible.  Convert scalar to a single-element list.
    # If it is a collections.Sequence (including a scalar converted to let),
    # then cast each element to cast_type.  Raise error if any cannot be converted.
    # -------------------------------------------------------------------
    ret_val = obj
    if ret_val is None:
        return None
    # Convert any non-sequence to single-element list
    if not isinstance(obj, Sequence):
        if cast_type is not None:
            try:
                ret_val = cast_type(obj)
            except Exception as e:
                raise Exception("Value {} cannot be converted to type: {}".format(obj, cast_type))
        ret_val = [ret_val,]
    # Convert all elements to cast_type
    if cast_type is not None:
        try:
            ret_val = [cast_type(elem) for elem in ret_val]
        except:
            raise Exception("Not all values in {}\n can be converted to type: {}".format(ret_val, cast_type))
    return ret_val


class ChoiceBox(object):

    def __init__(self, msg, title, choices, preselect, multiple_select, callback):

        self.callback = callback

        if choices is None:
            # Use default choice selections if none were specified:
            choices = ('Choice 1', 'Choice 2')
        self.choices = self.to_list_of_str(choices)

        # Convert preselect to always be a list or None.
        preselect_list = make_list_or_none(preselect, cast_type=int)
        if not multiple_select and len(preselect_list)>1:
            raise ValueError("Multiple selections not allowed, yet preselect has multiple values:{}".format(preselect_list))

        self.ui = GUItk(msg, title, self.choices, preselect_list, multiple_select,
                        self.callback_ui)

    def run(self):
        """ Start the ui """
        self.ui.run()
        self.ui = None
        return self.choices

    def stop(self):
        """ Stop the ui """
        self.ui.stop()

    def callback_ui(self, ui, command, choices):
        """ This method is executed when ok, cancel, or x is pressed in the ui.
        """
        if command == 'update':  # OK was pressed
            self.choices = choices
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command == 'x':
            self.stop()
            self.choices = None
        elif command == 'cancel':
            self.stop()
            self.choices = None

    # methods to change properties --------------

    @property
    def msg(self):
        """Text in msg Area"""
        return self._msg

    @msg.setter
    def msg(self, msg):
        self.ui.set_msg(msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg(self._msg)

    # Methods to validate what will be sent to ui ---------

    def to_list_of_str(self, choices):
        choices = [str(c) for c in choices]

        while len(choices) < 2:
            raise ValueError('at least two choices need to be specified')

        return choices



class GUItk(object):

    """ This object contains the tk root object.
        It draws the window, waits for events and communicates them
        to MultiBox, together with the entered values.

        The position in wich it is drawn comes from a global variable.

        It also accepts commands from Multibox to change its message.
    """

    def __init__(self, msg, title, choices, preselect, multiple_select, callback):

        self.callback = callback

        self.choices = choices

        self.width_in_chars = global_state.prop_font_line_length
        # Initialize self.selected_choices
        # This is the value that will be returned if the user clicks the close
        # icon
        # self.selected_choices = None

        self.multiple_select = multiple_select

        self.boxRoot = tk.Tk()

        self.boxFont = tk_Font.nametofont("TkTextFont")

        self.config_root(title)

        self.set_pos(global_state.window_position)  # GLOBAL POSITION

        self.create_msg_widget(msg)

        self.create_choicearea()

        self.create_ok_button()

        self.create_cancel_button()

        self.create_special_buttons()
        
        self.preselect_choice(preselect)

        self.choiceboxWidget.focus_force()

    # Run and stop methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()  # run it!
        self.boxRoot.destroy()   # Close the window

    def stop(self):
        # Get the current position before quitting
        self.get_pos()

        self.boxRoot.quit()

    def x_pressed(self):
        self.callback(self, command='x', choices=self.get_choices())

    def cancel_pressed(self, event):
        self.callback(self, command='cancel', choices=self.get_choices())

    def ok_pressed(self, event):
        self.callback(self, command='update', choices=self.get_choices())

    # Methods to change content ---------------------------------------

    # Methods to change content ---------------------------------------

    def set_msg(self, msg):
        self.messageArea.config(state=tk.NORMAL)
        self.messageArea.delete(1.0, tk.END)
        self.messageArea.insert(tk.END, msg)
        self.messageArea.config(state=tk.DISABLED)
        # Adjust msg height
        self.messageArea.update()
        numlines = self.get_num_lines(self.messageArea)
        self.set_msg_height(numlines)
        self.messageArea.update()
        # put the focus on the entryWidget

    def set_msg_height(self, numlines):
        self.messageArea.configure(height=numlines)

    def get_num_lines(self, widget):
        end_position = widget.index(tk.END)  # '4.0'
        end_line = end_position.split('.')[0]  # 4
        return int(end_line) + 1  # 5

    def set_pos(self, pos=None):
        if not pos:
            pos = global_state.window_position
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        global_state.window_position = '+' + geom.split('+', 1)[1]

    def preselect_choice(self, preselect):
        if preselect != None:
            for v in preselect:
                self.choiceboxWidget.select_set(v)
                self.choiceboxWidget.activate(v)

    def get_choices(self):
        choices_index = self.choiceboxWidget.curselection()
        if not choices_index:
            return None
        if self.multiple_select:
            selected_choices = [self.choiceboxWidget.get(index)
                                for index in choices_index]
        else:
            selected_choices = self.choiceboxWidget.get(choices_index)

        return selected_choices

    # Auxiliary methods -----------------------------------------------
    def calc_character_width(self):
        char_width = self.boxFont.measure('W')
        return char_width

    def config_root(self, title):

        screen_width = self.boxRoot.winfo_screenwidth()
        screen_height = self.boxRoot.winfo_screenheight()
        self.root_width = int((screen_width * 0.8))
        root_height = int((screen_height * 0.5))

        self.boxRoot.title(title)
        self.boxRoot.iconname('Dialog')
        self.boxRoot.expand = tk.NO
        # self.boxRoot.minsize(width=62 * self.calc_character_width())

        self.set_pos()

        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.bind('<Any-Key>', self.KeyboardListener)
        self.boxRoot.bind("<Escape>", self.cancel_pressed)

        self.boxRoot.attributes("-topmost", True)  # Put the dialog box in focus.

    def create_msg_widget(self, msg):

        if msg is None:
            msg = ""

        self.msgFrame = tk.Frame(
            self.boxRoot,
            padx=2 * self.calc_character_width(),

        )
        self.messageArea = tk.Text(
            self.msgFrame,
            width=self.width_in_chars,
            state=tk.DISABLED,
            background=self.boxRoot.config()["background"][-1],
            relief='flat',
            padx=(global_state.default_hpad_in_chars *
                  self.calc_character_width()),
            pady=(global_state.default_hpad_in_chars *
                  self.calc_character_width()),
            wrap=tk.WORD,

        )
        self.set_msg(msg)

        self.msgFrame.pack(side=tk.TOP, expand=1, fill='both')

        self.messageArea.pack(side=tk.TOP, expand=1, fill='both')

    def create_choicearea(self):

        self.choiceboxFrame = tk.Frame(master=self.boxRoot)
        self.choiceboxFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        lines_to_show = min(len(self.choices), 20)

        # --------  put the self.choiceboxWidget in the self.choiceboxFrame ---
        self.choiceboxWidget = tk.Listbox(self.choiceboxFrame,
                                          height=lines_to_show,
                                          borderwidth="1m", relief="flat",
                                          bg="white"
                                          )

        if self.multiple_select:
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
        self.choiceboxWidget.bind("<Return>", self.ok_pressed)
        self.choiceboxWidget.bind("<Double-Button-1>",
                                  self.ok_pressed)

    def create_ok_button(self):

        self.buttonsFrame = tk.Frame(self.boxRoot)
        self.buttonsFrame.pack(side=tk.TOP, expand=tk.YES, pady=0)

        # put the buttons in the self.buttonsFrame
        okButton = tk.Button(self.buttonsFrame, takefocus=tk.YES,
                             text="OK", height=1, width=6)
        bindArrows(okButton)
        okButton.pack(expand=tk.NO, side=tk.RIGHT, padx='2m', pady='1m',
                      ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events
        okButton.bind("<Return>", self.ok_pressed)
        okButton.bind("<Button-1>", self.ok_pressed)
        okButton.bind("<space>", self.ok_pressed)

    def create_cancel_button(self):
        cancelButton = tk.Button(self.buttonsFrame, takefocus=tk.YES,
                                 text="Cancel", height=1, width=6)
        bindArrows(cancelButton)
        cancelButton.pack(expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m',
                          ipady="1m", ipadx="2m")
        cancelButton.bind("<Return>", self.cancel_pressed)
        cancelButton.bind("<Button-1>", self.cancel_pressed)
        # self.cancelButton.bind("<Escape>", self.cancel_pressed)
        # for the commandButton, bind activation events to the activation event
        # handler

    def create_special_buttons(self):
        # add special buttons for multiple select features
        if not self.multiple_select:
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
