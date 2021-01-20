"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|

"""

import os
import sys
import traceback

# A set of variables and functions to centralize differences between
# python 2 and 3
runningPython27 = False
runningPython34 = False
if 0x020700F0 <= sys.hexversion <= 0x030000F0:
    runningPython27 = True
if 0x030400F0 <= sys.hexversion <= 0x040000F0:
    runningPython34 = True
if not runningPython27 and not runningPython34:
    raise Exception("You must run on Python 2.7+ or Python 3.4+")

# Import Tkinter, the tk filedialog, and put everything in tkinter into
# the current namespace
try:
    import tkinter as tk  # python3
    # TODO: Ultimately this should go away once everything stops using it.
    from tkinter import *
    import tkinter.filedialog as tk_FileDialog
    import tkinter.font as tk_Font
except ImportError:
    try:
        import Tkinter as tk  # python2
        # TODO: Ultimately this should go away once everything stops using it.
        from Tkinter import *
        import tkFileDialog as tk_FileDialog
        import tkFont as tk_Font

    except ImportError:
        raise ImportError("Unable to find tkinter package.")

if tk.TkVersion < 8.0:
    raise ImportError("You must use python-tk (tkinter) version 8.0 or higher")


# Try to import the Python Image Library.  If it doesn't exist, only .gif
# images are supported.
try:
    from PIL import Image as PILImage
    from PIL import ImageTk as PILImageTk
except:
    pass

# Code should use 'basestring' anywhere you might think to use the system 'str'.  This is all to support
# Python 2.  If 2 ever goes away, this logic can go away and uses of
# utils.basestring should be changed to just str
if runningPython27:
    basestring = basestring
if runningPython34:
    basestring = str


# -----------------------------------------------------------------------
# exception_format
# -----------------------------------------------------------------------
def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))


# -------------------------------------------------------------------
# utility routines
# -------------------------------------------------------------------
# These routines are used by several other functions in the EasyGui module.

def uniquify_list_of_strings(input_list):
    """
    Ensure that every string within input_list is unique.
    :param list input_list: List of strings
    :return: New list with unique names as needed.
    """
    output_list = list()
    for i, item in enumerate(input_list):
        tempList = input_list[:i] + input_list[i + 1:]
        if item not in tempList:
            output_list.append(item)
        else:
            output_list.append('{0}_{1}'.format(item, i))
    return output_list

import re


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


# -------------------------------------------------------------------
# getFileDialogTitle
# -------------------------------------------------------------------
def getFileDialogTitle(msg, title):
    """
    Create nicely-formatted string based on arguments msg and title
    :param msg: the msg to be displayed
    :param title: the window title
    :return: None
    """
    if msg and title:
        return "%s - %s" % (title, msg)
    if msg and not title:
        return str(msg)
    if title and not msg:
        return str(title)
    return None  # no message and no title


if __name__ == '__main__':
    print("Hello from utils")
