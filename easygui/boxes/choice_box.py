import string

from . import state as st
from .base_boxes import bindArrows
try:
    import tkinter as tk  # python 3
except:
    import Tkinter as tk  # python 2


def choicebox(msg="Pick an item", title="", choices=[], callback=None,
              run=True):
    """
    Present the user with a list of choices.
    return the choice that he selects.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :return: List containing choice selected or None if cancelled
    """
    if run:
        mb = ChoiceBox(msg, title, choices, multiple_select=False,
                       callback=callback)
        reply = mb.run()
        return reply
    else:
        mb = ChoiceBox(msg, title, choices, multiple_select=False,
                       callback=callback)
        return mb


def multchoicebox(msg="Pick an item", title="", choices=[], callback=None,
                  run=True):
    """ Same as choicebox, but the user can select many items.

    """
    if run:
        mb = ChoiceBox(msg, title, choices, multiple_select=True,
                       callback=callback)
        reply = mb.run()
        return reply
    else:
        mb = ChoiceBox(msg, title, choices, multiple_select=True,
                       callback=callback)
        return mb


class ChoiceBox(object):

    def __init__(self, msg, title, choices, multiple_select, callback):

        self.callback = callback

        self.choices = self.check_choices(choices)

        self.ui = GUItk(msg, title, choices, multiple_select, self.callback_ui)

    def run(self):
        """ Start the ui """
        self.ui.run()
        self.ui = None
        return self.values

    def stop(self):
        """ Stop the ui """
        self.ui.stop()

    def callback_ui(self, ui, command, values):
        """ This method is executed when ok, cancel, or x is pressed in the ui.
        """
        if command == 'update':  # OK was pressed
            self.values = values
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command == 'x':
            self.stop()
            self.values = None
        elif command == 'cancel':
            self.stop()
            self.values = None

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

    def check_choices(self, choices):
        # -------------------------------------------------------------------
        # If choices is a tuple, we make it a list so we can sort it.
        # If choices is already a list, we make a new list, so that when
        # we sort the choices, we don't affect the list object that we
        # were given.
        # -------------------------------------------------------------------
        choices = list(choices[:])

        if len(choices) == 0:
            choices = ["Program logic error - no choices were specified."]

        choices = [str(c) for c in choices]

        return choices


class GUItk(object):

    """ This object contains the tk root object.
        It draws the window, waits for events and communicates them
        to MultiBox, together with the entered values.

        The position in wich it is drawn comes from a global variable.

        It also accepts commands from Multibox to change its message.
    """

    def __init__(self, msg, title, choices, multiple_select, callback):

        self.callback = callback

        self.choices = choices

        self.multiple_select = multiple_select

        self.boxRoot = tk.Tk()

        self.config_root(title)

        self.set_pos(st.rootWindowPosition)  # GLOBAL POSITION

        self.create_frames()

        self.create_msg_widget(msg)

        self.create_choicearea()

        self.choiceboxWidget.select_set(0)

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
        self.callback(self, command='x', values=self.choiceboxResults)

    def cancel_pressed(self, event):
        self.callback(self, command='cancel', values=self.choiceboxResults)

    def ok_pressed(self, event):
        self.callback(self, command='update', values=self.choiceboxResults)

    # Methods to change content ---------------------------------------

    def set_msg(self, msg):
        self.messageWidget.configure(text=msg)
        self.entryWidgets[0].focus_force()  # put the focus on the entryWidget

    def set_pos(self, pos):
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        st.rootWindowPosition = '+' + geom.split('+', 1)[1]

    def config_root(self, title):

        # Initialize self.choiceboxResults
        # This is the value that will be returned if the user clicks the close
        # icon
        self.choiceboxResults = None

        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        screen_width = self.boxRoot.winfo_screenwidth()
        screen_height = self.boxRoot.winfo_screenheight()
        self.root_width = int((screen_width * 0.8))
        root_height = int((screen_height * 0.5))
        root_xpos = int((screen_width * 0.1))
        root_ypos = int((screen_height * 0.05))

        self.boxRoot.title(title)
        self.boxRoot.iconname('Dialog')
        st.rootWindowPosition = "+0+0"
        self.boxRoot.geometry(st.rootWindowPosition)
        self.boxRoot.expand = tk.NO
        self.boxRoot.minsize(self.root_width, root_height)
        st.rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
        self.boxRoot.geometry(st.rootWindowPosition)

    def create_frames(self):

        # ---------------- put the frames in the window -----------------------
        self.message_and_buttonsFrame = tk.Frame(master=self.boxRoot)
        self.message_and_buttonsFrame.pack(
            side=tk.TOP, fill=tk.X, expand=tk.NO)

        self.messageFrame = tk.Frame(self.message_and_buttonsFrame)
        self.messageFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.buttonsFrame = tk.Frame(self.message_and_buttonsFrame)
        self.buttonsFrame.pack(side=tk.RIGHT, expand=tk.NO, pady=0)

        self.choiceboxFrame = tk.Frame(master=self.boxRoot)
        self.choiceboxFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

    # -------------------------- put the widgets in the frames ---------------

    def create_msg_widget(self, msg):
        # ---------- put a msg widget in the msg frame-------------------
        messageWidget = tk.Message(self.messageFrame, anchor=tk.NW, text=msg,
                                   width=int(self.root_width * 0.9))
        messageWidget.configure(
            font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
        messageWidget.pack(
            side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, padx='1m', pady='1m')

    def create_choicearea(self):
        lines_to_show = min(len(self.choices), 20)

        # --------  put the self.choiceboxWidget in the self.choiceboxFrame ---
        self.choiceboxWidget = tk.Listbox(self.choiceboxFrame,
                                          height=lines_to_show,
                                          borderwidth="1m", relief="flat",
                                          bg="white"
                                          )

        if self.multiple_select:
            self.choiceboxWidget.configure(selectmode=tk.MULTIPLE)

        self.choiceboxWidget.configure(font=(st.PROPORTIONAL_FONT_FAMILY,
                                             st.PROPORTIONAL_FONT_SIZE))

        # Insert choices widgets
        for choice in self.choices:
            self.choiceboxWidget.insert(tk.END, choice)
            self.choices.append(choice)

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

        self.boxRoot.bind('<Any-Key>', self.KeyboardListener)

        # put the buttons in the self.buttonsFrame
        if len(self.choices):
            okButton = tk.Button(self.buttonsFrame, takefocus=tk.YES,
                                 text="OK", height=1, width=6)
            bindArrows(okButton)
            okButton.pack(expand=tk.NO, side=tk.TOP, padx='2m', pady='1m',
                          ipady="1m", ipadx="2m")

            # for the commandButton, bind activation events
            # to the activation event handler
            commandButton = okButton
            handler = self.choiceboxGetChoice
            for selectionEvent in st.STANDARD_SELECTION_EVENTS:
                commandButton.bind("<%s>" % selectionEvent, handler)

            # now bind the keyboard events
            self.choiceboxWidget.bind("<Return>", self.choiceboxGetChoice)
            self.choiceboxWidget.bind("<Double-Button-1>",
                                      self.choiceboxGetChoice)
        else:
            # now bind the keyboard events
            self.choiceboxWidget.bind("<Return>", self.cancel_pressed)
            self.choiceboxWidget.bind("<Double-Button-1>", self.cancel_pressed)

        cancelButton = tk.Button(self.buttonsFrame, takefocus=tk.YES,
                                 text="Cancel", height=1, width=6)
        bindArrows(cancelButton)
        cancelButton.pack(expand=tk.NO, side=tk.BOTTOM, padx='2m', pady='1m',
                          ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler

        # add special buttons for multiple select features
        if len(self.choices) and self.multiple_select:
            selectionButtonsFrame = tk.Frame(self.messageFrame)
            selectionButtonsFrame.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.NO)

            selectAllButton = tk.Button(
                selectionButtonsFrame, text="Select All", height=1, width=6)
            bindArrows(selectAllButton)

            selectAllButton.bind("<Button-1>", self.choiceboxSelectAll)
            selectAllButton.pack(expand=tk.NO, side=tk.TOP, padx='2m',
                                 pady='1m',
                                 ipady="1m", ipadx="2m")

            clearAllButton = tk.Button(selectionButtonsFrame, text="Clear All",
                                       height=1, width=6)
            bindArrows(clearAllButton)
            clearAllButton.bind("<Button-1>", self.choiceboxClearAll)
            clearAllButton.pack(expand=tk.NO, side=tk.TOP,
                                padx='2m', pady='1m',
                                ipady="1m", ipadx="2m")

    def choiceboxGetChoice(self, event):

        if self.multiple_select:
            self.choiceboxResults = [self.choiceboxWidget.get(index)
                                     for index in
                                     self.choiceboxWidget.curselection()]
        else:
            choice_index = self.choiceboxWidget.curselection()
            self.choiceboxResults = self.choiceboxWidget.get(choice_index)

        self.boxRoot.quit()

    def KeyboardListener(self, event):
        key = event.keysym
        if len(key) <= 1:
            if key in string.printable:
                # Find the key in the list.
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
