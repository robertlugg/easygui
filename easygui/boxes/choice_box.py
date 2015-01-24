#from Tkconstants import NO, TOP, X, LEFT, YES, RIGHT, BOTTOM, BOTH, NW, MULTIPLE, VERTICAL, HORIZONTAL, Y, END
#from Tkinter import Tk, Frame, Message, Listbox, Scrollbar, Button

import string

from . import state as st
from . import utils as ut
from .utils import *  # TODO: Fix up soon!
from .base_boxes import bindArrows

__choiceboxMultipleSelect = None


def __choicebox(msg, title, choices):
    """
    internal routine to support choicebox() and multchoicebox()
    """
    global boxRoot, __choiceboxResults, choiceboxWidget, defaultText
    global choiceboxWidget, choiceboxChoices
    # -------------------------------------------------------------------
    # If choices is a tuple, we make it a list so we can sort it.
    # If choices is already a list, we make a new list, so that when
    # we sort the choices, we don't affect the list object that we
    # were given.
    # -------------------------------------------------------------------
    choices = list(choices[:])

    if len(choices) == 0:
        choices = ["Program logic error - no choices were specified."]
    defaultButtons = ["OK", "Cancel"]

    choices = [str(c) for c in choices]

    # TODO RL: lines_to_show is set to a min and then set to 20 right after
    # that.  Figure out why.
    lines_to_show = min(len(choices), 20)
    lines_to_show = 20

    if title is None:
        title = ""

    # Initialize __choiceboxResults
    # This is the value that will be returned if the user clicks the close icon
    __choiceboxResults = None

    boxRoot = ut.tk.Tk()
    # RL: Removed so top-level program can be closed with an 'x'
    boxRoot.protocol('WM_DELETE_WINDOW', __choiceboxQuit)
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
    boxRoot.expand = NO
    boxRoot.minsize(root_width, root_height)
    st.rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
    boxRoot.geometry(st.rootWindowPosition)

    # ---------------- put the frames in the window --------------------------
    message_and_buttonsFrame = Frame(master=boxRoot)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO, pady=0)

    choiceboxFrame = Frame(master=boxRoot)
    choiceboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    # -------------------------- put the widgets in the frames ---------------

    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(
        messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

    # --------  put the choiceboxWidget in the choiceboxFrame ----------------
    choiceboxWidget = Listbox(choiceboxFrame, height=lines_to_show, borderwidth="1m", relief="flat", bg="white"
                              )

    if __choiceboxMultipleSelect:
        choiceboxWidget.configure(selectmode=MULTIPLE)

    choiceboxWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))

    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(
        choiceboxFrame, orient=VERTICAL, command=choiceboxWidget.yview)
    choiceboxWidget.configure(yscrollcommand=rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(
        choiceboxFrame, orient=HORIZONTAL, command=choiceboxWidget.xview)
    choiceboxWidget.configure(xscrollcommand=bottomScrollbar.set)

    # pack the Listbox and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)

    choiceboxWidget.pack(
        side=LEFT, padx="1m", pady="1m", expand=YES, fill=BOTH)

    # ---------------------------------------------------
    # sort the choices
    # eliminate duplicates
    # put the choices into the choicebox Widget
    # ---------------------------------------------------

    choices = ut.lower_case_sort(choices)

    lastInserted = None
    choiceboxChoices = list()
    for choice in choices:
        if choice == lastInserted:
            continue
        else:
            choiceboxWidget.insert(END, choice)
            choiceboxChoices.append(choice)
            lastInserted = choice

    boxRoot.bind('<Any-Key>', KeyboardListener)

    # put the buttons in the buttonsFrame
    if len(choices):
        okButton = Button(
            buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
        bindArrows(okButton)
        okButton.pack(
            expand=NO, side=TOP, padx='2m', pady='1m', ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events to the activation event
        # handler
        commandButton = okButton
        handler = __choiceboxGetChoice
        for selectionEvent in st.STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

        # now bind the keyboard events
        choiceboxWidget.bind("<Return>", __choiceboxGetChoice)
        choiceboxWidget.bind("<Double-Button-1>", __choiceboxGetChoice)
    else:
        # now bind the keyboard events
        choiceboxWidget.bind("<Return>", __choiceboxCancel)
        choiceboxWidget.bind("<Double-Button-1>", __choiceboxCancel)

    cancelButton = Button(
        buttonsFrame, takefocus=YES, text="Cancel", height=1, width=6)
    bindArrows(cancelButton)
    cancelButton.pack(
        expand=NO, side=BOTTOM, padx='2m', pady='1m', ipady="1m", ipadx="2m")

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = cancelButton
    handler = __choiceboxCancel
    for selectionEvent in st.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # add special buttons for multiple select features
    if len(choices) and __choiceboxMultipleSelect:
        selectionButtonsFrame = Frame(messageFrame)
        selectionButtonsFrame.pack(side=RIGHT, fill=Y, expand=NO)

        selectAllButton = Button(
            selectionButtonsFrame, text="Select All", height=1, width=6)
        bindArrows(selectAllButton)

        selectAllButton.bind("<Button-1>", __choiceboxSelectAll)
        selectAllButton.pack(
            expand=NO, side=TOP, padx='2m', pady='1m', ipady="1m", ipadx="2m")

        clearAllButton = Button(
            selectionButtonsFrame, text="Clear All", height=1, width=6)
        bindArrows(clearAllButton)
        clearAllButton.bind("<Button-1>", __choiceboxClearAll)
        clearAllButton.pack(
            expand=NO, side=TOP, padx='2m', pady='1m', ipady="1m", ipadx="2m")

    # -------------------- bind some keyboard events -------------------------
    boxRoot.bind("<Escape>", __choiceboxCancel)

    # --------------------- the action begins --------------------------------
    # put the focus on the choiceboxWidget, and the select highlight on the
    # first item
    choiceboxWidget.select_set(0)
    choiceboxWidget.focus_force()

    # --- run it! -----
    boxRoot.mainloop()
    try:
        boxRoot.destroy()
    except:
        pass
    return __choiceboxResults


def __choiceboxGetChoice(event):
    global boxRoot, __choiceboxResults, choiceboxWidget

    if __choiceboxMultipleSelect:
        __choiceboxResults = [
            choiceboxWidget.get(index) for index in choiceboxWidget.curselection()]
    else:
        choice_index = choiceboxWidget.curselection()
        __choiceboxResults = choiceboxWidget.get(choice_index)

    boxRoot.quit()


def KeyboardListener(event):
    global choiceboxChoices, choiceboxWidget
    key = event.keysym
    if len(key) <= 1:
        if key in string.printable:
            # Find the key in the list.
            # before we clear the list, remember the selected member
            try:
                start_n = int(choiceboxWidget.curselection()[0])
            except IndexError:
                start_n = -1

            # clear the selection.
            choiceboxWidget.selection_clear(0, 'end')

            # start from previous selection +1
            for n in range(start_n + 1, len(choiceboxChoices)):
                item = choiceboxChoices[n]
                if item[0].lower() == key.lower():
                    choiceboxWidget.selection_set(first=n)
                    choiceboxWidget.see(n)
                    return
            else:
                # has not found it so loop from top
                for n, item in enumerate(choiceboxChoices):
                    if item[0].lower() == key.lower():
                        choiceboxWidget.selection_set(first=n)
                        choiceboxWidget.see(n)
                        return

                # nothing matched -- we'll look for the next logical choice
                for n, item in enumerate(choiceboxChoices):
                    if item[0].lower() > key.lower():
                        if n > 0:
                            choiceboxWidget.selection_set(first=(n - 1))
                        else:
                            choiceboxWidget.selection_set(first=0)
                        choiceboxWidget.see(n)
                        return

                # still no match (nothing was greater than the key)
                # we set the selection to the first item in the list
                lastIndex = len(choiceboxChoices) - 1
                choiceboxWidget.selection_set(first=lastIndex)
                choiceboxWidget.see(lastIndex)
                return


def __choiceboxQuit():
    __choiceboxCancel(None)


def __choiceboxCancel(event):
    global boxRoot, __choiceboxResults

    __choiceboxResults = None
    boxRoot.quit()


def __choiceboxClearAll(event):
    global choiceboxWidget, choiceboxChoices

    choiceboxWidget.selection_clear(0, len(choiceboxChoices) - 1)


def __choiceboxSelectAll(event):
    global choiceboxWidget, choiceboxChoices

    choiceboxWidget.selection_set(0, len(choiceboxChoices) - 1)
