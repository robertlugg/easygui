
import collections
import re


class Choices(object):
    def __init__(self, input_choices, default_choice, cancel_choice, notification):
        """
        Choices is an abstract data class thar represents the choices the user can
        exert pushing the different buttons.
        Choices must have an order, (or else we will order them) that reflect in the order of buttons
        Also there can be a default choice, and a hotkey for any choice
        There also can be a choice that means that the procedure has to be canceled and the window closed
        The user can enter choices as a single string, a list of strings and a dictionary
        so first we transform them all into this ADC
        """
        self.description_of_problem = ''
        # First we transform input data into an ordered dictionary
        dict_choices = self.input_choices_to_dict(input_choices)
        dict_choices['No choice'] = None

        # Then into a dictionary of objects of the Choice type
        self.choices = self.dict_2_abstract_data_class(dict_choices)

        unique_choices = self.uniquify_list_of_strings(list(self.choices.keys()))

        for uc, choice in zip(unique_choices, self.choices.values()):
            choice.unique_text = uc

        if default_choice in self.choices:
            self.choices[default_choice].default = True
        else:
            notification.add_error("\nWARNING: Default choice <{}> is not part of choices".format(default_choice))

        if cancel_choice:
            if cancel_choice in self.choices:
                self.choices[cancel_choice].is_cancel = True
            else:
                notification.add_error("\nWARNING: Cancel choice <{}> is not part of choices".format(cancel_choice))

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

    def __iter__(self):
        return iter(self.choices.values())

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
                    choice_as_string = str(choice)
                    choices_dict[choice_as_string] = choice
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
        self.lowercase_hotkey = self.find_lowercase_hotkey(self.hotkey)
        self.default = False
        self.is_cancel = False

    def find_lowercase_hotkey(self, hotkey):
        """ if the hotkey is a single char and uppercase, return its lowercase version, if not, return None"""
        if not hotkey:
            return
        if len(hotkey) > 1:
            return None
        if hotkey.isupper():
            return hotkey.lower()
        return None

    def parse_hotkey(self, original_text):
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

        :param original_text: string
        :return: caption: string without the braces and the hidden text
                 hotkey: a string with the letter or number or keysym
                 position: int The position of the hotkey (for the underscore) inside the caption.

        """
        caption = original_text
        hotkey = None
        position = None

        if original_text is None:
            return caption, hotkey, position

        # Single character, hide it
        res = re.search('(?<=\[\[).(?=\]\])', original_text)
        if res:
            start = res.start(0)
            end = res.end(0)
            caption = original_text[:start - 2] + original_text[end + 2:]
            hotkey = original_text[start:end]
            position = None
            return caption, hotkey, position

        # Single character, remain visible
        res = re.search('(?<=\[).(?=\])', original_text)
        if res:
            start = res.start(0)
            end = res.end(0)
            caption = original_text[:start - 1] + original_text[start:end] + original_text[end + 1:]
            hotkey = original_text[start:end]
            position = start - 1
            return caption, hotkey, position

        # a Keysym.  Always hide it
        res = re.search('(?<=\[\<).+(?=\>\])', original_text)
        if res:
            start = res.start(0)
            end = res.end(0)
            caption = original_text[:start - 2] + original_text[end + 2:]
            hotkey = '<{}>'.format(original_text[start:end])
            position = None
            return caption, hotkey, position

        return caption, hotkey, position
