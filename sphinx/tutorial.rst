EasyGUI Tutorial
================

.. toctree::
   :maxdepth: 4

Introduction
------------
In EasyGUI, all GUI dialog windows are invoked by simple function calls. Linux users may need to run (for Python 2) ``sudo apt-get install python-tk`` **or** ``sudo apt-get install python3-tk`` for Python3, in order to install the tkinter dependency.  
Here is a simple demo program using easygui:

.. doctest::

    import easygui
    import sys

    # A nice welcome message:
    ret_val = easygui.msgbox("Hello, World!")
    if ret_val is None:  # msgbox() returns None if the window was closed.
        sys.exit()

    msg ="What is your favorite flavor?\nOr Press <cancel> to exit."
    title = "Ice Cream Survey"
    choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
    while True:
        choice = easygui.choicebox(msg, title, choices)
        if choice is None:
            sys.exit()
        easygui.msgbox("You chose: " + choice, "Survey Result")


EasyGUI's Demonstration Routine
-------------------------------
To run EasyGUI's demonstration routine, invoke EasyGUI from the command line this way::

    python easygui.py

or this way::

    python -m easygui

or from an IDE (such as IDLE, PythonWin, Wing, etc.) this way::

    from easygui import *
    egdemo()

The source code for these demo programs are in the ``test_cases`` folder in the git repo.
This allows you to try out the various EasyGUI functions,
and prints the results of your choices to the console.

Importing EasyGUI
-----------------
In order to use EasyGUI, you must import it. The simplest ``import`` statement is::

    import easygui

If you use this form, you must prefix EasyGUI functions with ``easygui``, this way::

    import easygui
    easygui.msgbox('Hello!')

One alternative is to import EasyGUI this way::

    from easygui import *

This lets you invoke the EasyGUI functions without the "easygui" prefix::

    from easygui import *
    msgbox('Hello!')

A third alternative is to use something like the following ``import`` statement::

    import easygui as eg

This allows you to keep the EasyGUI namespace separate with a minimal amount of typing. You can access EasyGUI functions like this::

    import easygui as eg
    eg.msgbox('Hello!')

This third alterative is actually the best way to do it once you get used to Python and EasyGUI.


Default Arguments for EasyGUI Functions
---------------------------------------
The first two arguments for GUI box functions are for the message and title,
respectively. In some cases, this might not be the most user-friendly
arrangement (for example, the dialogs for getting directory and filenames
ignore the message argument), but I felt that keeping this consistent
across all widgets was a consideration that is more important.

Most arguments to EasyGUI functions have defaults. The title defaults
to the empty string, and the message usually has a simple default.

For instance, the title argument to msgbox
is optional, so you can call msgbox specifying only a message, this way::

    easygui.msgbox("Danger, Will Robinson!")

...or specifying a message and a title, this way::

    easygui.msgbox("Danger, Will Robinson!", "Warning!")

On the various types of buttonbox, the default message is "Shall I continue?",
so you can (if you wish) invoke them without arguments at all. Here we
invoke ``ccbox()`` (the close/cancel box, which returns a boolean value) without
any arguments at all::

    if easygui.ccbox():
        pass  # User chose to continue.
    else:
        return  # User chose to cancel.

Using Keyword Arguments When Calling EasyGUI Functions
------------------------------------------------------
It is possible to use keyword arguments when calling EasyGUI functions.

Suppose for instance that you wanted to use a buttonbox, but
(for whatever reason) did not want to specify the title (second) positional
argument. You could still specify the choices argument (the third argument)
using a keyword, this way::

    choices = ["Yes", "No", "Only on Friday"]
    reply = easygui.choicebox("Do you like to eat fish?", choices=choices)

Using buttonboxes
-----------------

There are a number of functions built on top of ``buttonbox()`` for common needs.

- ``msgbox()`` displays a text message dialog box with a single OK button, and returns ``'OK'``.
- ``ccbox()`` displays a dialog box with Continue and Cancel buttons, and returns ``True`` or ``False``.
- ``ynbox()`` displays a dialog box with Yes and No buttons, and returns ``True`` or ``False``.
- ``buttonbox()`` displays a dialog box with custom buttons, and returns the text of the selected button.
- ``indexbox()`` displays a dialog box with custom buttons, and returns the integer index of the selected button (starting at ``0``).
- ``boolbox()`` displays a dialog box with True and False buttons, and returns ``True`` or ``False``.
- ``choicebox()`` displays a dialog box with a list of selectable items, and returns the text of the selected choice.
- ``multchoicebox()`` displays a dialog box with a list of selectable items, and returns a list of the selected choices.
- ``enterbox()`` lets the user enter a string into a text field, which is returned.
- ``integerbox()`` lets the user enter an integer into a text field, which is returned. (Non-integers cause an error box to appear.)
- ``multenterbox()`` displays a dialog box with labeled text fields for the user to enter replies, which are returned as a list of strings.
- ``passwordbox()`` lets the user enter a string into a text field which masks the input. The entered password is returned.
- ``multpasswordbox()`` displays a dialog box with labeled text fields for the user to enter replies, the last of which is masked. This is suitable for username/password dialogs. The entered replies are returned as a list of strings.
- ``textbox()`` displays a dialog box with a large, multi-line text box, and returns the entered text as a string. The message text is displayed in a proportional font and wraps.
- ``codebox()`` displays a dialog box with a large, multi-line text box, and returns the entered text as a string. The message text is displayed in a monospace font and doesn't wrap.
- ``diropenbox()`` displays an "open directory" dialog box and returns the name of the selected directory.
- ``fileopenbox()`` displays an "open file" dialog box and returns the name of the selected file.
- ``filesavebox()`` displays a "save file" dialog box and returns the name of the selected file.

msgbox()
^^^^^^^^
The ``msgbox()`` function displays a text message and offers an OK button. The message text appears in the center of the window, the title text appears in the title bar, and you can replace the "OK" default text on the button. Here is the signature::

    def msgbox(msg="(Your message goes here)", title="", ok_button="OK"):
        ....

The clearest way to override the button text is to do it with a keyword
argument, like this::

    easygui.msgbox("Backup complete!", ok_button="Good job!")

Here are a couple of examples::

    easygui.msgbox("Hello, world!")

.. image:: _static/tutorial/screenshot_msgbox.png
   :align: center

ccbox()
^^^^^^^
The ``ccbox()`` function offers a choice of Continue and Cancel, and returns either True (for continue) or False (for cancel).

::

    import easygui
    msg = "Do you want to continue?"
    title = "Please Confirm"
    if easygui.ccbox(msg, title):  # Show a Continue/Cancel dialog.
        pass  # User chose Continue.
    else:  # User chose Cancel.
        sys.exit()

.. image:: _static/tutorial//screenshot_ccbox.png
   :align: center

ynbox()
^^^^^^^
The ``ynbox()`` offers a choice of Yes and No, and returns either ``True`` of ``False``.

::

    import easygui
    result = easygui.ynbox('Is a hot dog a sandwich?', 'Hot Dog Question')
    if result == True:
        easygui.msgbox('That is an interesting answer.')
    else:
        easygui.msgbox('Well, that is your opinion.')

buttonbox()
^^^^^^^^^^^
The ``buttonbox()`` function displays a set of buttons, and returns the text of the selected button.

::

    import easygui
    result = easygui.buttonbox('Which door do you choose?', 'Win Prizes!', choices=['Door 1', 'Door 2', 'Door 3'])
    if result == 'Door 3':
        easygui.msgbox('You win a new car!')
    else:
        easygui.msgbox('Better luck next time.')


indexbox()
^^^^^^^^^^
The ``indexbox()`` function displays a set of buttons, and returns the index of the selected button. For example, if you invoked index box with three choices (A, B, C), indexbox would return 0 if the user picked A, 1 if he picked B, and 2 if he picked C.

::

    import easygui
    result = easygui.indexbox('Which door do you choose?', 'Win Prizes!', choices=['Door 1', 'Door 2', 'Door 3'])
    if result == 2:
        easygui.msgbox('You win a new car!')
    else:
        easygui.msgbox('Better luck next time.')


boolbox()
^^^^^^^^^
The ``boolbox()`` (boolean box) displays two buttons. Returns returns ``True`` if the first button is chosen. Otherwise returns ``False``.

::

    import easygui
    message = "What do they say?"
    title = "Romantic Question"
    if easygui.boolbox(message, title, ["They love me", "They love me not"]):
        easygui.msgbox('You should send them flowers.')
    else:
        easygui.msgbox('It was not meant to be.')

How to Show an Image in a buttonbox
-----------------------------------
When you invoke the ``buttonbox()`` function (or other functions that display a button box, such as ``msgbox()``, ``indexbox()``, ``ynbox()``, etc.), you can specify the keyword argument ``image='image_file.gif'`` to display that image in the dialog box.

.. note::
  The types of files supported depends on how you installed python.  If other formats don't work, you may need to install the PIL library.

If an image argument is specified, the image file will be displayed after the message.

Here is some sample code from EasyGUI's demonstration routine::

    import easygui
    image = "python_and_check_logo.gif"
    msg = "Do you like this picture?"
    choices = ["Yes", "No", "No opinion"]
    reply = easygui.buttonbox(msg, image=image, choices=choices)

If you click on one of the buttons on the bottom, its value will be returned in ``reply``.  You may also click on the image.
In that case, the image filename is returned.

.. image:: _static/tutorial/screenshot_buttonbox_with_image.png
   :align: center

Letting the user select from a list of choices
----------------------------------------------
choicebox()
^^^^^^^^^^^

Buttonboxes are good for presenting a small number of choices, but if there are many choices, it's better to present them as a list. The ``choicebox()`` provides a list of choices in a list box to choose from. The choices are specified in a sequence (a tuple or a list).

The keyboard can be used to select an element of the list.

Pressing "g" on the keyboard, for example, will jump the selection to the first element beginning with "g". Pressing "g" again, will jump the cursor to the next element beginning with "g". At the end of the elements beginning with "g", pressing "g" again will cause the selection to wrap around to the beginning of the list and jump to the first element beginning with "g".

If there is no element beginning with "g", then the last element that occurs before the position where "g" would occur is selected. If there is no element before "g", then the first element in the list is selected::

    import easygui
    msg ="What is your favorite flavor?"
    title = "Ice Cream Survey"
    choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
    choice = easygui.choicebox(msg, title, choices)  # choice is a string

.. image:: _static/tutorial/screenshot_choicebox_icecream.png
   :align: center

Another example of a choicebox:

.. image:: _static/tutorial/screenshot_choicebox.png
   :align: center

multchoicebox()
^^^^^^^^^^^^^^^
The ``multchoicebox()`` function provides a way for a user to select from a list of choices. The interface looks just like the ``choicebox()`` function's dialog box, but the user may select zero, one, or multiple choices.

The choices are specified in a sequence (a tuple or a list).

::

    import easygui
    msg ="What is your favorite flavor?"
    title = "Ice Cream Survey"
    choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
    choice = easygui.multchoicebox(msg, title, choices)

.. image:: _static/tutorial//screenshot_multchoicebox.png
   :align: center

Letting the User Enter Information
----------------------------------
enterbox()
^^^^^^^^^^
The ``enterbox()`` function lets the user enter a string into a text field, which is returned.

integerbox()
^^^^^^^^^^^^
The ``integerbox()`` function lets the user enter an integer into a text field, which is returned. (Non-integers cause an error box to appear.)

multenterbox()
^^^^^^^^^^^^^^
The ``multenterbox()`` displays a dialog box with labeled text fields for the user to enter replies, which are returned as a list of strings.

.. image:: _static/tutorial//screenshot_multenterbox_vista.png
   :align: center

In the dialog box:

  - If there are fewer values than names, the list of values is padded with empty strings until the number of values is the same as the number of names.

  - If there are more values than names, the list of values is truncated so that there are as many values as names.

Returns a list of the values of the fields, or None if the user cancels the operation.

Here is some example code, that shows how values returned from multenterbox can be checked for validity before they are accepted::

    from __future__ import print_function
    msg = "Enter your personal information"
    title = "Credit Card Application"
    fieldNames = ["Name", "Street Address", "City", "State", "ZipCode"]
    fieldValues = multenterbox(msg, title, fieldNames)
    if fieldValues is None:
        sys.exit(0)
    # make sure that none of the fields were left blank
    while 1:
        errmsg = ""
        for i, name in enumerate(fieldNames):
            if fieldValues[i].strip() == "":
              errmsg += "{} is a required field.\n\n".format(name)
        if errmsg == "":
            break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
        if fieldValues is None:
            break
    print("Reply was:{}".format(fieldValues))

.. note::
  The first line 'from __future__' is only necessary if you are using Python 2.*, and is only needed for this demo.

Letting the user enter password information
-------------------------------------------
passwordbox()
^^^^^^^^^^^^^
The ``passwordbox()`` function's dialog box is like a ``enterbox()``, but used for entering passwords. The text is masked as it is typed in.

multpasswordbox
^^^^^^^^^^^^^^^
The ``multpasswordbox()`` function has the same interface as ``multenterbox()``, but the last of the fields is assumed to be a password and is masked with asterisks. This is ideal for username/password dialog boxes.

.. image:: _static/tutorial/screenshot_passwordbox.png
   :align: center

Displaying text
---------------
EasyGUI provides functions for displaying text.

textbox()
^^^^^^^^^
The ``textbox()`` function displays a large text field in a proportional font. The text will word-wrap.

codebox()
^^^^^^^^^
The ``codebox()`` function displays a large text field in a monospaced font and does not wrap.

.. image:: _static/tutorial/screenshot_codebox_vista.png
   :align: center

Note that you can pass ``codebox()`` and ``textbox()`` either a string or a list of strings. A list of strings will be converted to text before being displayed. This means that you can use these functions to display the contents of a file this way::

    import os
    filename = os.path.normcase("c:/autoexec.bat")
    f = open(filename, "r")
    text = f.readlines()
    f.close()
    codebox("Contents of file " + filename, "Show File Contents", text)

Working with files
------------------
A common need is to ask the user for a filename or for a directory. EasyGUI provides a few basic functions for allowing a user to navigate through the file system and choose a directory or a file. (These functions are wrappers around widgets and classes in lib-tk.)

Note that in the current version of EasyGUI, the startpos argument is not supported.

diropenbox()
^^^^^^^^^^^
The ``diropenbox()`` function displays a dialog box that lets the user select a folder/directory and returns the name of the selected directory.

fileopenbox()
^^^^^^^^^^^^^
The ``fileopenbox()`` function displays a dialog box that lets the user select a file and returns the path and name of the selected file.

.. image:: _static/tutorial/screenshot_fileopenbox_vista.png
   :align: center

filesavebox()
^^^^^^^^^^^^^
The ``filesavebox()`` function displays a dialog box that lets the user select a filename, and returns the path and name selected.

Remembering User Settings
-------------------------

EgStore
^^^^^^^
A common need is to ask the user for some setting, and then to "persist it", or store it on disk, so that the next time the user uses your application, you can remember his previous setting.

In order to make the process of storing and restoring user settings, EasyGUI provides a class called EgStore. In order to remember some settings, your application must define a class (let's call it Settings, although you can call it anything you want) that inherits from EgStore.

Your application must also create an object of that class (let's call the object settings).

The constructor (the ``__init__()`` method) of the Settings class can initialize all of the values that you wish to remember.

Once you have done this, you can remember the settings simply by assigning values to instance variables in the settings object, and use the settings.store() method to persist the settings object to disk.

Here is an example of code using the Settings class::

    from easygui import EgStore

    # -----------------------------------------------------------------------
    # define a class named Settings as a subclass of EgStore
    # -----------------------------------------------------------------------
    class Settings(EgStore):

        def __init__(self, filename):  # filename is required
            # -------------------------------------------------
            # Specify default/initial values for variables that
            # this particular application wants to remember.
            # -------------------------------------------------
            self.userId = ""
            self.targetServer = ""

            # -------------------------------------------------
            # For subclasses of EgStore, these must be
            # the last two statements in  __init__
            # -------------------------------------------------
            self.filename = filename  # this is required
            self.restore()

    # Create the settings object.
    # If the settingsFile exists, this will restore its values
    # from the settingsFile.
    # create "settings", a persistent Settings object
    # Note that the "filename" argument is required.
    # The directory for the persistent file must already exist.

    settingsFilename = "settings.txt"
    settings = Settings(settingsFilename)

    # Now use the settings object.
    # Initialize the "user" and "server" variables
    # In a real application, we'd probably have the user enter them via enterbox
    user    = "obama_barak"
    server  = "whitehouse1"

    # Save the variables as attributes of the "settings" object
    settings.userId = user
    settings.targetServer = server
    settings.store()    # persist the settings
    print("\nInitial settings")
    print settings

    # Run code that gets a new value for userId
    # then persist the settings with the new value
    user    = "biden_joe"
    settings.userId = user
    settings.store()
    print("\nSettings after modification")
    print settings

    # Delete setting variable
    del settings.userId
    print("\nSettings after deletion of userId")
    print settings

Here is an example of code using a dedicated function to create the Settings class::

    from easygui import read_or_create_settings

    # Create the settings object.
    settings = read_or_create_settings('settings1.txt')

    # Save the variables as attributes of the "settings" object
    settings.userId = "obama_barak"
    settings.targetServer = "whitehouse1"
    settings.store()    # persist the settings
    print("\nInitial settings")
    print settings

    # Run code that gets a new value for userId
    # then persist the settings with the new value
    user    = "biden_joe"
    settings.userId = user
    settings.store()
    print("\nSettings after modification")
    print settings

    # Delete setting variable
    del settings.userId
    print("\nSettings after deletion of userId")
    print settings



Trapping Exceptions
-------------------
exceptionbox()
^^^^^^^^^^^^^^
EasyGUI provides a way to display exception tracebacks in a GUI via ``exceptionbox()``. The ``exceptionbox()`` function displays the stack trace in a ``codebox()``.

Here is a code example::

    import easygui
    try:
        1 / 0   # This raises a zero divide exception.
    except:
        easygui.exceptionbox()

.. image:: _static/tutorial/screenshot_exceptionbox_vista.png
   :align: center
