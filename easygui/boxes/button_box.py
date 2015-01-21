import re
from . import state as st
from . import utils as ut
tk = ut.tk
from .base_boxes import bindArrows

# TODO: RL: bindArrows works on the global root Tk node as defined in base_boxes.py and not this one.
#       Things appear to work fine, but they are certainly incorrect.

boxRoot = None
buttonsFrame = None
__replyButtonText = ''


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
        boxRoot = ut.tk.Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = ut.tk.Tk()
        boxRoot.withdraw()

    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(st.rootWindowPosition)
    boxRoot.minsize(400, 100)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = ut.tk.Frame(master=boxRoot)
    messageFrame.pack(side=ut.tk.TOP, fill=ut.tk.BOTH)

    # ------------- define the imageFrame ---------------------------------
    if image:
        tk_Image = None
        try:
            tk_Image = ut.load_tk_image(image)
        except Exception as inst:
            print(inst)
        if tk_Image:
            imageFrame = ut.tk.Frame(master=boxRoot)
            imageFrame.pack(side=ut.tk.TOP, fill=tk.BOTH)
            label = ut.tk.Label(imageFrame, image=tk_Image)
            label.image = tk_Image  # keep a reference!
            label.pack(side=ut.tk.TOP, expand=tk.YES, fill=tk.X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = ut.tk.Frame(master=boxRoot)
    buttonsFrame.pack(side=ut.tk.TOP, fill=tk.BOTH)

    # -------------------- place the widgets in the frames -------------------
    messageWidget = ut.tk.Message(messageFrame, text=msg, width=400)
    messageWidget.configure(
        font=(st.PROPORTIONAL_FONT_FAMILY, st.PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=ut.tk.TOP, expand=tk.YES, fill=tk.X, padx='3m', pady='3m')

    __put_buttons_in_buttonframe(choices, default_choice, cancel_choice)

    # -------------- the action begins -----------
    boxRoot.deiconify()
    boxRoot.mainloop()
    boxRoot.destroy()
    if root:
        root.deiconify()
    return __replyButtonText


def __put_buttons_in_buttonframe(choices, default_choice, cancel_choice):
    """Put the buttons in the buttons frame
    """
    global buttonsFrame

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
        this_button['widget'] = ut.tk.Button(buttonsFrame,
                                       takefocus=1,
                                       text=this_button['clean_text'],
                                       underline=hotkey_position)
        this_button['widget'].pack(
            expand=tk.YES, side=tk.LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')
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
