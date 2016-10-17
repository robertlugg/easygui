
try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2
    import tkFont as tk_Font

try:
    from . import global_state
    from . import utils as ut
    from .button_box_controller import BoxController
except (SystemError, ValueError, ImportError):
    import global_state
    import utils as ut
    from button_box_controller import BoxController

import re


class GUItk(object):
    """ This is the object that contains the tk root object"""

    def __init__(self, model):
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
        self.model = model

        self.controller = BoxController(self.model)

        self.boxRoot = tk.Tk()
        # self.boxFont = tk_Font.Font(
        #     family=global_state.PROPORTIONAL_FONT_FAMILY,
        #     size=global_state.PROPORTIONAL_FONT_SIZE)

        self.boxFont = tk_Font.nametofont("TkFixedFont")
        self.width_in_chars = global_state.fixw_font_line_length

        # default_font.configure(size=global_state.PROPORTIONAL_FONT_SIZE)

        self.configure_root(self.model.title)

        self.create_msg_widget(self.model.msg)

        self.create_images_frame()

        self.create_images(self.model.images)

        self.create_buttons_frame()

        self.buttons = self.create_buttons(self.model.choices)


    # Run, stop and update methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def stop(self):
        # Get the current position before quitting
        #self.get_pos()
        self.boxRoot.quit()

    def update_view(self):
        if self.model.stop:
            self.stop()
        if self.model.changed_msg:
            self.set_msg(self.model.msg)
            self.model.changed_msg = False

    # Methods to change content ---------------------------------------
    def set_msg(self, msg):
        self.messageArea.config(state=tk.NORMAL)
        self.messageArea.delete(1.0, tk.END)
        self.messageArea.insert(tk.END, msg, 'justify')
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

    def remember_window_position(self):
        # Determine window location and save to global
        # TODO: Not sure where this goes, but move it out of here!
        m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", self.boxRoot.geometry())
        if not m:
            raise ValueError(
                "failed to parse geometry string: {}".format(self.boxRoot.geometry()))
        width, height, xoffset, yoffset = [int(s) for s in m.groups()]
        global_state.window_position = '{0:+g}{1:+g}'.format(xoffset, yoffset)

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
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.controller.x_pressed)
        self.boxRoot.bind("<Escape>", self.controller.escape_pressed)
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
        self.messageArea.tag_config('justify', justify=tk.CENTER)
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

        def create_command(filename, row, column):
            def command():
                return self.controller.image_pressed(filename, row, column)
            return command


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
                fn = create_command(filename, _r, column_number)
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

    def create_buttons(self, choices):

        def create_command(button_text):
            def command():
                return self.controller.button_pressed(button_text)
            return command

        def command_when_hotkey_pressed(event):
            self.remember_window_position()
            return self.controller.hotkey_pressed(event.keysym, event.char)

        # Create buttons dictionary and Tkinter widgets
        buttons = dict()

        for column, choice in enumerate(choices.choices.values()):
            if choice.original_text == 'No choice':
                continue
            button = tk.Button(
                self.buttonsFrame,
                takefocus=1,
                text=choice.clean_text,
                underline=choice.hotkey_position)

            command_when_pressed = create_command(choice)

            button.configure(command=command_when_pressed)

            button.grid(row=0, column=column, padx='1m', pady='1m', ipadx='2m', ipady='1m')

            self.buttonsFrame.columnconfigure(column, weight=10)

            if choice.default:
                button.focus_force()

            # Add the choice as one property of a tk.Button
            button.choice = choice

            buttons[choice.unique_text] = button

            # Bind hotkey
            if choice.hotkey:
                self.boxRoot.bind_all(choice.hotkey, command_when_hotkey_pressed, add=True)

            # Also bind to its lowercase version if exists
            if choice.lowercase_hotkey:
                self.boxRoot.bind_all(choice.lowercase_hotkey, command_when_hotkey_pressed, add=True)

        return buttons

