EasyGUI FAQ
===========

.. toctree::
   :maxdepth: 4

An FAQ consisting of far too few questions.  Help please :)
-----------------------------------------------------------

General Questions
^^^^^^^^^^^^^^^^^
#. What other GUI libraries can I use?

   TkInter is a library shipped with Python and it is the de-facto standard
   for Python. You can find more about it at https://wiki.python.org/moin/TkInter

   PyQt is available at https://wiki.python.org/moin/PyQt

   wxPython is available at https://www.wxpython.org/

   A library inspired by easygui is the EasyGUI_qt project at http://easygui-qt.readthedocs.org/en/latest/
   "Under the hood" EasyGUI uses Tkinter while EasyGUI_qt uses pyQt

#. Why should I use EasyGUI instead of some other library?

   Well, sometimes you should start with those other (excellent) libraries.
   However, we hope that you find EasyGUI useful.  Some of the cases for using
   EasyGUI are:

   - You are starting to program and are tired of the command line >>>.
     easygui allows you to quickly create GUIs without worrying about all
     the details of Tk or Qt.
   - You already have a program and want to make it easier for people to use
     by building a GUI for it.
   - Its easy!  You can try it out in a couple of hours and decide for yourself

   Don't worry.  With easygui you are learning the basics.  We take only a
   few shortcuts to make things easier.  If you decide to move to a library
   with more functionality, you will already understand some of the
   GUI basics.

Specifics
^^^^^^^^^
#. Button box images don't appear and I get an error such as:

      Cannot load C:\Users\Robert\SkyDrive\GitHub\easygui\easygui\python_and_check_logo.jpg.
      Check to make sure it is an image file.
      PIL library isn't installed.  If it isn't installed, only .gif files can be used.

   Possibly you are trying to load files other than .gif.  Unfortunately, the 'PIL' library must be installed
   for this to work.