.. easygui documentation master file, created by
   sphinx-quickstart on Wed Nov 19 17:44:42 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EasyGUI
=======

EasyGUI is a module for very simple, very easy GUI programming in Python. EasyGUI is different from other GUI generators in that EasyGUI is NOT event-driven. Instead, all GUI interactions are invoked by simple function calls.

EasyGUI runs on Python 2 and 3, and does not have any dependencies.

Example Usage
-------------

    >>> import easygui
    >>> easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
    1
    >>> easygui.msgbox('This is a basic message box.', 'Title Goes Here')
    'OK'
    >>> easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
    'Chocolate'


.. toctree::

   Support, Contacts <support>
   API <api>
   Tutorial <tutorial>
   FAQ <faq>
   Cookbook <cookbook>
   Great Links <links>

* :ref:`genindex`
* :ref:`search`

**Background**

easygui was started several years ago by Stephen Ferg <http://www.ferg.org/contact_info/index.html> and was developed and supported by him through 2013.  From there, work was restarted circa 2014.  The first goal was to update the then four year old release and address some bugs and minor enhancements.  That first release will be/was 0.97.

__ display the about and license at top of file only



