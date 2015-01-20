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
import fileboxsetup as fbs

# -------------------------------------------------------------------
# fileopenbox
# -------------------------------------------------------------------


def fileopenbox(msg=None, title=None, default='*', filetypes=None, multiple=False):
    """
    A dialog to get a file name.

    **About the "default" argument**

    The "default" argument specifies a filepath that (normally)
    contains one or more wildcards.
    fileopenbox will display only files that match the default filepath.
    If omitted, defaults to "\*" (all files in the current directory).

    WINDOWS EXAMPLE::

        ...default="c:/myjunk/*.py"

    will open in directory c:\\myjunk\\ and show all Python files.

    WINDOWS EXAMPLE::

        ...default="c:/myjunk/test*.py"

    will open in directory c:\\myjunk\\ and show all Python files
    whose names begin with "test".


    Note that on Windows, fileopenbox automatically changes the path
    separator to the Windows path separator (backslash).

    **About the "filetypes" argument**

    If specified, it should contain a list of items,
    where each item is either:

    - a string containing a filemask          # e.g. "\*.txt"
    - a list of strings, where all of the strings except the last one
      are filemasks (each beginning with "\*.",
      such as "\*.txt" for text files, "\*.py" for Python files, etc.).
      and the last string contains a filetype description

    EXAMPLE::

        filetypes = ["*.css", ["*.htm", "*.html", "HTML files"]  ]

    .. note:: If the filetypes list does not contain ("All files","*"), it will be added.

    If the filetypes list does not contain a filemask that includes
    the extension of the "default" argument, it will be added.
    For example, if default="\*abc.py"
    and no filetypes argument was specified, then
    "\*.py" will automatically be added to the filetypes argument.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: filepath with wildcards
    :param object filetypes: filemasks that a user can choose, e.g. "\*.txt"
    :param bool multiple: If true, more than one file can be selected
    :return: the name of a file, or None if user chose to cancel
    """
    localRoot = tk.Tk()
    localRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fbs.fileboxSetup(
        default, filetypes)

    # ------------------------------------------------------------
    # if initialfile contains no wildcards; we don't want an
    # initial file. It won't be used anyway.
    # Also: if initialbase is simply "*", we don't want an
    # initialfile; it is not doing any useful work.
    # ------------------------------------------------------------
    if (initialfile.find("*") < 0) and (initialfile.find("?") < 0):
        initialfile = None
    elif initialbase == "*":
        initialfile = None

    func = ut.tk_FileDialog.askopenfilenames if multiple else ut.tk_FileDialog.askopenfilename
    ret_val = func(parent=localRoot,
                   title=ut.getFileDialogTitle(msg, title),
                   initialdir=initialdir, initialfile=initialfile,
                   filetypes=filetypes
                   )

    if multiple:
        f = [os.path.normpath(x) for x in localRoot.tk.splitlist(ret_val)]
    else:
        f = os.path.normpath(ret_val)

    localRoot.quit()

    if not f:
        return None
    return f


if __name__ == '__main__':
    print("Hello from file open box")
