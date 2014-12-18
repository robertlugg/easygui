Cookbook
========

.. toctree::
   :maxdepth: 4

A section to hold code snippets and recipes
-------------------------------------------

#. Simple demo program

   Here is a simple demo program using easygui. The screens that it
   produces are shown on the easygui home page.

   .. doctest::

      from easygui import *
      import sys

      while 1:
          msgbox("Hello, world!")

          msg ="What is your favorite flavor?"
          title = "Ice Cream Survey"
          choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
          choice = choicebox(msg, title, choices)

          # note that we convert choice to string, in case
          # the user cancelled the choice, and we got None.
          msgbox("You chose: " + str(choice), "Survey Result")

          msg = "Do you want to continue?"
          title = "Please Confirm"
          if ccbox(msg, title):     # show a Continue/Cancel dialog
              pass  # user chose Continue
          else:
              sys.exit(0)           # user chose Cancel

              
#. Controlling the order of items in choicebox

   In a choicebox, the choices must be in sort order so that the keyboard
   "jump to" feature (jump down in the list by pressing keyboard keys) will work.
   But it often happens that a sort of first-cut listing of choices doesn't sort
   in a user-friendly order. So what can you do to control the order of the items
   displayed in a choicebox?

   A useful technique is to specify keys for the items in the choicebox.
   For example, suppose you want a choicebox to display View, Update, Delete, Exit.
   If you specified your choices this way::

       choices = ["View", "Update", "Delete", "Exit"]

   you'd get this:

   - Delete
   - Exit
   - Update
   - View

   It is definitely in alphabetic order, but not very user-friendly.
   But if you specified keys for your choices this way::

       choices = ["V View", "U Update", "D elete", "X Exit"]

   you'd get this (with "X" appearing at the bottom):

   - D Delete
   - U Update
   - V View
   - X Exit

   Suppose you wanted to force View to the top, so it is the easiest choice to select.
   You could change its key from "V" to "A"::

       choices = ["A View", "U Update", "D elete", "X Exit"]

   and you'd get this:

   - A View
   - D Delete
   - U Update
   - X Exit
     
   Another technique is to prepend a space to the choice.
   Since space characters always sorts before a non-space character,
   you can use this trick to force something like "V  View" to the top of the list::

       choices = [" V View", "U Update", "D Delete", "X Exit"]

   produces this:

   - V View
   - D Delete
   - U Update
   - X Exit

   In the proportional font used by choicebox, the space before the "V" is almost imperceptible.

   Personally, I prefer to use alphabetic keys rather than numeric keys for choicebox items.
   It is easier to navigate the choices using alpha keys on the keyboard than by using
   the number keys.

   And it is possible to use multi-character keys, like this:

   - L1  Log old version
   - L2  Log new version

   Using keys for choices also makes it relatively easy to check for the user's selection::

       choices = [" V View", "U Update", "D elete", "X Exit"]
       choice = choicebox(msg,title,choices)

       if choice == None:
           return
       reply = choice.split()[0] # reply = the first word of the choice

       if reply == "X":
           return
       elif reply == "V":
           processView()
       elif reply == "L1":
           saveLog(version="old")
       elif reply == "L2":
           saveLog(version="new")

#. Registration System demo

   The Registration System demo application is a simple database application to maintain
   a list of courses, and students who are registered for the courses.

   It is not completely implemented -- its purpose is to give you a feel for what is possible
   with EasyGui and how you might do it, not to be a complete working application.

   File:  :download:`registration zip file <_static/registration_system/easygui_demo_registration_app.zip>`

   Screenshots:

   .. image:: _static/registration_system/screenshot_register_main.png
      :align: center


   .. image:: _static/registration_system/screenshot_register_show.png
      :align: center

