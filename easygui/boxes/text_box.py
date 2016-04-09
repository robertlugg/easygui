"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import sys

try:
    from . import global_state
except (SystemError, ValueError, ImportError):
    import global_state

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font


def demo_textbox():
    demo_1()
    Demo2()
    Demo3()


def demo_1():

    title = "Demo of textbox: Classic box"

    gnexp = ("This is a demo of the classic textbox call, "
             "you can see it closes when ok is pressed.\n\n")

    challenge = "INSERT A TEXT WITH MORE THAN TWO PARAGRAPHS"

    text = "Insert your text here\n"

    msg = gnexp + challenge

    finished = False
    while True:

        text = textbox(msg, title, text)
        escaped = not text
        if escaped or finished:
            break

        if text.count("\n") >= 2:
            msg = (u"You did it right! Press OK")
            finished = True
        else:
            msg = u"You did it wrong! Try again!\n" + challenge


class Demo2(object):

    """ Program that challenges the user to write 5 a's """

    def __init__(self):
        """ Set and run the program """

        title = "Demo of textbox: Classic box with callback"

        gnexp = ("This is a demo of the textbox with a callback, "
                 "it doesn't flicker!.\n\n")

        msg = "INSERT A TEXT WITH FIVE OR MORE A\'s"

        text_snippet = "Insert your text here"

        self.finished = False

        textbox(gnexp + msg, title, text_snippet, False,
                callback=self.check_answer, run=True)

    def check_answer(self, box):
        """ Callback from TextBox

        Parameters
        -----------
        box: object
            object containing parameters and methods to communicate with the ui

        Returns
        -------
        nothing:
            its return is through the box object
        """

        if self.finished:
            box.stop()

        if box.text.lower().count("a") >= 5:
            box.msg = u"\n\nYou did it right! Press OK button to continue."
            box.stop()
            self.finished
        else:
            box.msg = u"\n\nMore a's are needed!"


class Demo3(object):

    """ Program that challenges the user to find a typo """

    def __init__(self):
        """ Set and run the program """

        self.finished = False

        title = "Demo of textbox: Object with callback"

        msg = ("This is a demo of the textbox set as "
               "an object with a callback, "
               "you can configure it and when you are finished, "
               "you run it.\n\nThere is a typo in it. Find and correct it.")

        text_snippet = "Hello"  # This text wont show

        box = textbox(
            msg, title, text_snippet, False, callback=self.check_answer, run=False)

        box.text = (
            "It was the west of times, and it was the worst of times. "
            "The  rich ate cake, and the poor had cake recommended to them, "
            "but wished only for enough cash to buy bread."
            "The time was ripe for revolution! ")

        box.run()

    def check_answer(self, box):
        """ Callback from TextBox

        Parameters
        ----------
        box: object
            object containing parameters and methods to communicate with the ui

        Returns
        -------
        nothing:
            its return is through the box object
        """
        if self.finished:
            box.stop()

        if "best" in box.text:
            box.msg = u"\n\nYou did right! Press OK button to continue."
            self.finished = True
        else:
            box.msg = u"\n\nLook to the west!"


def textbox(msg="", title=" ", text="",
            codebox=False, callback=None, run=True):
    """ Display a message and a text to edit

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
        If OK is pressed returns the contents of textArea

    """

    tb = TextBox(msg=msg, title=title, text=text,
                 codebox=codebox, callback=callback)
    if not run:
        return tb
    else:
        reply = tb.run()
        return reply


class TextBox(object):

    """ Display a message and a text to edit

    This object separates user from ui, defines which methods can
    the user invoke and which properties can he change.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.
    """

    def __init__(self, msg, title, text, codebox, callback=lambda *args, **kwargs: True):
        """ Create box object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        text: str, list or tuple
            text displayed in textAres (editable)
        codebox: bool
            if True, don't wrap and width is set to 80 chars
        callback: function
            if set, this function will be called when OK is pressed

        Returns
        -------
        object
            The box object
        """

        self.callback = callback
        self.ui = GUItk(msg, title, text, codebox, self.callback_ui)
        self.text = text

    def run(self):
        """ Start the ui """
        self.ui.run()
        self.ui = None
        return self._text

    def stop(self):
        """ Stop the ui """
        self.ui.stop()

    def callback_ui(self, ui, command, text):
        """ This method is executed when ok, cancel, or x is pressed in the ui.
        """
        if command == 'update':  # OK was pressed
            self._text = text
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command == 'x':
            self.stop()
            self._text = None
        elif command == 'cancel':
            self.stop()
            self._text = None

    # methods to change properties --------------
    @property
    def text(self):
        """Text in text Area"""
        return self._text

    @text.setter
    def text(self, text):
        self._text = self.to_string(text)
        self.ui.set_text(self._text)

    @text.deleter
    def text(self):
        self._text = ""
        self.ui.set_text(self._text)

    @property
    def msg(self):
        """Text in msg Area"""
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = self.to_string(msg)
        self.ui.set_msg(self._msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg(self._msg)

    # Methods to validate what will be sent to ui ---------

    def to_string(self, something):
        try:
            basestring  # python 2
        except NameError:
            basestring = str  # Python 3

        if isinstance(something, basestring):
            return something
        try:
            text = "".join(something)  # convert a list or a tuple to a string
        except:
            textbox(
                "Exception when trying to convert {} to text in self.textArea"
                .format(type(something)))
            sys.exit(16)
        return text


class GUItk(object):

    """ This is the object that contains the tk root object"""

    def __init__(self, msg, title, text, codebox, callback):
        """ Create ui object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        text: str, list or tuple
            text displayed in textAres (editable)
        codebox: bool
            if True, don't wrap, and width is set to 80 chars
        callback: function
            if set, this function will be called when OK is pressed

        Returns
        -------
        object
            The ui object
        """

        self.callback = callback

        self.boxRoot = tk.Tk()
        # self.boxFont = tk_Font.Font(
        #     family=global_state.PROPORTIONAL_FONT_FAMILY,
        #     size=global_state.PROPORTIONAL_FONT_SIZE)

        wrap_text = not codebox
        if wrap_text:
            self.boxFont = tk_Font.nametofont("TkTextFont")
            self.width_in_chars = global_state.prop_font_line_length
        else:
            self.boxFont = tk_Font.nametofont("TkFixedFont")
            self.width_in_chars = global_state.fixw_font_line_length

        # default_font.configure(size=global_state.PROPORTIONAL_FONT_SIZE)

        self.configure_root(title)

        self.create_msg_widget(msg)

        self.create_text_area(wrap_text)

        self.create_buttons_frame()

        self.create_cancel_button()

        self.create_ok_button()

    # Run and stop methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def stop(self):
        # Get the current position before quitting
        self.get_pos()
        self.boxRoot.quit()

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

    def set_msg_height(self, numlines):
        self.messageArea.configure(height=numlines)

    def get_num_lines(self, widget):
        end_position = widget.index(tk.END)  # '4.0'
        end_line = end_position.split('.')[0]  # 4
        return int(end_line) + 1  # 5

    def set_text(self, text):
        self.textArea.delete(1.0, tk.END)
        self.textArea.insert(tk.END, text, "normal")
        self.textArea.focus()

    def set_pos(self, pos):
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        global_state.window_position = '+' + geom.split('+', 1)[1]

    def get_text(self):
        return self.textArea.get(0.0, 'end-1c')

    # Methods executing when a key is pressed -------------------------------
    def x_pressed(self):
        self.callback(self, command='x', text=self.get_text())

    def cancel_pressed(self, event):
        self.callback(self, command='cancel', text=self.get_text())

    def ok_button_pressed(self, event):
        self.callback(self, command='update', text=self.get_text())

    # Auxiliary methods -----------------------------------------------
    def calc_character_width(self):
        char_width = self.boxFont.measure('W')
        return char_width

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title):

        self.boxRoot.title(title)

        self.set_pos(global_state.window_position)

        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.bind("<Escape>", self.cancel_pressed)

        self.boxRoot.iconname('Dialog')

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
            padx=(global_state.default_hpad_in_chars) *
            self.calc_character_width(),
            pady=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            wrap=tk.WORD,

        )
        self.set_msg(msg)

        self.msgFrame.pack(side=tk.TOP, expand=1, fill='both')

        self.messageArea.pack(side=tk.TOP, expand=1, fill='both')

    def create_text_area(self, wrap_text):
        """
        Put a textArea in the top frame
        Put and configure scrollbars
        """

        self.textFrame = tk.Frame(
            self.boxRoot,
            padx=2 * self.calc_character_width(),
        )

        self.textFrame.pack(side=tk.TOP)
        # self.textFrame.grid(row=1, column=0, sticky=tk.EW)

        self.textArea = tk.Text(
            self.textFrame,
            padx=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            pady=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            height=25,  # lines
            width=self.width_in_chars,   # chars of the current font
        )

        if wrap_text:
            self.textArea.configure(wrap=tk.WORD)
        else:
            self.textArea.configure(wrap=tk.NONE)

        # some simple keybindings for scrolling
        self.boxRoot.bind("<Next>", self.textArea.yview_scroll(1, tk.PAGES))
        self.boxRoot.bind(
            "<Prior>", self.textArea.yview_scroll(-1, tk.PAGES))

        self.boxRoot.bind("<Right>", self.textArea.xview_scroll(1, tk.PAGES))
        self.boxRoot.bind("<Left>", self.textArea.xview_scroll(-1, tk.PAGES))

        self.boxRoot.bind("<Down>", self.textArea.yview_scroll(1, tk.UNITS))
        self.boxRoot.bind("<Up>", self.textArea.yview_scroll(-1, tk.UNITS))

        # add a vertical scrollbar to the frame
        rightScrollbar = tk.Scrollbar(
            self.textFrame, orient=tk.VERTICAL, command=self.textArea.yview)
        self.textArea.configure(yscrollcommand=rightScrollbar.set)

        # add a horizontal scrollbar to the frame
        bottomScrollbar = tk.Scrollbar(
            self.textFrame, orient=tk.HORIZONTAL, command=self.textArea.xview)
        self.textArea.configure(xscrollcommand=bottomScrollbar.set)

        # pack the textArea and the scrollbars.  Note that although
        # we must define the textArea first, we must pack it last,
        # so that the bottomScrollbar will be located properly.

        # Note that we need a bottom scrollbar only for code.
        # Text will be displayed with wordwrap, so we don't need to have
        # a horizontal scroll for it.

        if not wrap_text:
            bottomScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        rightScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    def create_buttons_frame(self):

        self.buttonsFrame = tk.Frame(self.boxRoot,
                                     # background="green",

                                     )
        self.buttonsFrame.pack(side=tk.TOP)

    def create_cancel_button(self):
        # put the buttons in the buttonsFrame
        self.cancelButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="Cancel",
            height=1, width=6)
        self.cancelButton.pack(
            expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        self.cancelButton.bind("<Return>", self.cancel_pressed)
        self.cancelButton.bind("<Button-1>", self.cancel_pressed)
        self.cancelButton.bind("<Escape>", self.cancel_pressed)

    def create_ok_button(self):
        # put the buttons in the buttonsFrame
        self.okButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
        self.okButton.pack(
            expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        self.okButton.bind("<Return>", self.ok_button_pressed)
        self.okButton.bind("<Button-1>", self.ok_button_pressed)


if __name__ == '__main__':
    demo_textbox()
