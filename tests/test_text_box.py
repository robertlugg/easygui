import tkinter as tk
import unittest
from tkinter import font

from mock import patch, Mock, ANY

from easygui.text_box import TextBox, textbox, codebox
from tests import WAIT_0_MILLISECONDS, WAIT_1_MILLISECONDS

MODBASE = 'easygui.text_box'

TEST_MESSAGE = 'example message'
TEST_TITLE = 'example title'
TEST_TEXT = 'example text'
TEST_MONOSPACE = False
TEST_CALLBACK = Mock()
TEST_ARGS = [TEST_MESSAGE, TEST_TITLE, TEST_TEXT, TEST_MONOSPACE, TEST_CALLBACK]


def test__textbox_method__instantiates_textbox_class_and_runs_it():
    """ Test that the textbox() method calls the underlying TextBox class in the expected way """
    with patch(MODBASE + '.TextBox') as mock_text_box_class:
        mock_text_box_instance = Mock()
        mock_text_box_instance.run = Mock(return_value='return text')
        mock_text_box_class.return_value = mock_text_box_instance

        return_text = textbox(TEST_MESSAGE, TEST_TITLE, TEST_TEXT, TEST_CALLBACK, run=True)

        mock_text_box_class.assert_called_once_with(
            msg=TEST_MESSAGE,
            title=TEST_TITLE,
            text=TEST_TEXT,
            monospace=TEST_MONOSPACE,
            callback=TEST_CALLBACK
        )
        mock_text_box_instance.run.assert_called_once_with()
        assert return_text == 'return text'


class TestTextBox(unittest.TestCase):
    def setUp(self):
        self.tb = TextBox(*TEST_ARGS)

    def test_instantiation(self):
        # Instance attributes should be configured:
        self.assertEqual(self.tb.text, TEST_TEXT)
        self.assertEqual(self.tb.msg.strip(), TEST_MESSAGE)
        self.assertEqual(self.tb._user_specified_callback, TEST_CALLBACK)

        # The following Tk widgets should also have been created:
        isinstance(self.tb.box_root, tk.Tk)
        isinstance(self.tb.msg_widget, tk.Tk)
        isinstance(self.tb.text_area, tk.Tk)

        # And configured:
        self.assertEqual(self.tb.msg_widget.get(0.0, 'end-1c'), TEST_MESSAGE)
        self.assertEqual(self.tb.text_area.get(0.0, 'end-1c'), TEST_TEXT)

    def test_run(self):
        self.tb.box_root = Mock()
        return_value = self.tb.run()
        self.assertEqual(return_value, None  )
        self.tb.box_root.mainloop.assert_called_once_with()
        self.tb.box_root.destroy.assert_called_once_with()

    def test_stop(self):
        self.tb.box_root = Mock()
        self.tb.stop()
        self.tb.box_root.quit.assert_called_once_with()

    def test_set_msg_area(self):
        new_msg = 'some new text'
        self.tb.msg = new_msg
        self.assertEqual(self.tb.msg_widget.get(1.0, 'end-1c'), new_msg)

    def test_get_text(self):
        actual = self.tb.text
        self.assertEqual(actual, TEST_TEXT)

    def test_set_text(self):
        new_text = 'some new text'
        self.tb.text = new_text
        self.assertEqual(self.tb.text_area.get(1.0, 'end-1c'), new_text)


class TestTextBoxIntegration(unittest.TestCase):

    def test_textbox_cancel_button_pressed_results_in_run_returning_None(self):
        tb = textbox(run=False)

        def simulate_cancel_button_pressed(tb_instance):
            tb_instance.cancel_button_pressed('ignored button handler arg')

        tb.box_root.after(WAIT_0_MILLISECONDS, simulate_cancel_button_pressed, tb)
        actual = tb.run()

        self.assertEqual(actual, None)

    def test_textbox_ok_pressed_calls_user_defined_callback(self):
        tb = textbox(text=TEST_TEXT, callback=TEST_CALLBACK, run=False)

        def simulate_ok_button_pressed(tb_instance):
            tb_instance.ok_button_pressed('ignored button handler arg')

        def stop_running(tb_instance):
            tb_instance.stop()

        tb.box_root.after(WAIT_0_MILLISECONDS, simulate_ok_button_pressed, tb)
        tb.box_root.after(WAIT_1_MILLISECONDS, stop_running, tb)
        actual = tb.run()

        TEST_CALLBACK.assert_called_once_with(ANY)
        self.assertEqual(actual, TEST_TEXT)

    def test_textbox_ok_pressed_with_no_user_defined_callback(self):
        tb = textbox(msg=TEST_MESSAGE, title=TEST_TITLE, text=TEST_TEXT, run=False)

        def simulate_ok_button_pressed(tb_instance):
            tb_instance.ok_button_pressed('ignored button handler arg')

        tb.box_root.after(WAIT_0_MILLISECONDS, simulate_ok_button_pressed, tb)
        actual = tb.run()

        # tb.stop() happens because no user _user_specified_callback is set
        # the initial text value is unchanged, and is returned from run()
        self.assertEqual(actual, TEST_TEXT)


class TestTextBoxCodeBox(unittest.TestCase):

    def test_instantiation_codebox(self):
        cb = codebox(msg=TEST_MESSAGE, title=TEST_TITLE, text=TEST_TEXT * 100, callback=TEST_CALLBACK, run=False)

        # cget returns strings so the monospace assertion is a bit messy:
        self.assertEqual(cb.text_area.cget('font'), "font1")  # a monospace font
