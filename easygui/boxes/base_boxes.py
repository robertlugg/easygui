"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|
"""


if __name__ == "__main__" and __package__ is None:
    from os import path
    sys.path.append(path.dirname(path.abspath(__file__)))

boxRoot = None


def bindArrows(widget):

    widget.bind("<Down>", tabRight)
    widget.bind("<Up>", tabLeft)

    widget.bind("<Right>", tabRight)
    widget.bind("<Left>", tabLeft)


def tabRight(event):
    boxRoot.event_generate("<Tab>")


def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")

if __name__ == '__main__':
    print("Hello from base_boxes")
