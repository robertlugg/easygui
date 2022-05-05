from easygui import textbox

def demo_1():

    title = "Demo of textbox: Classic box"

    gnexp = ("This is a demo of the classic textbox call, "
             "you can see it closes when ok is pressed.\n\n")

    challenge = "INSERT A TEXT WITH MORE THAN TWO PARAGRAPHS"

    text = "Insert your text here\n"

    msg = gnexp + challenge

    finished = False
    while True:

        text = textbox(msg, title, text)
        escaped = not text
        if escaped or finished:
            break

        if text.count("\n") >= 2:
            msg = (u"You did it right! Press OK")
            finished = True
        else:
            msg = u"You did it wrong! Try again!\n" + challenge


class Demo2(object):

    """ Program that challenges the user to write 5 a's """

    def __init__(self):
        """ Set and run the program """

        title = "Demo of textbox: Classic box with callback"

        gnexp = ("This is a demo of the textbox with a callback, "
                 "it doesn't flicker!.\n\n")

        msg = "INSERT A TEXT WITH FIVE OR MORE A\'s"

        text_snippet = "Insert your text here"

        self.finished = False

        textbox(gnexp + msg, title, text_snippet, callback=self.check_answer, run=True)

    def check_answer(self, box):
        """ Callback from TextBox

        Parameters
        -----------
        box: object
            object containing parameters and methods to communicate with the ui

        Returns
        -------
        nothing:
            its return is through the box object
        """

        if self.finished:
            box.stop()

        if box.text.lower().count("a") >= 5:
            box.msg = u"\n\nYou did it right! Press OK button to continue."
            box.stop()
            self.finished
        else:
            box.msg = u"\n\nMore a's are needed!"


class Demo3(object):

    """ Program that challenges the user to find a typo """

    def __init__(self):
        """ Set and run the program """

        self.finished = False

        title = "Demo of textbox: Object with callback"

        msg = ("This is a demo of the textbox set as "
               "an object with a callback, "
               "you can configure it and when you are finished, "
               "you run it.\n\nThere is a typo in it. Find and correct it.")

        text_snippet = "Hello"  # This text wont show

        box = textbox(msg, title, text_snippet, callback=self.check_answer, run=False)

        box.text = (
            "It was the west of times, and it was the worst of times. "
            "The  rich ate cake, and the poor had cake recommended to them, "
            "but wished only for enough cash to buy bread."
            "The time was ripe for revolution! ")

        box.run()

    def check_answer(self, box):
        """ Callback from TextBox

        Parameters
        ----------
        box: object
            object containing parameters and methods to communicate with the ui

        Returns
        -------
        nothing:
            its return is through the box object
        """
        if self.finished:
            box.stop()

        if "best" in box.text:
            box.msg = u"\n\nYou did right! Press OK button to continue."
            self.finished = True
        else:
            box.msg = u"\n\nLook to the west!"

if __name__ == '__main__':
    demo_1()
    Demo2()
    Demo3()