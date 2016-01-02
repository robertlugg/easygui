"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import os
try:
    from . import utils as ut
except (SystemError, ValueError, ImportError):
    import utils as ut

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font


# -------------------------------------------------------------------
# diropenbox
# -------------------------------------------------------------------
def diropenbox(msg=None, title=None, default=None):
    """
    A dialog to get a directory name.
    Note that the msg argument, if specified, is ignored.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str default: starting directory when dialog opens
    :return: Normalized path selected by user
    """
    title = ut.getFileDialogTitle(msg, title)
    localRoot = tk.Tk()
    localRoot.withdraw()
    if not default:
        default = None
    f = ut.tk_FileDialog.askdirectory(
        parent=localRoot, title=title, initialdir=default, initialfile=None
    )
    localRoot.destroy()
    if not f:
        return None
    return os.path.normpath(f)


if __name__ == '__main__':
    print("Hello from base_boxes")
