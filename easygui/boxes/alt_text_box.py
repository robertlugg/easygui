"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|
"""

import sys

if __name__ == "__main__" and __package__ is None:
    from os import path
    sys.path.append(path.dirname(path.abspath(__file__)))
import utils as ut
from utils import tk
import state as st


def textbox(msg="", title=" ", text="", codebox=0, callback=None):
    tb = TextBox(msg=msg, title=title, text=text,
                 codebox=codebox, callback=callback)
    reply = tb.run()
    return reply


class TextBox(object):

    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    :param str self.codebox: if 1, act as a codebox
    """

    def __init__(self, msg, title, text, codebox, callback):

        self.codebox = codebox
        self.callback = callback

        self.boxRoot = tk.Tk()

        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.stop_from_x())

        self.configure_root()

        self.create_frames()

        self.create_text_area()

        self.create_msg_widget(msg)

        self.set_text_area(text)

        self.set_title(title)

        self.create_button()

    def run(self):
        self.boxRoot.mainloop()
        return self.areaText

    def set_text_area(self, text):
        text = to_string(text)
        self.textArea.insert('end', text, "normal")

    def set_title(self, title):
        if title is None:
            title = ""
        self.boxRoot.title(title)

    def set_size(self, rel_width, rel_height):
        screen_width = self.boxRoot.winfo_screenwidth()
        screen_height = self.boxRoot.winfo_screenheight()
        self.root_width = int(screen_width * rel_width)
        self.root_height = int(screen_height * rel_height)
        self.boxRoot.geometry('{}x{}'.format(
            self.root_width, self.root_height))

    def stop_from_x(self):
        def stop():
            self.areaText = self.textArea.get(0.0, 'end-1c')
            self.boxRoot.quit()
        return stop

    def stop(self):
        self.boxRoot.quit()

    def button_pressed(self):
        def send_info(event):
            self.areaText = self.textArea.get(0.0, 'end-1c')
            if self.callback:
                self.callback(self, self.areaText)
            else:
                self.boxRoot.quit()
        return send_info

    def configure_root(self):
        screen_width = self.boxRoot.winfo_screenwidth()
        eighty_chars = 80 * st.MONOSPACE_FONT_SIZE
        fraction_of_screen = int((screen_width * 0.8))
        if eighty_chars < fraction_of_screen:
            self.root_width = eighty_chars
        else:
            self.root_width = fraction_of_screen

        screen_height = self.boxRoot.winfo_screenheight()
        self.root_height = int((screen_height * 0.5))

        root_xpos = int((screen_width * 0.1))
        root_ypos = int((screen_height * 0.05))

        self.boxRoot.minsize(self.root_width, self.root_height)
        self.boxRoot.expand = tk.NO

        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")

        rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
        self.boxRoot.geometry(rootWindowPosition)

        self.boxRoot.iconname('Dialog')

    def create_frames(self):
        self.mainframe = tk.Frame(master=self.boxRoot)
        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        # ----  put frames in the window -----------------------------------
        # we pack the textFrame first, so it will expand first
        self.textFrame = tk.Frame(self.mainframe, borderwidth=3)
        self.textFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        message_and_buttonsFrame = tk.Frame(self.mainframe)
        message_and_buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)

        self.messageFrame = tk.Frame(message_and_buttonsFrame)
        self.messageFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        self.buttonsFrame = tk.Frame(message_and_buttonsFrame)
        self.buttonsFrame.pack(side=tk.RIGHT, expand=tk.NO)

    def create_text_area(self):
        """
        Put a textArea in the top frame
        Put and configure scrollbars
        """

        # character_width = 90
        self.textArea = tk.Text(
            self.textFrame, height=25, padx="2m",
            pady="1m"
        )
        self.textArea.configure(wrap=tk.WORD)
        self.textArea.configure(
            font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))

        if self.codebox:
            self.textArea.configure(wrap=tk.NONE)

        # some simple keybindings for scrolling
        self.mainframe.bind("<Next>", self.textArea.yview_scroll(1, tk.PAGES))
        self.mainframe.bind(
            "<Prior>", self.textArea.yview_scroll(-1, tk.PAGES))

        self.mainframe.bind("<Right>", self.textArea.xview_scroll(1, tk.PAGES))
        self.mainframe.bind("<Left>", self.textArea.xview_scroll(-1, tk.PAGES))

        self.mainframe.bind("<Down>", self.textArea.yview_scroll(1, tk.UNITS))
        self.mainframe.bind("<Up>", self.textArea.yview_scroll(-1, tk.UNITS))

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
        if self.codebox:
            bottomScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        rightScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    def create_msg_widget(self, msg):

        if msg is None:
            msg = ""
        # ---------- put a msg widget in the msg frame-------------------
        messageWidget = tk.Message(
            self.messageFrame, anchor=tk.NW, text=msg,
            width=int(self.root_width * 0.5))
        messageWidget.configure(
            font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
        messageWidget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH,
                           padx='1m', pady='1m')

    def create_button(self):
        # put the buttons in the buttonsFrame
        self.okButton = tk.Button(
            self.buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
        self.okButton.pack(
            expand=tk.NO, side=tk.TOP, padx='2m', pady='1m', ipady="1m",
            ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        self.okButton.bind("<Return>", self.button_pressed())
        self.okButton.bind("<Button-1>", self.button_pressed())
        self.okButton.bind("<Escape>", self.button_pressed())

        self.okButton.focus_force()


def to_string(something):
    if isinstance(something, ut.basestring):
        return something
    try:
        text = "".join(something)  # convert a list or a tuple to a string
    except:
        msgbox(
            "Exception when trying to convert {} to text in self.textArea"
            .format(type(something)))
        sys.exit(16)
    return text

import random


def update_box(box, text):

    t = random.choice(("This is the title",
                       "Another title",
                       "Yet Another",
                       "Title number 4",
                       "fifth title"))

    box.set_title(t)

    g = random.choice([(0.5, 0.5), (0.8, 0.3)])
    box.set_size(*g)


def demo_textbox():
    text_snippet = ((
        "It was the best of times, and it was the worst of times.  The rich "
        "ate cake, and the poor had cake recommended to them, but wished "
        "only for enough cash to buy bread.  The time was ripe for "
        "revolution! "
        * 5) + "\n\n") * 3
    title = "Demo of textbox"
    msg = "Press ok many times to see the window change"
    reply = textbox(msg, title, text_snippet, None, update_box)
    print(u"Reply was: {!s}".format(reply))

if __name__ == '__main__':
    demo_textbox()
