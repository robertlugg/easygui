"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import os
import sys

from . import utils as ut
tk = ut.tk
from . import fileboxsetup as fbs


# -------------------------------------------------------------------
# filesavebox
# -------------------------------------------------------------------


def filesavebox(msg=None, title=None, default="", filetypes=None):
    """
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    The "default" argument should contain a filename (i.e. the
    current name of the file to be saved).  It may also be empty,
    or contain a filemask that includes wildcards.

    The "filetypes" argument works like the "filetypes" argument to
    fileopenbox.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: default filename to return
    :param object filetypes: filemasks that a user can choose, e.g. " \*.txt"
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
