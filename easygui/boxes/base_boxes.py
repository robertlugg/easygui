"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import os
import sys
import string

# Refs:
#   https://www.python.org/dev/peps/pep-0366
#   http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py
if __name__ == "__main__" and __package__ is None:
    from os import path
    sys.path.append(path.dirname(path.abspath(__file__)))
import utils as ut
from utils import *
import state as st

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

# -------------------------------------------------------------------
# buttonbox
# -------------------------------------------------------------------


def buttonbox(msg="", title=" ", choices=("Button[1]", "Button[2]", "Button[3]"), image=None, root=None, default_choice=None, cancel_choice=None):
    """
    Display a msg, a title, an image, and a set of buttons.
    The buttons are defined by the members of the choices list.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: the text of the button that the user selected
    """
    global boxRoot, __replyButtonText, buttonsFrame

    # If default is not specified, select the first button.  This matches old
    # behavior.
    if default_choice is None:
        default_choice = choices[0]

    # Initialize __replyButtonText to the first choice.
    # This is what will be used if the window is closed by the close button.
    __replyButtonText = choices[0]

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()

    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(st.rootWindowPosition)
    boxRoot.minsize(400, 100)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    if image:
        tk_Image = None
        try:
            tk_Image = ut.load_tk_image(image)
        except Exception as inst:
            print(inst)
        if tk_Image:
            imageFrame = Frame(master=boxRoot)
            imageFrame.pack(side=TOP, fill=BOTH)
            label = Label(imageFrame, image=tk_Image)
            label.image = tk_Image  # keep a reference!
            label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    # -------------------- place the widgets in the frames -------------------
    messageWidget = Message(messageFrame, text=msg, width=400)
    messageWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=TOP, expand=YES, fill=X, padx='3m', pady='3m')

    __put_buttons_in_buttonframe(choices, default_choice, cancel_choice)

    # -------------- the action begins -----------
    boxRoot.deiconify()
    boxRoot.mainloop()
    boxRoot.quit()
    if root:
        root.deiconify()
    return __replyButtonText


def bindArrows(widget):

    widget.bind("<Down>", tabRight)
    widget.bind("<Up>", tabLeft)

    widget.bind("<Right>", tabRight)
    widget.bind("<Left>", tabLeft)


def tabRight(event):
    boxRoot.event_generate("<Tab>")


def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")


# -----------------------------------------------------------------------
# __multfillablebox
# -----------------------------------------------------------------------
def __multfillablebox(msg="Fill in values for the fields.", title=" ", fields=(), values=(), mask=None):
    global boxRoot, __multenterboxText, __multenterboxDefaultText, cancelButton, entryWidget, okButton

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


# -----------------------------------------------------------------------
# __multenterboxGetText
# -----------------------------------------------------------------------
def __multenterboxGetText(event):
    global __multenterboxText

    __multenterboxText = list()
    for entryWidget in entryWidgets:
        __multenterboxText.append(entryWidget.get())
    boxRoot.quit()


def __multenterboxCancel(event):
    global __multenterboxText
    __multenterboxText = None
    boxRoot.quit()


def __multenterboxQuit():
    __multenterboxCancel(None)


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
    boxRoot.quit()  # button_click didn't destroy boxRoot, so we do it now
    return __enterboxText


def __enterboxGetText(event):
    global __enterboxText

    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    global entryWidget

    entryWidget.delete(0, len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)


def __enterboxCancel(event):
    global __enterboxText

    __enterboxText = None
    boxRoot.quit()


def __enterboxQuit():
    return __enterboxCancel(None)


# -----------------------------------------------------------------------
# __choicebox
# -----------------------------------------------------------------------
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

    boxRoot = Tk()
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
        boxRoot.quit()
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


def __choiceboxSelectAll(event):
    global choiceboxWidget, choiceboxChoices

    choiceboxWidget.selection_set(0, len(choiceboxChoices) - 1)


def __choiceboxClearAll(event):
    global choiceboxWidget, choiceboxChoices

    choiceboxWidget.selection_clear(0, len(choiceboxChoices) - 1)


def __choiceboxCancel(event):
    global boxRoot, __choiceboxResults

    __choiceboxResults = None
    boxRoot.quit()


def __choiceboxQuit():
    __choiceboxCancel(None)


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


def __buttonEvent(event=None, buttons=None, virtual_event=None):
    """
    Handle an event that is generated by a person interacting with a button.  It may be a button press
    or a key press.
    """
    # TODO: Replace globals with tkinter variables
    global boxRoot, __replyButtonText

    # Determine window location and save to global
    m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", boxRoot.geometry())
    if not m:
        raise ValueError(
            "failed to parse geometry string: {}".format(boxRoot.geometry()))
    width, height, xoffset, yoffset = [int(s) for s in m.groups()]
    st.rootWindowPosition = '{0:+g}{1:+g}'.format(xoffset, yoffset)

    # print('{0}:{1}:{2}'.format(event, buttons, virtual_event))
    if virtual_event == 'cancel':
        for button_name, button in buttons.items():
            if 'cancel_choice' in button:
                __replyButtonText = button['original_text']
        __replyButtonText = None
        boxRoot.quit()
        return

    if virtual_event == 'select':
        text = event.widget.config('text')[-1]
        if not isinstance(text, ut.basestring):
            text = ' '.join(text)
        for button_name, button in buttons.items():
            if button['clean_text'] == text:
                __replyButtonText = button['original_text']
                boxRoot.quit()
                return

    # Hotkeys
    if buttons:
        for button_name, button in buttons.items():
            hotkey_pressed = event.keysym
            if event.keysym != event.char:  # A special character
                hotkey_pressed = '<{}>'.format(event.keysym)
            if button['hotkey'] == hotkey_pressed:
                __replyButtonText = button_name
                boxRoot.quit()
                return

    print("Event not understood")


def __put_buttons_in_buttonframe(choices, default_choice, cancel_choice):
    """Put the buttons in the buttons frame
    """
    global buttonsFrame, cancel_invoke

    # TODO: I'm using a dict to hold buttons, but this could all be cleaned up if I subclass Button to hold
    #      all the event bindings, etc
    # TODO: Break __buttonEvent out into three: regular keyboard, default
    # select, and cancel select.
    unique_choices = ut.uniquify_list_of_strings(choices)
    # Create buttons dictionary and Tkinter widgets
    buttons = dict()
    for button_text, unique_button_text in zip(choices, unique_choices):
        this_button = dict()
        this_button['original_text'] = button_text
        this_button['clean_text'], this_button[
            'hotkey'], hotkey_position = ut.parse_hotkey(button_text)
        this_button['widget'] = Button(buttonsFrame,
                                       takefocus=1,
                                       text=this_button['clean_text'],
                                       underline=hotkey_position)
        this_button['widget'].pack(
            expand=YES, side=LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')
        buttons[unique_button_text] = this_button
    # Bind arrows, Enter, Escape
    for this_button in buttons.values():
        bindArrows(this_button['widget'])
        for selectionEvent in st.STANDARD_SELECTION_EVENTS:
            this_button['widget'].bind("<{}>".format(selectionEvent),
                                       lambda e: __buttonEvent(
                                           e, buttons, virtual_event='select'),
                                       add=True)

    # Assign default and cancel buttons
    if cancel_choice in buttons:
        buttons[cancel_choice]['cancel_choice'] = True
    boxRoot.bind_all('<Escape>', lambda e: __buttonEvent(
        e, buttons, virtual_event='cancel'), add=True)
    boxRoot.protocol('WM_DELETE_WINDOW', lambda: __buttonEvent(
        None, buttons, virtual_event='cancel'))
    if default_choice in buttons:
        buttons[default_choice]['default_choice'] = True
        buttons[default_choice]['widget'].focus_force()
    # Bind hotkeys
    for hk in [button['hotkey'] for button in buttons.values() if button['hotkey']]:
        boxRoot.bind_all(hk, lambda e: __buttonEvent(e, buttons), add=True)

    return


if __name__ == '__main__':
    print("Hello from base_boxes")
