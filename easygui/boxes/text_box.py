"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|
"""

import sys

from . import utils as ut
from .utils import *
from . import state as st


def textbox(msg="", title=" ", text="", codebox=0):
    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    :param str codebox: if 1, act as a codebox
    """

    if msg is None:
        msg = ""
    if title is None:
        title = ""

    boxRoot = tk.Tk()

    def __textboxOK(event):
        boxRoot.quit()

    # Quit when x button pressed
    boxRoot.protocol('WM_DELETE_WINDOW', boxRoot.quit)

    screen_width = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width = int((screen_width * 0.8))
    root_height = int((screen_height * 0.5))
    root_xpos = int((screen_width * 0.1))
    root_ypos = int((screen_height * 0.05))

    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    st.rootWindowPosition = "+0+0"
    boxRoot.geometry(st.rootWindowPosition)
    boxRoot.expand = tk.NO
    boxRoot.minsize(root_width, root_height)
    st.rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
    boxRoot.geometry(st.rootWindowPosition)

    mainframe = tk.Frame(master=boxRoot)
    mainframe.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    # ----  put frames in the window -----------------------------------
    # we pack the textboxFrame first, so it will expand first
    textboxFrame = tk.Frame(mainframe, borderwidth=3)
    textboxFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

    message_and_buttonsFrame = tk.Frame(mainframe)
    message_and_buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)

    messageFrame = tk.Frame(message_and_buttonsFrame)
    messageFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

    buttonsFrame = tk.Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=tk.RIGHT, expand=tk.NO)

    # -------------------- put widgets in the frames --------------------

    # put a textArea in the top frame
    if codebox:
        character_width = int((root_width * 0.6) / st.MONOSPACE_FONT_SIZE)
        textArea = tk.Text(
            textboxFrame, height=25, width=character_width, padx="2m",
            pady="1m")
        textArea.configure(wrap=tk.NONE)
        textArea.configure(font=(st.MONOSPACE_FONT_FAMILY,
                                 st.MONOSPACE_FONT_SIZE))

    else:
        character_width = int((root_width * 0.6) / st.MONOSPACE_FONT_SIZE)
        textArea = tk.Text(
            textboxFrame, height=25, width=character_width, padx="2m",
            pady="1m"
        )
        textArea.configure(wrap=tk.WORD)
        textArea.configure(
            font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))

    # some simple keybindings for scrolling
    mainframe.bind("<Next>", textArea.yview_scroll(1, tk.PAGES))
    mainframe.bind("<Prior>", textArea.yview_scroll(-1, tk.PAGES))

    mainframe.bind("<Right>", textArea.xview_scroll(1, tk.PAGES))
    mainframe.bind("<Left>", textArea.xview_scroll(-1, tk.PAGES))

    mainframe.bind("<Down>", textArea.yview_scroll(1, tk.UNITS))
    mainframe.bind("<Up>", textArea.yview_scroll(-1, tk.UNITS))

    # add a vertical scrollbar to the frame
    rightScrollbar = tk.Scrollbar(
        textboxFrame, orient=tk.VERTICAL, command=textArea.yview)
    textArea.configure(yscrollcommand=rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = tk.Scrollbar(
        textboxFrame, orient=tk.HORIZONTAL, command=textArea.xview)
    textArea.configure(xscrollcommand=bottomScrollbar.set)

    # pack the textArea and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last,
    # so that the bottomScrollbar will be located properly.

    # Note that we need a bottom scrollbar only for code.
    # Text will be displayed with wordwrap, so we don't need to have
    # a horizontal scroll for it.
    if codebox:
        bottomScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    rightScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    textArea.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = tk.Message(
        messageFrame, anchor=tk.NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH,
                       padx='1m', pady='1m')

    # put the buttons in the buttonsFrame
    okButton = tk.Button(
        buttonsFrame, takefocus=tk.YES, text="OK", height=1, width=6)
    okButton.pack(
        expand=tk.NO, side=tk.TOP, padx='2m', pady='1m', ipady="1m",
        ipadx="2m")

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = okButton
    handler = __textboxOK
    for selectionEvent in ["Return", "Button-1", "Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ----------------- the action begins ------------------------------------
    text = to_string(text)
    try:
        textArea.insert('end', text, "normal")
    except:
        msgbox("Exception when trying to load the textArea.")
        sys.exit(16)

    try:
        okButton.focus_force()
    except:
        msgbox("Exception when trying to put focus on okButton.")
        sys.exit(16)

    boxRoot.mainloop()

    # this line MUST go before the line that destroys boxRoot
    areaText = textArea.get(0.0, 'end-1c')
    boxRoot.destroy()
    return areaText  # return __replyButtonText


def to_string(something):
    if isinstance(something, ut.basestring):
        return something
    try:
        text = "".join(something)  # convert a list or a tuple to a string
    except:
        msgbox(
            "Exception when trying to convert {} to text in textArea"
            .format(type(something)))
        sys.exit(16)
    return text


def demo_textbox():
    text_snippet = ((
        "It was the best of times, and it was the worst of times.  The rich "
        "ate cake, and the poor had cake recommended to them, but wished "
        "only for enough cash to buy bread.  The time was ripe for "
        "revolution! "
        * 5) + "\n\n") * 10
    title = "Demo of textbox"
    msg = "Here is some sample text. " * 16
    reply = textbox(msg, title, text_snippet)
    print("Reply was: {!s}".format(reply))
