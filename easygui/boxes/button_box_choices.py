

try:
    from . import utils as ut
except (SystemError, ValueError, ImportError):
    import utils as ut

import collections


class Choices(object):
    def __init__(self, input_choices, default_choice):
        """
        User can enter choices as a single string, a list of strings and a dictionary
        Here we transform them all into a dicrionary
        """
        choices_dict = self.input_choices_to_dict(input_choices)
        self.choices = self.dict_2_abstract_data_class(choices_dict)
        self.selected_choice = None

        unique_choices = ut.uniquify_list_of_strings(self.choices.keys())

        for uc, choice in zip(unique_choices, self.choices.values()):
            choice.unique_text = uc

        if default_choice in self.choices:
            self.default_choice =self.choices[default_choice]



    def input_choices_to_dict(self, choices):
        if isinstance(choices, collections.Mapping):  # If it is dictionary-like
            choices_dict = choices
        else:
            try:
                # Try to convert to OrderedDict, it will succeed if it is a list of lists or list or tuples...
                # http://stackoverflow.com/questions/25480089/initializing-an-ordereddict-using-its-constructor
                choices_dict = collections.OrderedDict(choices)
            except:
                # Convert into a dictionary of equal key and values
                choices_list = list(choices)
                choices_dict = collections.OrderedDict()
                for choice in choices_list:
                    choices_dict[choice] = choice
        return choices_dict

    def dict_2_abstract_data_class(self, choices_dict):
        choices = collections.OrderedDict()
        for text, result in choices_dict.items():
            choices[text] = Choice(text, result)
        return choices


    def select_choice(self, choice):
        try:
            self.selected_choice = self.choices[choice].result
        except:
            self.selected_choice = None


class Choice(object):
    def __init__(self, text, result):
        self.original_text = text
        self.result = result
        self.clean_text, self.hotkey, self.hotkey_position = ut.parse_hotkey(self.original_text)
        self.default = False

