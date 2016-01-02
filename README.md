EasyGUI
=======

EasyGUI is a module for very simple, very easy GUI programming in Python. EasyGUI is different from other GUI
libraries in that EasyGUI is NOT event-driven. Instead, all GUI interactions are invoked by simple function calls.

EasyGUI runs on Python 2 and 3, and does not have any dependencies beyond python.

Example Usage
-------------

    >>> import easygui
    >>> easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
    1
    >>> easygui.msgbox('This is a basic message box.', 'Title Goes Here')
    'OK'
    >>> easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
    'Chocolate'


Full documentation is always available.

For the most-recent production version:
<http://easygui.readthedocs.org/en/master/>.

For our develop version which will be released next:
<http://easygui.readthedocs.org/en/develop>.

========================================================================
0.98.0
========================================================================
This is an exciting time for easygui.  We continue to make good progress with refactoring as
well as some enhancements and bug fixes here and there.

We would like to welcome Juanjo Denis-Corrales to the team.  He is responsible for lots of good new work
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

KNOWN ISSUES
------------
 * There were previous issues when using easygui with the IDLE IDE.  I hope I resolved these problems, however,
   I've never actually been able to repeat them.  Please report any problems found in github.

OTHER CHANGES
-------------
 * Centralized the Python 2 versus Python 3 "compatibility layer" into boxes/utils.py


0.97.4
========================================================================
This is a minor bug-fix release to address python 3 import errors.

0.97.3
========================================================================
We are happy to release version 0.97.3 of easygui.  The intent of this release is to address some basic
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
 * Restructured loading of image files to try PIL first throw error if file doesn't exist.
 * Converted docs to sphinx with just a bit of doctest.  Most content was retained from the old site, so
   there might be some redundancies still.  Please make any suggested improvements.
 * Set up a GitHub repository for development: https://github.com/robertlugg/easygui
 * Improved output/packaging for Debian distribution

EasyGui is licensed under what is generally known as
the "modified BSD license" (aka "revised BSD", "new BSD", "3-clause BSD").
This license is GPL-compatible but less restrictive than GPL.
