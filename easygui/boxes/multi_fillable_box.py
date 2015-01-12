from Tkconstants import TOP, BOTH, RIGHT, LEFT, BOTTOM
from Tkinter import Tk, Frame, Message, Label, Entry, Button


if __name__ == "__main__" and __package__ is None:
    from os import path, sys
    sys.path.append(path.dirname(path.abspath(__file__)))
import state as st
from base_boxes import bindArrows, boxRoot

__multenterboxText = ""
cancelButton = None
entryWidget = None
okButton = None


def __multfillablebox(msg="Fill in values for the fields.", title=" ", fields=(), values=(), mask=None):
    global boxRoot, __multenterboxText, cancelButton, entryWidget, okButton

    choices = ["OK", "Cancel"]
    if len(fields) == 0:
        return None

    fields = list(fields[:])  # convert possible tuples to a list
    values = list(values[:])  # convert possible tuples to a list

    # TODO RL: The following seems incorrect when values>fields.  Replace
    # below with zip?
    if len(values) == len(fields):
        pass
    elif len(values) > len(fields):
        fields = fields[0:len(values)]
    else:
        while len(values) < len(fields):
            values.append("")

    boxRoot = Tk()

    boxRoot.protocol('WM_DELETE_WINDOW', __multenterboxQuit)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(st.rootWindowPosition)
    boxRoot.bind("<Escape>", __multenterboxCancel)

    # -------------------- put subframes in the boxRoot --------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # -------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame, width="4.5i", text=msg)
    messageWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    global entryWidgets
    entryWidgets = list()

    lastWidgetIndex = len(fields) - 1

    for widgetIndex in range(len(fields)):
        argFieldName = fields[widgetIndex]
        argFieldValue = values[widgetIndex]
        entryFrame = Frame(master=boxRoot)
        entryFrame.pack(side=TOP, fill=BOTH)

        # --------- entryWidget ----------------------------------------------
        labelWidget = Label(entryFrame, text=argFieldName)
        labelWidget.pack(side=LEFT)

        entryWidget = Entry(entryFrame, width=40, highlightthickness=2)
        entryWidgets.append(entryWidget)
        entryWidget.configure(
            font=(st.PROPORTIONAL_FONT_FAMILY, st.TEXT_ENTRY_FONT_SIZE))
        entryWidget.pack(side=RIGHT, padx="3m")

        bindArrows(entryWidget)

        entryWidget.bind("<Return>", __multenterboxGetText)
        entryWidget.bind("<Escape>", __multenterboxCancel)

        # for the last entryWidget, if this is a multpasswordbox,
        # show the contents as just asterisks
        if widgetIndex == lastWidgetIndex:
            if mask:
                entryWidgets[widgetIndex].configure(show=mask)

        # put text into the entryWidget
        if argFieldValue is None:
            argFieldValue = ''
        entryWidgets[widgetIndex].insert(0, '{}'.format(argFieldValue))
        widgetIndex += 1

    # ------------------ ok button -------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=BOTTOM, fill=BOTH)

    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(
        expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = okButton
    handler = __multenterboxGetText
    for selectionEvent in st.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(
        expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event
    # handler
    commandButton = cancelButton
    handler = __multenterboxCancel
    for selectionEvent in st.STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------- time for action! -----------------
    entryWidgets[0].focus_force()  # put the focus on the entryWidget
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    boxRoot.quit()  # button_click didn't destroy boxRoot, so we do it now
    return __multenterboxText


def __multenterboxQuit():
    __multenterboxCancel(None)


def __multenterboxCancel(event):
    global __multenterboxText
    __multenterboxText = None
    boxRoot.quit()


def __multenterboxGetText(event):
    global __multenterboxText

    __multenterboxText = list()
    for entryWidget in entryWidgets:
        __multenterboxText.append(entryWidget.get())
    boxRoot.quit()