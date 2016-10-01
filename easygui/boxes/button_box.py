"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""

import collections
import os
import re
import sys

try:
    from . import global_state
    from . import utils as ut
    from .text_box import textbox
except (SystemError, ValueError, ImportError):
    import global_state
    import utils as ut
    from text_box import textbox

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2
    import tkFont as tk_Font


def demo_buttonbox_1():
    print("hello from the demo")
    value = buttonbox(
        title="First demo",
        msg="bonjour",
        choices=["Button[1]", "Button[2]", "Button[3]"],
        default_choice="Button[2]")
    print("Return: {}".format(value))


def demo_buttonbox_2():
    package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  ;# My parent's directory
    images = list()
    images.append(os.path.join(package_dir, "python_and_check_logo.gif"))
    images.append(os.path.join(package_dir, "zzzzz.gif"))
    images.append(os.path.join(package_dir, "python_and_check_logo.png"))
    images = [images, images, images, images, ]
    value = buttonbox(
        title="Second demo",
        msg="Now is a good time to press buttons and show images",
        choices=['ok', 'cancel'],
        images=images)
    print("Return: {}".format(value))


def demo_buttonbox_3():
    msg = "This demoes interfacing without a callback \nYou haven't pushed a button"
    while True:
        choice_selected = buttonbox(
            title="This demoes interfacing without a callback",
            msg=msg,
            choices=["Button[1]", "Button[2]", "Button[3]"],
            default_choice="Button[2]")

        msg = "You have pushed button {} \nNotice the flicking".format(choice_selected)

        if not choice_selected:
            break


def demo_buttonbox_4():

    def actualize(box):
        msg = "You have pushed button {} \nNotice the absence of flicking!!! ".format(box.choice_selected)
        box.msg = msg

    choice_selected = buttonbox(
        title="This demoes interfacing with a callback",
        msg="This demoes interfacing WITH a callback \nYou haven't pushed a button",
        choices={"Button[1]":1, "Button[2]":2, "Button[3]":3},
        default_choice="Button[2]",
        callback=actualize)


def buttonbox(msg="",
              title=" ",
              choices=("Button[1]", "Button[2]", "Button[3]"),
              image=None,
              images=None,
              default_choice=None,
              cancel_choice=None,
              callback=None,
              run=True):
    """
    Display a msg, a title, an image, and a set of buttons.
    The buttons are defined by the members of the choices global_state.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: (Only here for backward compatibility)
    :param str images: Filename of image or iterable or iterable of iterable to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :return: the text of the button that the user selected



    """
    validations = Validations()
    images = validations.validate_images(image, images)
    images = validations.images_to_matrix(images)
    bb = ButtonBox(
            msg=msg,
            title=title,
            choices=choices,
            images=images,
            default_choice=default_choice,
            cancel_choice=cancel_choice,
            callback=callback,
            validations=validations)

    reply = bb.run()

    return reply


class Validations(object):

    def validate_images(self, image, images):
        if image and images:
            raise ValueError("Specify 'images' parameter only for buttonbox.")
        if image:
            images = image
        return images

    def images_to_matrix(self, img_filenames):
        """
        Create one or more images in the dialog.
        :param img_filenames:
        May be a filename (which will generate a single image), a list of filenames (which will generate
        a row of images), or a list of list of filename (which will create a 2D array of buttons.
        :return:
        """

        if img_filenames is None:
            return
        # Convert to a list of lists of filenames regardless of input
        if self.is_string(img_filenames):
            img_filenames = [[img_filenames, ], ]
        elif self.is_sequence(img_filenames) and self.is_string(img_filenames[0]):
            img_filenames = [img_filenames, ]
        elif self.is_sequence(img_filenames) and self.is_sequence(img_filenames[0]) and self.is_string(img_filenames[0][0]):
            pass
        else:
            raise ValueError("Incorrect images argument.")

        return img_filenames

    def convert_choices_to_dict(self, choices):
        if isinstance(choices, collections.Mapping): # If it is dictionary-like
            choices_dict = choices
            choices_list = choices_dict.keys()
        else:
            # Convert into a dictionary of equal key and values
            choices_list = list(choices)
            choices_dict = {i: i for i in choices_list}
        return choices_dict, choices_list


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

    # REF: http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string
    def is_sequence(self, arg):
        return hasattr(arg, "__getitem__") or hasattr(arg, "__iter__")


    def is_string(self, arg):
        ret_val = None
        try:
            ret_val = isinstance(arg, basestring) #Python 2
        except:
            ret_val = isinstance(arg, str) #Python 3
        return ret_val



class ButtonBox(object):
    """ Display various types of button boxes

    This object separates user from ui, defines which methods can
    the user invoke and which properties can he change.

    It also calls the ui in defined ways, so if other gui
    library can be used (wx, qt) without breaking anything for the user.
    """

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback, validations):
        """ Create box object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        choices : iterable of strings
            build a button for each string in choices
        images : iterable of filenames, or an iterable of iterables of filenames
            displays each image
        default_choice : string
            one of the strings in choices to be the default selection
        cancel_choice : string
            if X or <esc> is pressed, it appears as if this button was pressed.
        callback: function
            if set, this function will be called when any button is pressed.

        Returns
        -------
        object
            The box object
        """

        self.callback = callback
        self.cancel_choice = cancel_choice
        self.choices_dict, choices_list = validations.convert_choices_to_dict(choices)
        self.choice_selected = None

        # Set the window, don't show it
        self.cb_interface = CallBackInterface()
        self.ui = GUItk(msg, title, choices_list, images, default_choice, cancel_choice, self.update)

    def run(self):
        """ Show the window and wait """
        self.ui.run()
        # The window is closed
        self.ui = None
        return self.choice_selected


    def update(self, command, choice_selected, row_column_selected):
        """ This method is executed when any buttons or x are pressed in the ui.
        """
        self.select_choice(choice_selected)

        self.row_column_selected = row_column_selected

        self.cb_interface.row_column_selected = self.row_column_selected
        self.cb_interface.choice_selected = self.choice_selected
        self.cb_interface.msg = None

        if command == 'update':  # Any button was pressed
            if self.callback:
                # If a callback was set, call main process
                self.callback(self.cb_interface)
            else:
                self.cb_interface.stop = True
        elif command == 'x':
            self.choice_selected = None
            self.cb_interface.stop = True
        elif command == 'cancel':
            self.choice_selected = None
            self.cb_interface.stop = True

        return self.cb_interface.stop, self.cb_interface.msg

    def select_choice(self, choice_selected):
        try:
            self.choice_selected = self.choices_dict[choice_selected]
        except:
            self.choice_selected = None


class CallBackInterface(object):
    choice_selected = None
    row_column_selected = None
    stop = False
    msg = None


class GUItk(object):
    """ This is the object that contains the tk root object"""

    def __init__(self, msg, title, choices, images, default_choice, cancel_choice, update):
        """ Create ui object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        choices : iterable of strings
            build a button for each string in choices
        images : iterable of filenames, or an iterable of iterables of filenames
            displays each image
        default_choice : string
            one of the strings in choices to be the default selection
        cancel_choice : string
            if X or <esc> is pressed, it appears as if this button was pressed.
        update: function
            if set, this function will be called when any button is pressed.


        Returns
        -------
        object
            The ui object
        """
        self._title = title
        self._msg = msg
        self._choices = choices
        self._default_choice = default_choice
        self._cancel_choice = cancel_choice
        self.update = update
        self._choice_text = None
        self._choice_row_column = None
        self._images = list()

        self.boxRoot = tk.Tk()
        # self.boxFont = tk_Font.Font(
        #     family=global_state.PROPORTIONAL_FONT_FAMILY,
        #     size=global_state.PROPORTIONAL_FONT_SIZE)

        self.boxFont = tk_Font.nametofont("TkFixedFont")
        self.width_in_chars = global_state.fixw_font_line_length

        # default_font.configure(size=global_state.PROPORTIONAL_FONT_SIZE)

        self.configure_root(title)

        self.create_msg_widget(msg)

        self.create_images_frame()

        self.create_images(images)

        self.create_buttons_frame()

        self.create_buttons(choices, default_choice)


    # Run and stop methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def stop(self):
        # Get the current position before quitting
        #self.get_pos()
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

    def set_pos(self, pos):
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        global_state.window_position = '+' + geom.split('+', 1)[1]

    # Methods executing when a key is pressed -------------------------------
    def x_pressed(self):
        self._choice_text = self._cancel_choice
        self.update_box(command='x')

    def cancel_pressed(self, event):
        self._choice_text = self._cancel_choice
        self.update_box(command='cancel')

    def button_pressed(self, button_text, button_row_column):
        self._choice_text = button_text
        self._choice_row_column = button_row_column
        self.update_box(command='update')

    def update_box(self, command):
        stop, msg = self.update(command, self._choice_text, self._choice_row_column)
        if stop:
            self.stop()
        if msg:
            self.set_msg(msg)


    def hotkey_pressed(self, event=None):
        """
        Handle an event that is generated by a person interacting with a button.  It may be a button press
        or a key press.

        TODO: Enhancement: Allow hotkey to be specified in filename of image as a shortcut too!!!
        """

        # Determine window location and save to global
        # TODO: Not sure where this goes, but move it out of here!
        m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", self.boxRoot.geometry())
        if not m:
            raise ValueError(
                "failed to parse geometry string: {}".format(self.boxRoot.geometry()))
        width, height, xoffset, yoffset = [int(s) for s in m.groups()]
        global_state.window_position = '{0:+g}{1:+g}'.format(xoffset, yoffset)

        # Hotkeys
        if self._buttons:
            for button_name, button in self._buttons.items():
                hotkey_pressed = event.keysym
                if event.keysym != event.char:  # A special character
                    hotkey_pressed = '<{}>'.format(event.keysym)
                if button['hotkey'] == hotkey_pressed:
                    self._choice_text = button_name
                    self.update(self, command='update')
                    return
        print("Event not understood")

    # Auxiliary methods -----------------------------------------------
    def calc_character_width(self):
        char_width = self.boxFont.measure('W')
        return char_width

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title):
        self.boxRoot.title(title)

        self.set_pos(global_state.window_position)

        # Resize setup
        self.boxRoot.columnconfigure(0, weight=10)
        self.boxRoot.minsize(100, 200)
        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.bind("<Escape>", self.cancel_pressed)
        self.boxRoot.iconname('Dialog')

    def create_msg_widget(self, msg):

        if msg is None:
            msg = ""

        self.messageArea = tk.Text(
            self.boxRoot,
            width=self.width_in_chars,
            state=tk.DISABLED,
            padx=(global_state.default_hpad_in_chars) *
            self.calc_character_width(),
            relief="flat",
            background=self.boxRoot.config()["background"][-1],
            pady=global_state.default_hpad_in_chars *
            self.calc_character_width(),
            wrap=tk.WORD,
        )
        self.set_msg(msg)
        self.messageArea.grid(row=0)
        self.boxRoot.rowconfigure(0, weight=10, minsize='10m')

    def create_images_frame(self):
        self.imagesFrame = tk.Frame(self.boxRoot)
        row = 1
        self.imagesFrame.grid(row=row)
        self.boxRoot.rowconfigure(row, weight=10, minsize='10m')

    def create_images(self, img_filenames):
        """
        Create one or more images in the dialog.
        :param img_filenames:
         a list of list of filenames
        :return:
        """

        if img_filenames is None:
            return


        images = list()
        for _r, images_row in enumerate(img_filenames):
            row_number = len(img_filenames) - _r
            for column_number, filename in enumerate(images_row):
                this_image = dict()
                try:
                    this_image['tk_image'] = ut.load_tk_image(filename)
                except Exception as e:
                    print(e)
                    this_image['tk_image'] = None
                this_image['widget'] = tk.Button(
                    self.imagesFrame,
                    takefocus=1,
                    compound=tk.TOP)
                if this_image['widget'] is not None:
                    this_image['widget'].configure(image=this_image['tk_image'])
                fn = lambda text=filename, row=_r, column=column_number: self.button_pressed(text, (row, column))
                this_image['widget'].configure(command=fn)
                sticky_dir = tk.N+tk.S+tk.E+tk.W
                this_image['widget'].grid(row=row_number, column=column_number, sticky=sticky_dir, padx='1m', pady='1m', ipadx='2m', ipady='1m')
                self.imagesFrame.rowconfigure(row_number, weight=10, minsize='10m')
                self.imagesFrame.columnconfigure(column_number, weight=10)
                images.append(this_image)
        self._images = images  # Image objects must live, so place them in self.  Otherwise, they will be deleted.

    def create_buttons_frame(self):
        self.buttonsFrame = tk.Frame(self.boxRoot)
        self.buttonsFrame.grid(row=2, column=0)

    def create_buttons(self, choices, default_choice):

        unique_choices = ut.uniquify_list_of_strings(choices)
        # Create buttons dictionary and Tkinter widgets
        buttons = dict()
        i_hack = 0
        for row, (button_text, unique_button_text) in enumerate(zip(choices, unique_choices)):
            this_button = dict()
            this_button['original_text'] = button_text
            this_button['clean_text'], this_button['hotkey'], hotkey_position = ut.parse_hotkey(button_text)
            this_button['widget'] = tk.Button(
                    self.buttonsFrame,
                    takefocus=1,
                    text=this_button['clean_text'],
                    underline=hotkey_position)
            fn = lambda text=button_text, row=row, column=0: self.button_pressed(text, (row, column))
            this_button['widget'].configure(command=fn)
            this_button['widget'].grid(row=0, column=i_hack, padx='1m', pady='1m', ipadx='2m', ipady='1m')
            self.buttonsFrame.columnconfigure(i_hack, weight=10)
            i_hack += 1
            buttons[unique_button_text] = this_button
        self._buttons = buttons
        if default_choice in buttons:
            buttons[default_choice]['widget'].focus_force()
        # Bind hotkeys
        for hk in [button['hotkey'] for button in buttons.values() if button['hotkey']]:
            self.boxRoot.bind_all(hk, lambda e: self.hotkey_pressed(e), add=True)


if __name__ == '__main__':
    demo_buttonbox_1()
    demo_buttonbox_2()
    demo_buttonbox_3()
    demo_buttonbox_4()