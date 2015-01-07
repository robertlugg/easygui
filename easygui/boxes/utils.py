"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|

"""

import sys
import traceback


def write(*args):
    args = [str(arg) for arg in args]
    args = " ".join(args)
    sys.stdout.write(args)


def writeln(*args):
    write(*args)
    sys.stdout.write("\n")


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
    list of special keys, see this reference: http://infohost.nmt.edu/tcc/help/
    pubs/tkinter/web/key-names.html
    :param text:
    :return: list containing cleaned text, hotkey, and hotkey position within
    cleaned text.
    """

    ret_val = [text, None, None]  # Default return values
    if text is None:
        return ret_val

    # Single character, remain visible
    res = re.search('(?<=\[).(?=\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 1] + text[start:end] + text[end + 1:]
        ret_val = [caption, text[start:end], start - 1]

    # Single character, hide it
    res = re.search('(?<=\[\[).(?=\]\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [caption, text[start:end], None]

    # a Keysym.  Always hide it
    res = re.search('(?<=\[\<).+(?=\>\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [caption, '<{}>'.format(text[start:end]), None]

    return ret_val
