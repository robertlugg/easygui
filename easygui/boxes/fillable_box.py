#from Tkconstants import TOP, BOTH, YES, X, RIGHT, LEFT
#from Tkinter import Toplevel, Tk, Frame, Label, Message, Entry, Button

from .utils import *  # TODO: Fix this soon
from . import state as st
from .base_boxes import bindArrows

boxRoot = None
entryWidget = None
__enterboxText = ''
__enterboxDefaultText = ''
cancelButton = None
entryWidget = None
okButton = None


def __fillablebox(msg, title="", default="", mask=None, image=None, root=None):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """

    global boxRoot, __enterboxText, __enterboxDefaultText
    global cancelButton, entryWidget, okButton

    if title is None:
        title == ""
    if default is None:
        default = ""
    __enterboxDefaultText = default
    __enterboxText = __enterboxDefaultText

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()

    boxRoot.protocol('WM_DELETE_WINDOW', __enterboxQuit)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(st.rootWindowPosition)
    boxRoot.bind("<Escape>", __enterboxCancel)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    try:
        tk_Image = ut.load_tk_image(image)
    except Exception as inst:
        print(inst)
        tk_Image = None
    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame, image=tk_Image)
        label.image = tk_Image  # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the entryFrame ---------------------------------
    entryFrame = Frame(master=boxRoot)
    entryFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    # -------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame, width="4.5i", text=msg)
    messageWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    # --------- entryWidget ----------------------------------------------
    entryWidget = Entry(entryFrame, width=40)
    bindArrows(entryWidget)
    entryWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.TEXT_ENTRY_FONT_SIZE))
    if mask:
        entryWidget.configure(show=mask)
    entryWidget.pack(side=LEFT, padx="3m")
    entryWidget.bind("<Return>", __enterboxGetText)
    entryWidget.bind("<Escape>", __enterboxCancel)
    # put text into the entryWidget
    entryWidget.insert(0, __enterboxDefaultText)

    # ------------------ ok button -------------------------------
    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(
        expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = okButton
    handler = __enterboxGetText
    for selectionEvent in st.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<{}>".format(selectionEvent), handler)

    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(
        expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = cancelButton
    handler = __enterboxCancel
    for selectionEvent in st.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<{}>".format(selectionEvent), handler)

    # ------------------- time for action! -----------------
    entryWidget.focus_force()  # put the focus on the entryWidget
    boxRoot.deiconify()
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    if root:
        root.deiconify()
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __enterboxText


def __enterboxQuit():
    return __enterboxCancel(None)


def __enterboxCancel(event):
    global __enterboxText

    __enterboxText = None
    boxRoot.quit()


def __enterboxGetText(event):
    global __enterboxText

    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    global entryWidget

    entryWidget.delete(0, len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)
