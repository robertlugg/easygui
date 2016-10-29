
try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2
    import tkFont as tk_Font

try:
    from . import utils as ut
except (SystemError, ValueError, ImportError):
    import utils as ut


class ViewTk(object):
    """ Create the window the user sees, it relies on the tk library"""

    def __init__(self, model):  # type: (ButtonBoxModel) -> None
        """ Create ui object
            The ui object
        """
        self.model = model

        self.root = None
        self.message_area = None

        self.images = None

    # Main methods - they are called from model ------------
    def configure(self, position, fixw_font_line_length, default_hpad_in_chars):
        self.root = tk.Tk()
        self.configure_root(self.model.title, position)

        # Calculate pad in points
        box_font = tk_Font.nametofont("TkFixedFont")
        char_width = box_font.measure('W')
        pad_in_points = default_hpad_in_chars * char_width

        # The msg widget sets the overall width of the window
        self.create_msg_widget(self.model.msg, fixw_font_line_length, pad_in_points)

        images = self.create_images(self.model.images)
        self.images = images  # Image objects must live, so place them in self.  Otherwise, they will be deleted.

        self.create_buttons(self.model.choices)

    def run(self):
        self.root.mainloop()
        self.root.destroy()

    def set_msg(self, msg):  # type: (str) -> None
        self.message_area.config(state=tk.NORMAL)
        self.message_area.delete(1.0, tk.END)
        self.message_area.insert(tk.END, msg, 'visual_style')
        self.message_area.config(state=tk.DISABLED)

        # Adjust msg height
        self.message_area.update()

        # Get number of lines of message area
        end_position = self.message_area.index(tk.END)  # '4.0'
        end_line = end_position.split('.')[0]  # 4
        numlines = int(end_line) + 1  # 5

        # Set msg height to the number of lines
        self.message_area.configure(height=numlines)

        self.message_area.update()

    def get_position_on_screen(self):
        # The geometry() method returns a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.root.geometry()  # "628x672+300+200"
        position = '+' + geom.split('+', 1)[1]
        return position

    def stop(self):
        self.root.quit()

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title, position):
        self.root.title(title)

        self.set_position_on_screen(position)

        # Resize setup
        self.root.columnconfigure(0, weight=10)
        self.root.minsize(100, 200)

        # Quit when x button pressed
        self.root.protocol('WM_DELETE_WINDOW', self.model.x_pressed)
        self.root.bind("<Escape>", self.model.escape_pressed)

        self.root.iconname('Dialog')

    def set_position_on_screen(self, pos):
        # The geometry("250x150+300+300") method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        self.root.geometry(pos)

    def create_msg_widget(self, msg, width_in_chars, pad_in_points):

        if msg is None:
            msg = ""

        self.message_area = tk.Text(
            self.root,
            width=width_in_chars,
            state=tk.DISABLED,
            padx=pad_in_points,
            relief="flat",
            background=self.root.config()["background"][-1],
            pady=pad_in_points,
            wrap=tk.WORD,
        )
        
        # Create style of the message to insert
        self.message_area.tag_config('visual_style', justify=tk.CENTER)
        
        # Insert the message
        self.set_msg(msg)

        self.message_area.grid(row=0)
        self.root.rowconfigure(0, weight=10, minsize='10m')

    def create_images(self, img_filenames):
        """
        Create one or more images in the dialog.
        :param img_filenames:
         a list of list of filenames
        :return:
        """

        if img_filenames is None:
            return

        # Create frame
        images_frame = tk.Frame(self.root)
        row = 1
        images_frame.grid(row=row)
        self.root.rowconfigure(row, weight=10, minsize='10m')

        def create_command(name_of_file, row, column):
            def command():
                return self.model.image_pressed(name_of_file, row, column)
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
                    images_frame,
                    takefocus=1,
                    compound=tk.TOP)
                if this_image['widget'] is not None:
                    this_image['widget'].configure(image=this_image['tk_image'])
                fn = create_command(filename, _r, column_number)
                this_image['widget'].configure(command=fn)
                sticky_dir = tk.N+tk.S+tk.E+tk.W
                this_image['widget'].grid(row=row_number, column=column_number, sticky=sticky_dir, padx='1m', pady='1m', ipadx='2m', ipady='1m')
                images_frame.rowconfigure(row_number, weight=10, minsize='10m')
                images_frame.columnconfigure(column_number, weight=10)
                images.append(this_image)
        return images

    def create_buttons(self, choices):

        # Create buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.grid(row=2, column=0)

        # Function that creates commands to associate with buttons
        # This one is tricky, is a function that returns a function
        # The function returned belongs to the model,
        # and it holds a reference to a determined choice
        def create_command(choice_associated_with_command):
            def command(event=None):
                return self.model.button_or_hotkey_pressed(choice_associated_with_command)
            return command

        # Create buttons
        for column, choice in enumerate(choices):

            button = tk.Button(
                buttons_frame,
                takefocus=1,
                text=choice.clean_text,
                underline=choice.hotkey_position)

            button.grid(row=0, column=column, padx='1m', pady='1m', ipadx='2m', ipady='1m')

            buttons_frame.columnconfigure(column, weight=10)

            if choice.default:
                button.focus_force()

            # Create command to call when button is pressed
            command_to_call = create_command(choice)

            # Bind command to button press
            button.configure(command=command_to_call)

            # Bind command to hotkey
            if choice.hotkey:
                self.root.bind_all(choice.hotkey, command_to_call, add=True)

            # Also bind to its lowercase version if exists
            if choice.lowercase_hotkey:
                self.root.bind_all(choice.lowercase_hotkey, command_to_call, add=True)

        return


