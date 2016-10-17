

import collections
import re


class Choices(object):
    def __init__(self, input_choices, default_choice, cancel_choice):
        """
        User can enter choices as a single string, a list of strings and a dictionary
        Here we transform them all into a dicrionary
        """
        dict_choices = self.input_choices_to_dict(input_choices)
        dict_choices['No choice'] = None
        self.choices = self.dict_2_abstract_data_class(dict_choices)

        unique_choices = self.uniquify_list_of_strings(list(self.choices.keys()))

        for uc, choice in zip(unique_choices, self.choices.values()):
            choice.unique_text = uc

        if default_choice in self.choices:
            self.choices[default_choice].default = True

        if cancel_choice:
            if cancel_choice in self.choices:
                self.choices[cancel_choice].is_cancel = True
            else:
                err_msg = "Cancel choice <{}> is not part of choices".format(cancel_choice)
                raise ValueError(err_msg)

        self.selected_choice = self.choices['No choice']

    def unselect_choice(self):
        self.selected_choice = self.choices['No choice']

    def select_choice_from_hotkey(self, hotkey):
        success = False
        for choice in self.choices.values():
            if choice.hotkey == hotkey:
                self.selected_choice = choice
                success = True
        return success

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.
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

    def uniquify_list_of_strings(self, input_list):
        """
        Ensure that every string within input_list is unique.
        :param list input_list: List of strings
        :return: New list with unique names as needed.
        """
        output_list = list()
        for i, item in enumerate(input_list):
            tempList = input_list[:i] + input_list[i + 1:]
            if item not in tempList:
                output_list.append(item)
            else:
                output_list.append('{0}_{1}'.format(item, i))
        return output_list

    def __repr__(self):
        return repr(self.choices)


class Choice(object):
    def __init__(self, text, result):
        self.original_text = text
        self.result = result
        self.clean_text, self.hotkey, self.hotkey_position = self.parse_hotkey(self.original_text)
        self.default = False
        self.is_cancel = False

    def parse_hotkey(self, text):
        """
        Extract a desired hotkey from the text.

        The format to enclose the hotkey in square braces as in Button_[1]
        which would extract the keyboard key 1 for that button.
        The 1 will be included in the button text, without the braces

        To hide they key, use double square braces as in:  Ex[[qq]]
        which would assign the q key to the Exit button.

        Special keys such as <Enter> may also be used:  Move [<left>]
        for a full list of special keys, see this reference:
        http://infohoglobal_state.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html

        :param text: string
        :return: caption: string without the braces and the hidden text
                 hotkey: a string with the letter or number or keysym
                 position: int The position of the hotkey (for the underscore) inside the caption.

        """
        caption = text
        hotkey = None
        position = None

        if text is None:
            return caption, hotkey, position

        # Single character, hide it
        res = re.search('(?<=\[\[).(?=\]\])', text)
        if res:
            start = res.start(0)
            end = res.end(0)
            caption = text[:start - 2] + text[end + 2:]
            hotkey = text[start:end]
            position = None
            return caption, hotkey, position

        # Single character, remain visible
        res = re.search('(?<=\[).(?=\])', text)
        if res:
            start = res.start(0)
            end = res.end(0)
            caption = text[:start - 1] + text[start:end] + text[end + 1:]
            hotkey = text[start:end]
            position = start - 1
            return caption, hotkey, position

        # a Keysym.  Always hide it
        res = re.search('(?<=\[\<).+(?=\>\])', text)
        if res:
            start = res.start(0)
            end = res.end(0)
            caption = text[:start - 2] + text[end + 2:]
            hotkey = '<{}>'.format(text[start:end])
            position = None
            return caption, hotkey, position

        return caption, hotkey, position
