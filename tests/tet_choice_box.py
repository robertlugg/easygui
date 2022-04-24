import unittest

from mock import patch, Mock

from easygui.choice_box import choicebox, multchoicebox

MODBASE = 'easygui.choice_box'

TEST_MESSAGE = 'example message'
TEST_TITLE = 'example title'
TEST_CHOICES = ['choice 1', 'choice 2']
TEST_PRESELECT = []
TEST_CALLBACK = Mock()

TEST_RETURN_TEXT = 'return text'


@patch(MODBASE + '.ChoiceBox')
class TestChoiceBoxUtilities(unittest.TestCase):
    def configureMocks(self, mock_choicebox_class):
        self.mock_choicebox_instance = Mock()
        self.mock_choicebox_instance.run = Mock(return_value=TEST_RETURN_TEXT)
        mock_choicebox_class.return_value = self.mock_choicebox_instance

    def test_choicebox_method_instantiates_choicebox_class_correctly_and_runs_it(self, mock_choicebox_class):
        self.configureMocks(mock_choicebox_class)

        return_text = choicebox(msg=TEST_MESSAGE, title=TEST_TITLE, choices=TEST_CHOICES, preselect=TEST_PRESELECT,
                                callback=TEST_CALLBACK, run=True)

        self.assertEqual(return_text, TEST_RETURN_TEXT)
        mock_choicebox_class.assert_called_once_with(
            TEST_MESSAGE,
            TEST_TITLE,
            TEST_CHOICES,
            preselect=TEST_PRESELECT,
            multiple_select=False,  # this is the only difference between choicebox() and multchoicebox()
            callback=TEST_CALLBACK
        )
        self.mock_choicebox_instance.run.assert_called_once_with()

    def test_multchoicebox_method_instantiates_choicebox_class_correctly_and_runs_it(self, mock_choicebox_class):
        self.configureMocks(mock_choicebox_class)

        return_text = multchoicebox(msg=TEST_MESSAGE, title=TEST_TITLE, choices=TEST_CHOICES, preselect=TEST_PRESELECT,
                                    callback=TEST_CALLBACK, run=True)

        self.assertEqual(return_text, TEST_RETURN_TEXT)
        mock_choicebox_class.assert_called_once_with(
            TEST_MESSAGE,
            TEST_TITLE,
            TEST_CHOICES,
            preselect=TEST_PRESELECT,
            multiple_select=True,  # this is the only difference between choicebox() and multchoicebox()
            callback=TEST_CALLBACK
        )
        self.mock_choicebox_instance.run.assert_called_once_with()
