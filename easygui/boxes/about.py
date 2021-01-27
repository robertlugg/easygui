"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

"""
try:
    from .derived_boxes import codebox
except (SystemError, ValueError, ImportError):
    from derived_boxes import codebox

eg_version = '0.98.2-RELEASED'
egversion = eg_version


def abouteasygui():
    """
    Shows the EasyGUI revision history.
    """
    codebox("About EasyGui\n{}".format(eg_version),
            "EasyGui", EASYGUI_ABOUT_INFORMATION)
    return None


EASYGUI_ABOUT_INFORMATION = '''

0.98.2
========================================================================
Several updates and fixes thanks to Al and others.

0.98.0
========================================================================
This is an exciting time for easygui.  We continue to make good progress with refactoring as
well as some enhancements and bug fixes here and there.

We would like to welcome Juanjo Corrales to the team.  He is responsible for lots of good new work
this release.  Of course we appreciate the work of everyone who contributed.

NOTE: I decided in this release to change the API a bit.  Please consult the function documentation for details.

BUG FIXES
---------
 * Made changes guessing at fixes to any IDLE problems.  Please report any problems found.

ENHANCEMENTS
------------
 * Refactored the easygui.py file into several smaller files to improve our ability to manage the code
 * Added callbacks to allow for more dynamic dialogs.  See the docs for usage.
 * Added class access to dialogs so properties may be changed.
 * Improved button boxes ability to resize during window resize by converting to Tkinter grid from packer.

KNOWN ISSUES
------------
 * (old) In the documentation, there were previous references to issues when using the IDLE IDE.  I haven't
   experienced those, but also didn't do anything to fix them, so they may still be there.  Please report
   any problems and we'll try to address them

OTHER CHANGES
-------------
 * Centralized the Python 2 versus Python 3 "compatibility layer" into boxes/utils.py

========================================================================
0.97.4
========================================================================
This is a minor bug-fix release to address python 3 import errors.

========================================================================
0.97.3
========================================================================
Some more fixes especially to fix Debian distro problems.

========================================================================
0.97.1 & 0.97.2 (2014-12-24)
========================================================================
Boring, embarrassing uploads to fix pypi install problems.

========================================================================
0.97(2014-12-20)
========================================================================
We are happy to release version 0.97 of easygui.  The intent of this release is to address some basic
functionality issues as well as improve easygui in the ways people have asked.

Robert Lugg (me) was searching for a GUI library for my python work.  I saw easygui and liked very much its
paradigm.  Stephen Ferg, the creator and developer of easygui, graciously allowed me to start development
back up.  With the help of Alexander Zawadzki, Horst Jens, and others I set a goal to release before the
end of 2014.

We rely on user feedback so please bring up problems, ideas, or just say how you are using easygui.

BUG FIXES
---------
 * sourceforge #4: easygui docs contain bad references to easygui_pydoc.html
 * sourceforge #6: no index.html in docs download file.  Updated to sphinx which as autolinking.
 * sourceforge #8: unicode issues with file*box.  Fixed all that I knew how.
 * sourceforge #12: Cannot Exit with 'X'.  Now X and escape either return "cancel_button", if set, or None

ENHANCEMENTS
------------
 * Added ability to specify default_choice and cancel_choice for button widgets (See API docs)
 * True and False are returned instead of 1 and 0 for several boxes
 * Allow user to map keyboard keys to buttons by enclosing a hotkey in square braces like: "Pick [M]e", which would assign
   keyboard key M to that button.  Double braces hide that character, and keysyms are allowed:
     [[q]]Exit    Would show Exit on the button, and the button would be controlled by the q key
     [<F1>]Help   Would show Help on the button, and the button would be controlled by the F1 function key
   NOTE: We are still working on the exact syntax of these key mappings as Enter, space, and arrows are already being
         used.
 * Escape and the windows 'X' button always work in buttonboxes.  Those return None in that case.
 * sourceforge #9: let fileopenbox open multiple files.  Added optional argument 'multiple'
 * Location of dialogs on screen is preserved.  This isn't perfect yet, but now, at least, the dialogs don't
   always reset to their default position!
 * added some, but not all of the bugs/enhancements developed by Robbie Brook:
   http://all-you-need-is-tech.blogspot.com/2013/01/improving-easygui-for-python.html

KNOWN ISSUES
------------
 * In the documentation, there were previous references to issues when using the IDLE IDE.  I haven't
   experienced those, but also didn't do anything to fix them, so they may still be there.  Please report
   any problems and we'll try to address them
 * I am fairly new to contributing to open source, so I don't understand packaging, pypi, etc.  There
   are likely problems as well as better ways to do things.  Again, I appreciate any help or guidance.

Other Changes (that you likely don't care about)
------------------------------------------------
 * Restructured loading of image files to try PIL first throw error if file doesn't exiglobal_state.
 * Converted docs to sphinx with just a bit of docteglobal_state.  Most content was retained from the old site, so
   there might be some redundancies still.  Please make any suggested improvements.
 * Set up a GitHub repository for development: https://github.com/robertlugg/easygui

EasyGui is licensed under what is generally known as
the "modified BSD license" (aka "revised BSD", "new BSD", "3-clause BSD").
This license is GPL-compatible but less restrictive than GPL.

========================================================================
0.96(2010-08-29)
========================================================================
This version fixes some problems with version independence.

BUG FIXES
------------------------------------------------------
 * A statement with Python 2.x-style exception-handling syntax raised
   a syntax error when running under Python 3.x.
   Thanks to David Williams for reporting this problem.

 * Under some circumstances, PIL was unable to display non-gif images
   that it should have been able to display.
   The cause appears to be non-version-independent import syntax.
   PIL modules are now imported with a version-independent syntax.
   Thanks to Horst Jens for reporting this problem.

LICENSE CHANGE
------------------------------------------------------
Starting with this version, EasyGui is licensed under what is generally known as
the "modified BSD license" (aka "revised BSD", "new BSD", "3-clause BSD").
This license is GPL-compatible but less restrictive than GPL.
Earlier versions were licensed under the Creative Commons Attribution License 2.0.


========================================================================
0.95(2010-06-12)
========================================================================

ENHANCEMENTS
------------------------------------------------------
 * Previous versions of EasyGui could display only .gif image files using the
   msgbox "image" argument. This version can now display all image-file formats
   supported by PIL the Python Imaging Library) if PIL is installed.
   If msgbox is asked to open a non-gif image file, it attempts to import
   PIL and to use PIL to convert the image file to a displayable format.
   If PIL cannot be imported (probably because PIL is not installed)
   EasyGui displays an error message saying that PIL must be installed in order
   to display the image file.

   Note that
   http://www.pythonware.com/products/pil/
   says that PIL doesn't yet support Python 3.x.


========================================================================
0.94(2010-06-06)
========================================================================

ENHANCEMENTS
------------------------------------------------------
 * The codebox and textbox functions now return the contents of the box, rather
   than simply the name of the button ("Yes").  This makes it possible to use
   codebox and textbox as data-entry widgets.  A big "thank you!" to Dominic
   Comtois for requesting this feature, patiently explaining his requirement,
   and helping to discover the tkinter techniques to implement it.

   NOTE THAT in theory this change breaks backward compatibility.  But because
   (in previous versions of EasyGui) the value returned by codebox and textbox
   was meaningless, no application should have been checking it.  So in actual
   practice, this change should not break backward compatibility.

 * Added support for SPACEBAR to command buttons.  Now, when keyboard
   focus is on a command button, a press of the SPACEBAR will act like
   a press of the ENTER key; it will activate the command button.

 * Added support for keyboard navigation with the arrow keys (up,down,left,right)
   to the fields and buttons in enterbox, multenterbox and multpasswordbox,
   and to the buttons in choicebox and all buttonboxes.

 * added highlightthickness=2 to entry fields in multenterbox and
   multpasswordbox.  Now it is easier to tell which entry field has
   keyboard focus.


BUG FIXES
------------------------------------------------------
 * In EgStore, the pickle file is now opened with "rb" and "wb" rather than
   with "r" and "w".  This change is necessary for compatibility with Python 3+.
   Thanks to Marshall Mattingly for reporting this problem and providing the fix.

 * In integerbox, the actual argument names did not match the names described
   in the docstring. Thanks to Daniel Zingaro of at University of Toronto for
   reporting this problem.

 * In integerbox, the "argLowerBound" and "argUpperBound" arguments have been
   renamed to "lowerbound" and "upperbound" and the docstring has been corrected.

   NOTE THAT THIS CHANGE TO THE ARGUMENT-NAMES BREAKS BACKWARD COMPATIBILITY.
   If argLowerBound or argUpperBound are used, an AssertionError with an
   explanatory error message is raised.

 * In choicebox, the signature to choicebox incorrectly showed choicebox as
   accepting a "buttons" argument.  The signature has been fixed.


========================================================================
0.93(2009-07-07)
========================================================================

ENHANCEMENTS
------------------------------------------------------

 * Added exceptionbox to display stack trace of exceptions

 * modified names of some font-related constants to make it
   easier to customize them


========================================================================
0.92(2009-06-22)
========================================================================

ENHANCEMENTS
------------------------------------------------------

 * Added EgStore class to to provide basic easy-to-use persistence.

BUG FIXES
------------------------------------------------------

 * Fixed a bug that was preventing Linux users from copying text out of
   a textbox and a codebox.  This was not a problem for Windows users.

'''

if __name__ == '__main__':
    abouteasygui()
