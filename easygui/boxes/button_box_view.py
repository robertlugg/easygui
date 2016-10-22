
try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2
    import tkFont as tk_Font

try:
    from . import utils as ut
    from .button_box_controller import BoxController
except (SystemError, ValueError, ImportError):
    import utils as ut
    from button_box_controller import BoxController


class GUItk(object):
    """ Create the window the user sees, it relies on the tk library"""

    def __init__(self, model):  # type: (ButtonBoxModel) -> None
        """ Create ui object
            The ui object
        """
        self.model = model

        self.controller = BoxController(self.model)

        self.boxRoot = None
        self.messageArea = None
        self._images = None

    # Main methods - they are called from model ------------
    def configure(self, position, fixw_font_line_length, default_hpad_in_chars):
        self.boxRoot = tk.Tk()
        self.configure_root(self.model.title, position)

        # Calculate pad in points
        box_font = tk_Font.nametofont("TkFixedFont")
        char_width = box_font.measure('W')
        pad_in_points = default_hpad_in_chars * char_width

        # msg widget sets the overall width of the window
        self.create_msg_widget(self.model.msg, fixw_font_line_length, pad_in_points)

        imagesFrame = self.create_images_frame()
        self.create_images(imagesFrame, self.model.images)

        buttonsFrame = self.create_buttons_frame()
        self.create_buttons(buttonsFrame, self.model.choices)

    def run(self):
        self.boxRoot.mainloop()
        self.boxRoot.destroy()

    def update(self):
        if self.model.changed_msg:
            self.set_msg(self.model.msg)
            self.model.changed_msg = False

    def get_position_on_screen(self):
        # The geometry() method returns a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        position = '+' + geom.split('+', 1)[1]
        return position

    def stop(self):
        self.boxRoot.quit()

    # Methods to change content ---------------------------------------
    def set_msg(self, msg): # type: (str) -> None
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

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def configure_root(self, title, position):
        self.boxRoot.title(title)

        self.set_position_on_screen(position)

        # Resize setup
        self.boxRoot.columnconfigure(0, weight=10)
        self.boxRoot.minsize(100, 200)

        # Quit when x button pressed
        self.boxRoot.protocol('WM_DELETE_WINDOW', self.controller.x_pressed)
        self.boxRoot.bind("<Escape>", self.controller.escape_pressed)

        self.boxRoot.iconname('Dialog')

    def set_position_on_screen(self, pos):
        # The geometry("250x150+300+300") method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        self.boxRoot.geometry(pos)

    def create_msg_widget(self, msg, width_in_chars, pad_in_points):

        if msg is None:
            msg = ""

        self.messageArea = tk.Text(
            self.boxRoot,
            width=width_in_chars,
            state=tk.DISABLED,
            padx=pad_in_points,
            relief="flat",
            background=self.boxRoot.config()["background"][-1],
            pady=pad_in_points,
            wrap=tk.WORD,
        )
        self.messageArea.tag_config('justify', justify=tk.CENTER)
        self.set_msg(msg)
        self.messageArea.grid(row=0)
        self.boxRoot.rowconfigure(0, weight=10, minsize='10m')

    def create_images_frame(self):
        imagesFrame = tk.Frame(self.boxRoot)
        row = 1
        imagesFrame.grid(row=row)
        self.boxRoot.rowconfigure(row, weight=10, minsize='10m')
        return imagesFrame

    def create_images(self, imagesFrame, img_filenames):
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
                    imagesFrame,
                    takefocus=1,
                    compound=tk.TOP)
                if this_image['widget'] is not None:
                    this_image['widget'].configure(image=this_image['tk_image'])
                fn = create_command(filename, _r, column_number)
                this_image['widget'].configure(command=fn)
                sticky_dir = tk.N+tk.S+tk.E+tk.W
                this_image['widget'].grid(row=row_number, column=column_number, sticky=sticky_dir, padx='1m', pady='1m', ipadx='2m', ipady='1m')
                imagesFrame.rowconfigure(row_number, weight=10, minsize='10m')
                imagesFrame.columnconfigure(column_number, weight=10)
                images.append(this_image)
        self._images = images  # Image objects must live, so place them in self.  Otherwise, they will be deleted.

    def create_buttons_frame(self):
        buttonsFrame = tk.Frame(self.boxRoot)
        buttonsFrame.grid(row=2, column=0)
        return buttonsFrame

    def create_buttons(self, buttonsFrame, choices):

        def create_command(choice):
            def command(event=None):
                return self.controller.button_or_hotkey_pressed(choice)
            return command

        # Create buttons dictionary and Tkinter widgets
        buttons = dict()

        for column, choice in enumerate(choices.choices.values()):
            if choice.original_text == 'No choice':
                continue
            button = tk.Button(
                buttonsFrame,
                takefocus=1,
                text=choice.clean_text,
                underline=choice.hotkey_position)

            command_to_call = create_command(choice)

            button.configure(command=command_to_call)

            button.grid(row=0, column=column, padx='1m', pady='1m', ipadx='2m', ipady='1m')

            buttonsFrame.columnconfigure(column, weight=10)

            if choice.default:
                button.focus_force()

            buttons[choice.unique_text] = button

            # Bind hotkey
            if choice.hotkey:
                self.boxRoot.bind_all(choice.hotkey, command_to_call, add=True)

            # Also bind to its lowercase version if exists
            if choice.lowercase_hotkey:
                self.boxRoot.bind_all(choice.lowercase_hotkey, command_to_call, add=True)

        return buttons


