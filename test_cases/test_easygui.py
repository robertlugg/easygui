import sys
sys.path.append('..')
import easygui

import inspect
import os
import time
import threading

import pytest
from pynput.keyboard import Key, Controller

KEYBOARD = Controller()
FOLDER_OF_THIS_FILE = os.path.dirname(os.path.abspath(__file__))
GUI_WAIT = 0.2 # if tests start failing, maybe try bumping this up a bit (though that'll slow the tests down)


"""
NOTE: You will often see this code in this test:

    print('Line', inspect.currentframe().f_lineno);

This is because due to the GUI nature of these tests, if something messes up
and PyAutoGUI is unable to click on the message box, this program will get
held up. By printing out the line number, you will at least be able to see
which line displayed the message box that is held up.

This is a bit unorthodox, and I'm welcome to other suggestions about how to
deal with this possible scenario.
"""

class KeyPresses(threading.Thread):
    def __init__(self, keyPresses):
        super(KeyPresses, self).__init__()
        self.keyPresses = keyPresses

    def run(self):
        time.sleep(GUI_WAIT)
        KEYBOARD.type(self.keyPresses)


def test_test_images_exist():
    assert os.path.exists(os.path.join(FOLDER_OF_THIS_FILE, 'pi.jpg'))
    assert os.path.exists(os.path.join(FOLDER_OF_THIS_FILE, 'result.png'))

def test_msgbox():
    # Test hitting space to click OK.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox() == 'OK'

    # Test hitting Esc to close.
    t = KeyPresses([Key.esc])
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox() is None

    # Test with custom message.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox('Message') == 'OK'

    # Test with custom message and title.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox('Message', 'Title') == 'OK'

    # Test with custom OK button text.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox(ok_button='Button') == 'Button'

    # Test with custom message, title, and OK button text.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox('Message', 'Title', ok_button='Button') == 'Button'

    # Test with jpg image.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox(image=os.path.join(FOLDER_OF_THIS_FILE, 'pi.jpg')) == 'OK'

    # Test with png image.
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.msgbox(image=os.path.join(FOLDER_OF_THIS_FILE, 'result.png')) == 'OK'

def test_buttonbox():
    # Test hitting space to click OK with different default buttons:
    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.buttonbox('Message', 'Title', choices=('Button[1]', 'Button[2]', 'Button[3]'), default_choice='Button[1]') == 'Button[1]'

    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.buttonbox('Message', 'Title', choices=('Button[1]', 'Button[2]', 'Button[3]'), default_choice='Button[2]') == 'Button[2]'

    t = KeyPresses(' ')
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.buttonbox('Message', 'Title', choices=('Button[1]', 'Button[2]', 'Button[3]'), default_choice='Button[3]') == 'Button[3]'

    # Test hitting Esc to close.
    # TODO: If button boxes aren't given a default choice, then their window won't be in focus and this test hangs.
    #t = KeyPresses([Key.esc])
    #t.start()
    #print('Line', inspect.currentframe().f_lineno)
    #assert easygui.buttonbox() is None

    # Test hitting Esc to close.
    t = KeyPresses([Key.esc])
    t.start()
    print('Line', inspect.currentframe().f_lineno)
    assert easygui.buttonbox(default_choice='Button[1]') is None

