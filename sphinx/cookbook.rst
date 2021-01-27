Cookbook
========

.. toctree::
   :maxdepth: 4

A section to hold code snippets and recipes
-------------------------------------------

#. Simple demo program

   Here is a simple demo program using EasyGUI. The screens that it
   produces are shown on the EasyGUI home page.

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


#. Registration System demo

   The Registration System demo application is a simple database application to maintain
   a list of courses, and students who are registered for the courses.

   It is not completely implemented -- its purpose is to give you a feel for what is possible
   with EasyGUI and how you might do it, not to be a complete working application.

   File:  :download:`registration zip file <_static/registration_system/easygui_demo_registration_app.zip>`

   Screenshots:

   .. image:: _static/registration_system/screenshot_register_main.png
      :align: center


   .. image:: _static/registration_system/screenshot_register_show.png
      :align: center

