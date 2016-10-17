

class BoxController(object):

    def __init__(self, model):
        """
        :param object model: holds the data of this call
        :param function callback: if set, this function will be called when any button is pressed.
        """
        self.model = model

    # Methods executing when a key is pressed -------------------------------
    # If cancel, x, or escape, close ui and return None
    def x_pressed(self):
        self.nothing_selected_and_stop()

    def escape_pressed(self, event):
        self.nothing_selected_and_stop()

    def button_or_hotkey_pressed(self, choice):
        # If cancel
        if choice.is_cancel:
            self.nothing_selected_and_stop()
        else:
            # So there has been a choice selected
            self.model.choices.selected_choice = choice
            self.model.check_callback_updated()

    def image_pressed(self, filename, row, column):
        self.model.choices.unselect_choice()
        self.model.row_column_selected = (row, column)
        self.model.check_callback_updated()

    def nothing_selected_and_stop(self):
        self.model.choices.unselect_choice()
        self.model.row_column_selected = None
        self.model.stop = True
        self.model.model_updated()

