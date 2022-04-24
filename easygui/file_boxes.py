from os.path import normpath

from tkinter import filedialog


def diropenbox(title='Open', default_directory=None):
    """
    A dialog to get a directory name.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.

    :param str msg: used in the window title
    :param str msg: used in the window title on some platforms
    :param str title: the window title
    :param str default: starting directory when dialog opens
    :return: Normalized path selected by user
    """
    directory_path = filedialog.askdirectory(title=title, initialdir=default_directory)
    return None if directory_path is None else normpath(directory_path)


def filesavebox(title='Save As', default_directory="", filetypes=None):
    """A dialog box to get the name of a file. Return the name of a file, or None if user chose to cancel """
    file_path = filedialog.asksaveasfilename(title=title, initialdir=default_directory, filetypes=filetypes)
    return None if file_path is None else normpath(file_path)


def fileopenbox(title='Open', default_directory='*', filetypes=(), multiple=False):
    """ A dialog to get a file name.
    fileopenbox automatically changes the path separator to backslash on Windows.

    :param str title: the window title
    :param str default_directory: filepath to search, may contain wildcards, defaults to all files in current directory
    :param object filetypes: a file pattern OR a list of file patterns and a file type description
                            eg. ["*.css", ["*.htm", "*.html", "HTML files"]  ]
                            If the filetypes list does not contain ("All files","*"), it will be added.
    :param bool multiple: allow selection of more than one file
    :return: the name of a file, or None if user chose to cancel
    """
    kwargs = dict(title=title, initialdir=default_directory, filetypes=filetypes)

    if multiple:
        filenames = filedialog.askopenfilenames(**kwargs)
        return None if filenames is None else [normpath(x) for x in filenames]

    else:
        filename = filedialog.askopenfilename(**kwargs)
        return None if filename is None else normpath(filename)
