"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

DEFAULT_NUM_CHAR_WIDTH = 62
DEFAULT_NUM_CHAR_HEIGHT = 50
X_PAD_CHARS = 2

import sys

if __name__ == "__main__" and __package__ is None:
    from os import path
    sys.path.append(path.dirname(path.abspath(__file__)))

import utils as ut

from utils import tk
from utils import tk_Font

import state as st

import derived_boxes as db

finished = False


def demo_textbox():
    demo_1()
    demo_2()
    demo_3()


def demo_1():

    title = "Demo of textbox: Classic box"

    gnexp = "This is a demo of the classic textbox call, \
you can see it closes when ok is pressed.\n\n"

    msg = "INSERT A TEXT WITH MORE THAN TWO PARAGRAPHS"

    text_snippet = "Insert your text here\n"

    reply = textbox(gnexp + msg, title, text_snippet, None)

    if reply.count("\n") >= 2:
        db.msgbox(u"You did it right!")
    else:
        db.msgbox(u"You did it wrong!")


def demo_2():
    global finished
    finished = False

    title = "Demo of textbox: Classic box with callback"

    gnexp = "This is a demo of the classic textbox call, \
you can see it closes when ok is pressed.\n\n"

    msg = "INSERT A TEXT WITH FIVE OR MORE A\'s"

    text_snippet = "Insert your text here"

    def check_answer(box):
        global finished

        if finished:
            box.stop()

        if box.text.lower().count("a") >= 5:
            box.msg = u"\n\nYou did it right! Press OK button to continue."
            finished = True
        else:
            box.msg = u"\n\nMore a's are needed!"

    textbox(gnexp + msg, title, text_snippet, None,
            callback=check_answer, run=True)


def demo_3():
    global finished
    finished = False

    def check_answer(box):
        global finished

        if finished:
            box.stop()

        if "best" in box.text:
            box.msg = u"\n\nYou did right! Press OK button to continue."
            finished = True
        else:
            box.msg = u"\n\nLook to the west!"

    title = "Demo of textbox: Object with callback"

    msg = "This is a demo of the textbox set as an object with a callback, \
you can see you can configure it and when you are finished, you run it.\
\n\nThere is a typo in it. Find and correct it."

    text_snippet = "Hello"  # This text wont show

    box = textbox(
        msg, title, text_snippet, None, callback=check_answer, run=False)

    box.text = ((
        "It was the west of times, and it was the worst of times.  The rich "
        "ate cake, and the poor had cake recommended to them, but wished "
        "only for enough cash to buy bread.  The time was ripe for "
        "revolution! "))

    box.run()


def textbox(msg="", title=" ", text="",
            codebox=False, callback=None, run=True):
    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    :param str self.codebox: if 1, act as a codebox
    :param callback: if set, this function will be called when OK is pressed
    :param run: if True, a box object will be created and returned, but not run
    :str self.codebox: if 1, act as a codebox
    """

    if run:
        tb = TextBox(msg=msg, title=title, text=text,
                     codebox=codebox, callback=callback)
        reply = tb.run()
        return reply
    else:
        tb = TextBox(msg=msg, title=title, text=text,
                     codebox=codebox, callback=callback)
        return tb


class TextBox(object):

    """
    This object separates user from ui, defines which methods can
    the user invoke and which properties can he change.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without braking anithing to the user
    """

    def __init__(self, msg, title, text, codebox, callback):
        self.callback = callback
        self.ui = uiControl(msg, title, text, codebox, self.cb_ui2box)
        self.text = text

    def run(self):
        self.ui.run()
        self.ui = None
        return self._text

    def stop(self):
        self.ui.stop()

    def cb_ui2box(self, ui, event, text):
        # This method is executed when ok, cancel, or x is pressed in the ui.
        self._text = text
        if event == 'update':  # OK was pressed
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif event == 'x':
            self.stop()
        elif event == 'cancel':
            self.stop()

    @property
    def text(self):
        """Text in text Area"""
        return self._text

    @text.setter
    def text(self, text):
        self._text = to_string(text)
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
        self._msg = to_string(msg)
        self.ui.set_msg(self._msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg(self._msg)


class uiControl(object):

    def __init__(self, msg, title, text, codebox, callback):

        self.callback = callback

        self.boxRoot = tk.Tk()
        # self.boxFont = tk_Font.Font(
        #     family=st.PROPORTIONAL_FONT_FAMILY,
        #     size=st.PROPORTIONAL_FONT_SIZE)

        self.wrap = not codebox
        if self.wrap:
            self.boxFont = tk_Font.nametofont("TkTextFont")
        else:
            self.boxFont = tk_Font.nametofont("TkFixedFont")

        if self.wrap:
            self.width_in_chars = st.WIDTH_TEXT_PROP
        else:
            self.width_in_chars = st.WIDTH_TEXT_FIXED

        # default_font.configure(size=st.PROPORTIONAL_FONT_SIZE)

        self.configure_root(title)

        self.create_msg_widget(msg)

        self.create_text_area()

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
        st.rootWindowPosition = '+' + geom.split('+', 1)[1]

    # Methods executing when a key is pressed -------------------------------
    # These are 'special' methods.
    # Its return value is a function, which will be binded to the events

    def x_pressed(self):
        def call_stop():
            command = 'x'
            areaText = self.textArea.get(0.0, 'end-1c')
            self.callback(self, command, areaText)
        return call_stop

    def cancel_pressed(self):
        def call_stop(event):
            command = 'cancel'
            areaText = self.textArea.get(0.0, 'end-1c')
            self.callback(self, command, areaText)
        return call_stop

    def ok_button_pressed(self):
        def call_update(event):
            command = 'update'
            areaText = self.textArea.get(0.0, 'end-1c')
            self.callback(self, command, areaText)
            # self.textArea.focus_set()
        return call_update

    # Auxiliary methods -----------------------------------------------

    def calc_character_width(self):
        char_width = self.boxFont.measure('W')
        return char_width

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title):

        self.boxRoot.title(title)

        self.set_pos(st.rootWindowPosition)

        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed())

        self.boxRoot.iconname('Dialog')

    def create_msg_widget(self, msg):

        if msg is None:
            msg = ""

        # width = self.width_in_chars * self.calc_character_width()
        # print width
        self.messageArea = tk.Text(
            self.boxRoot,
            width=self.width_in_chars,
            state=tk.DISABLED,
            # aspect=3000,  # Use full width
            padx=(X_PAD_CHARS + 2) * self.calc_character_width(),
            pady=X_PAD_CHARS * self.calc_character_width(),
            wrap=tk.WORD,
        )
        self.set_msg(msg)

        self.messageArea.pack(side=tk.TOP, expand=1, fill='both')
        # self.messageArea.grid(row=0, column=0, sticky=tk.W)
        # self.messageArea.expand = (tk.YES)

    def create_text_area(self):
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
            padx=X_PAD_CHARS * self.calc_character_width(),
            pady=X_PAD_CHARS * self.calc_character_width(),
            height=25,  # lines
            width=self.width_in_chars,   # chars of the current font
        )

        if self.wrap:
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
        if not self.wrap:
            bottomScrollbar.grid(row=1, column=0)
        rightScrollbar.grid(row=0, column=1)

        self.textArea.grid(row=0, column=0, sticky=tk.EW)

    def create_buttons_frame(self):

        self.buttonsFrame = tk.Frame(self.boxRoot,
                                     # background="green",
                                     )
        self.buttonsFrame.pack(side=tk.TOP)
        # self.buttonsFrame.grid(row=2, column=0, sticky=tk.N)

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
        self.cancelButton.bind("<Return>", self.cancel_pressed())
        self.cancelButton.bind("<Button-1>", self.cancel_pressed())
        self.cancelButton.bind("<Escape>", self.cancel_pressed())

    def create_ok_button(self):
        # put the buttons in the buttonsFrame
        self.okButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
        self.okButton.pack(
            expand=tk.NO, side=tk.LEFT, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        self.okButton.bind("<Return>", self.ok_button_pressed())
        self.okButton.bind("<Button-1>", self.ok_button_pressed())


def to_string(something):
    if isinstance(something, ut.basestring):
        return something
    try:
        text = "".join(something)  # convert a list or a tuple to a string
    except:
        db.msgbox(
            "Exception when trying to convert {} to text in self.textArea"
            .format(type(something)))
        sys.exit(16)
    return text


if __name__ == '__main__':
    demo_textbox()
