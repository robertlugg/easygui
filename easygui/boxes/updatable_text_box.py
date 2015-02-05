"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|
"""

import sys

if sys.hexversion >= 0x020600F0:
    runningPython26 = True
else:
    runningPython26 = False

if sys.hexversion >= 0x030000F0:
    runningPython3 = True
else:
    runningPython3 = False

# Try to import the Python Image Library.  If it doesn't exist, only .gif
# images are supported.
try:
    from PIL import Image as PILImage
    from PIL import ImageTk as PILImageTk
except:
    pass

if runningPython3:
    from tkinter import *
    import tkinter.filedialog as tk_FileDialog
    from io import StringIO
else:
    from Tkinter import *
    import tkFileDialog as tk_FileDialog
    from StringIO import StringIO

# Set up basestring appropriately
if runningPython3:
    basestring = str


if TkVersion < 8.0:
    stars = "*" * 75
    print("""\n\n\n""" + stars + """
You are running Tk version: """ + str(TkVersion) + """
You must be using Tk version 8.0 or greater to use EasyGui.
Terminating.
""" + stars + """\n\n\n""")
    sys.exit(0)

rootWindowPosition = "+300+200"

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = ("Courier")

PROPORTIONAL_FONT_SIZE = 10
# a little smaller, because it it more legible at a smaller size
MONOSPACE_FONT_SIZE = 9
TEXT_ENTRY_FONT_SIZE = 12  # a little larger makes it easier to see


STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]

# Initialize some global variables that will be reset later
__choiceboxMultipleSelect = None
__replyButtonText = None
__choiceboxResults = None
__firstWidget = None
__enterboxText = None
__enterboxDefaultText = ""
__multenterboxText = ""
choiceboxChoices = None
choiceboxWidget = None
entryWidget = None
boxRoot = None


#-------------------------------------------------------------------
# textbox
#-------------------------------------------------------------------
def textbox(msg="", title=" ", text="", codebox=0, get_updated_text=None):
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

    global boxRoot, __replyButtonText, __widgetTexts, buttonsFrame
    global rootWindowPosition
    choices = ["OK"]
    __replyButtonText = choices[0]

    boxRoot = Tk()

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
    rootWindowPosition = "+0+0"
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand = NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
    boxRoot.geometry(rootWindowPosition)

    mainframe = Frame(master=boxRoot)
    mainframe.pack(side=TOP, fill=BOTH, expand=YES)

    # ----  put frames in the window -----------------------------------
    # we pack the textboxFrame first, so it will expand first
    textboxFrame = Frame(mainframe, borderwidth=3)
    textboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    message_and_buttonsFrame = Frame(mainframe)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO)

    # -------------------- put widgets in the frames --------------------

    # put a textArea in the top frame
    if codebox:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(
            textboxFrame, height=25, width=character_width, padx="2m", pady="1m")
        textArea.configure(wrap=NONE)
        textArea.configure(font=(MONOSPACE_FONT_FAMILY, MONOSPACE_FONT_SIZE))

    else:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(
            textboxFrame, height=25, width=character_width, padx="2m", pady="1m"
        )
        textArea.configure(wrap=WORD)
        textArea.configure(
            font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))

    # some simple keybindings for scrolling
    mainframe.bind("<Next>", textArea.yview_scroll(1, PAGES))
    mainframe.bind("<Prior>", textArea.yview_scroll(-1, PAGES))

    mainframe.bind("<Right>", textArea.xview_scroll(1, PAGES))
    mainframe.bind("<Left>", textArea.xview_scroll(-1, PAGES))

    mainframe.bind("<Down>", textArea.yview_scroll(1, UNITS))
    mainframe.bind("<Up>", textArea.yview_scroll(-1, UNITS))

    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(
        textboxFrame, orient=VERTICAL, command=textArea.yview)
    textArea.configure(yscrollcommand=rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(
        textboxFrame, orient=HORIZONTAL, command=textArea.xview)
    textArea.configure(xscrollcommand=bottomScrollbar.set)

    # pack the textArea and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    # Note that we need a bottom scrollbar only for code.
    # Text will be displayed with wordwrap, so we don't need to have a horizontal
    # scroll for it.
    if codebox:
        bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)

    textArea.pack(side=LEFT, fill=BOTH, expand=YES)

    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(
        messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(
        font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

    # put the buttons in the buttonsFrame
    okButton = Button(
        buttonsFrame, takefocus=YES, text="Update", height=1, width=6)
    okButton.pack(
        expand=NO, side=TOP, padx='2m', pady='1m', ipady="1m", ipadx="2m")

    def __update_myself(event):
        new_text = get_updated_text()
        textArea.delete(1.0, END)
        textArea.insert('end', new_text, "normal")

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = okButton
    handler = __textboxOK
    handler = __update_myself
    for selectionEvent in ["Return", "Button-1", "Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ----------------- the action begins ------------------------------------
    try:
        # load the text into the textArea
        if isinstance(text, basestring):
            pass
        else:
            try:
                text = "".join(text)  # convert a list or a tuple to a string
            except:
                msgbox(
                    "Exception when trying to convert {} to text in textArea".format(type(text)))
                sys.exit(16)
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


def __textboxOK(event):
    global boxRoot
    boxRoot.quit()


def update(reply=None):
    return "To close, use the x button"


def _demo_textbox():
    title = "Demo of updatable textbox"
    msg = "Push update button to update. " * 16
    text_snippet = ((
        "Update button!!!. " * 5) + "\n\n") * 10
    reply = textbox(msg, title, text_snippet, get_updated_text=update)
    print("Reply was: {!s}".format(reply))