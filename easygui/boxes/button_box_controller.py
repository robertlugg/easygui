

class BoxController(object):

    def __init__(self, model, view):
        """
        :param object model: holds the data of this call
        :param function callback: if set, this function will be called when any button is pressed.
        """
        self.model = model
        self.view = view


    # Methods executing when a key is pressed -------------------------------
    # If cancel, x, or escape, close ui and return None
    def x_pressed(self):
        self.nothing_selected_and_stop()

    def escape_pressed(self, event):
        self.nothing_selected_and_stop()

    def button_pressed(self, button_text):
        # If cancel
        cancel_presed = (button_text == self.model.cancel_choice)
        if cancel_presed:
            self.nothing_selected_and_stop()
        else:
            # So there has been a choice selected
            self.model.choices.select_choice(button_text)
            self.model.check_callback_updated()

    def image_pressed(self, filename, row, column):
        self.model.choices.select_choice(None)
        self.model.row_column_selected = (row, column)
        self.model.model_updated()

    def nothing_selected_and_stop(self):
        self.model.choices.select_choice(None)
        self.model.row_column_selected = None
        self.model.stop = True
        self.model.model_updated()

