import os
import re
import tkinter as tk

from easygui.global_state import PROP_FONT_LINE_LENGTH, FIXW_FONT_LINE_LENGTH, DEFAULT_PADDING, REGULAR_FONT_WIDTH, \
    FIXED_FONT_WIDTH, GLOBAL_WINDOW_POSITION


class AbstractBox(object):
    """
    The following boxes have commonalities, so we can abstract some code here to a parent class
        ButtonBox:          def __init__(self, msg, title, choices, images, default_choice, cancel_choice, callback):
        ChoiceBox:          def __init__(self, msg, title, choices, preselect, multiple_select, callback):
        FillableBox:        def __init__(self, msg, title, default, mask=None, image=None, root=None):
        MultiFillableBox:   def __init__(self, msg, title, fields=None, values=None, mask_last=False, callback=None):
        TextBox             def __init__(self, msg, title, text, codebox, callback):
    """

    def __init__(self, msg, title, callback, monospace=False) -> None:
        super().__init__()
        self._user_specified_callback = callback
        self.box_root = self._configure_box_root(title)
        self.set_message(msg, monospace)
        self.return_value = None

    def _set_return_value(self):
        raise NotImplemented

    def _configure_box_root(self, title):
        box_root = tk.Tk()
        box_root.title(title)
        box_root.iconname('Dialog')
        box_root.geometry(GLOBAL_WINDOW_POSITION)
        box_root.bind("<Escape>", self.cancel_button_pressed)
        box_root.protocol('WM_DELETE_WINDOW', self.cancel_button_pressed)
        return box_root

    def set_message(self, msg, monospace):
        """
        # TODO: fix bug that the line count does not include wrapped lines
        # height = message.tk.call((self.mess\age._w, "count", "-update", "-displaylines", "1.0", "end"))
        :param msg:
        :param bool monospace: whether the message shold be monospace or proportional text
        :return:
        """
        padding, width_in_chars = get_width_and_padding(monospace=monospace)

        message_frame = tk.Frame(self.box_root, padx=padding)
        message_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        message_text = tk.Text(
            master=message_frame,
            width=width_in_chars,
            padx=padding,
            pady=padding,
            wrap=tk.WORD,
            # wrap=tk.NONE if monospace else tk.WORD
        )
        message_text.insert(tk.END, msg)
        message_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        line, char = message_text.index(tk.END).split('.')
        message_text.configure(height=int(line))
        message_text.configure(state=tk.DISABLED)

    def cancel_button_pressed(self, *args):
        """
        Set the return value to None so that and quit the mainloop()
        Care: may be called:
         * with zero args when handling a window close action
         * with one arg when handling an Escape button precessed binding
        :param args: zero or more args
        :return: None
        """
        self.return_value = None
        self.box_root.quit()

    def ok_button_pressed(self, _):
        self._set_return_value()
        if self._user_specified_callback:
            # If a callback was set, call main process
            self._user_specified_callback(self)
        else:
            self.stop()

    def run(self):
        self.box_root.mainloop()
        self.box_root.destroy()
        return self.return_value

    def stop(self):
        self.box_root.quit()


def parse_hotkey(text):
    """
    Extract a desired hotkey from the text.  The format to enclose
    the hotkey in square braces
    as in Button_[1] which would assign the keyboard key 1 to that button.
      The one will be included in the
    button text.  To hide they key, use double square braces as in:  Ex[[qq]]
    it  , which would assign
    the q key to the Exit button. Special keys such as <Enter> may also be
    used:  Move [<left>]  for a full
    list of special keys, see this reference: http://infohoglobal_state.nmt.edu/tcc/help/
    pubs/tkinter/web/key-names.html
    :param text:
    :return: list containing cleaned text, hotkey, and hotkey position within
    cleaned text.
    """

    ret_val = [text, None, None]  # Default return values
    if text is None:
        return ret_val

    # Single character, remain visible
    res = re.search(r'(?<=\[).(?=\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 1] + text[start:end] + text[end + 1:]
        ret_val = [caption, text[start:end], start - 1]

    # Single character, hide it
    res = re.search(r'(?<=\[\[).(?=\]\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [caption, text[start:end], None]

    # a Keysym.  Always hide it
    res = re.search(r'(?<=\[\<).+(?=\>\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [caption, '<{}>'.format(text[start:end]), None]

    return ret_val


def load_tk_image(filename, tk_master=None):
    """
    Load in an image file and return as a tk Image.

    Loads an image.  If the PIL library is available use it.  otherwise use the tk method.

    NOTE: tk_master is required if there are more than one Tk() instances, which there are very often.
      REF: http://stackoverflow.com/a/23229091/2184122

    :param filename: image filename to load
    :param tk_master: root object (Tk())
    :return: tk Image object
    """

    if filename is None:
        return None

    if not os.path.isfile(filename):
        raise ValueError(
            'Image file {} does not exist.'.format(filename))

    tk_image = None

    filename = os.path.normpath(filename)
    _, ext = os.path.splitext(filename)

    try:
        # Try to import the Python Image Library.  If it doesn't exist, only .gif
        from PIL import Image as PILImage
        from PIL import ImageTk as PILImageTk
        pil_image = PILImage.open(filename)
        tk_image = PILImageTk.PhotoImage(pil_image, master=tk_master)
    except:
        try:
            # Fallback if PIL isn't available
            tk_image = tk.PhotoImage(file=filename, master=tk_master)
        except:
            msg = "Cannot load {}.  Check to make sure it is an image file.".format(
                filename)
            try:
                _ = PILImage
            except:
                msg += "\nPIL library isn't installed.  If it isn't installed, only .gif files can be used."
            raise ValueError(msg)
    return tk_image


def get_width_and_padding(monospace):
    if monospace:
        padding = DEFAULT_PADDING * FIXED_FONT_WIDTH
        width_in_chars = FIXW_FONT_LINE_LENGTH
    else:
        padding = DEFAULT_PADDING * REGULAR_FONT_WIDTH
        width_in_chars = PROP_FONT_LINE_LENGTH
    return padding, width_in_chars


class MouseClickHandler:
    """ Handle mouse events with state to store whether the mouse is actually on a button or not.
        This lets us ensure that:
         * button presses are handled on mouse-release, *not* immediately on mouse-click
         * callbacks are only called if there is a mouse-button release *and* your cursor is still on the button
    """

    def __init__(self, callback):
        self._callback = callback
        self._mouse_is_on_button = False

    def enter(self, _):
        self._mouse_is_on_button = True

    def leave(self, _):
        self._mouse_is_on_button = False

    def release(self, event):
        if self._mouse_is_on_button:
            return self._callback(event)


def bind_to_mouse(button, callback):
    handler = MouseClickHandler(callback=callback)
    button.bind("<Enter>", handler.enter)
    button.bind("<Leave>", handler.leave)
    button.bind("<ButtonRelease-1>", handler.release)
