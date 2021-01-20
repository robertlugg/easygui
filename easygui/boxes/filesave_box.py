"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import os

try:
    from . import utils as ut
    from . import fileboxsetup as fbs
except (SystemError, ValueError, ImportError):
    import utils as ut
    import fileboxsetup as fbs

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except:
    import Tkinter as tk  # python 2
    import tkFont as tk_Font



# -------------------------------------------------------------------
# filesavebox
# -------------------------------------------------------------------


def filesavebox(msg=None, title=None, default="", filetypes=None):
    """
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    **About the "default" argument**

    The ``default`` argument specifies the path and "glob pattern" for file
    names. The "\\*" value, for example, sets the open file dialog to the
    current working directory and showing all files.

    For another example, setting the ``default`` argument to ``"C:/myjunk/*.py"``
    sets the open file dialog to the C:\\myjunk folder and showing only files
    that have the .py file extension. This glob pattern at the end of the
    ``default`` argument is required: passing ``"C:/myjunk"`` would not set the
    open file dialog to the C:\\myjunk folder, but rather to the C:\\ folder
    and "myjunk" as the initial filename.

    Note that on Windows, ``fileopenbox()`` automatically changes the path
    separator to the Windows path separator (backslash).


    The "filetypes" argument works like the "filetypes" argument to
    fileopenbox.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: default filename to return
    :param object filetypes: filemasks that a user can choose, e.g. " \\*.txt"
    :return: the name of a file, or None if user chose to cancel
    """

    localRoot = tk.Tk()
    localRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fbs.fileboxSetup(
        default, filetypes)

    f = ut.tk_FileDialog.asksaveasfilename(
        parent=localRoot,
        title=ut.getFileDialogTitle(
            msg, title),
        initialfile=initialfile, initialdir=initialdir,
        filetypes=filetypes
    )
    localRoot.destroy()
    if not f:
        return None
    return os.path.normpath(f)


if __name__ == '__main__':
    print("Hello from file save box")
    ret_val = filesavebox("Please select a file to save to", "My File Save dialog")
    print("Return value is:{}".format(ret_val))