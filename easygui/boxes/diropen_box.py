"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""


import os
import sys

# Refs:
#   https://www.python.org/dev/peps/pep-0366
#   http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py
if __name__ == "__main__" and __package__ is None:
    from os import path
    sys.path.append(path.dirname(path.abspath(__file__)))
import utils as ut
tk = ut.tk


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
    localRoot.quit()
    if not f:
        return None
    return os.path.normpath(f)


if __name__ == '__main__':
    print("Hello from base_boxes")
