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


A full tutorial is available at
<http://easygui.sourceforge.net/tutorial/>.