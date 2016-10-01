import os

try:
    from .button_box import buttonbox
except (SystemError, ValueError, ImportError):
    from button_box import buttonbox

def demo_buttonbox_1():
    print("hello from the demo")
    value = buttonbox(
        title="First demo",
        msg="bonjour",
        choices=["Button[1]", "Button[2]", "Button[3]"],
        default_choice="Button[2]")
    print("Return: {}".format(value))


def demo_buttonbox_2():
    package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  ;# My parent's directory
    images = list()
    images.append(os.path.join(package_dir, "python_and_check_logo.gif"))
    images.append(os.path.join(package_dir, "zzzzz.gif"))
    images.append(os.path.join(package_dir, "python_and_check_logo.png"))
    images = [images, images, images, images, ]
    value = buttonbox(
        title="Second demo",
        msg="Now is a good time to press buttons and show images",
        choices=['ok', 'cancel'],
        images=images)
    print("Return: {}".format(value))


def demo_buttonbox_3():
    msg = "This demoes interfacing without a callback \nYou haven't pushed a button"
    while True:
        choice_selected = buttonbox(
            title="This demoes interfacing without a callback",
            msg=msg,
            choices=["Button[1]", "Button[2]", "Button[3]"],
            default_choice="Button[2]")

        msg = "You have pushed button {} \nNotice the flicking".format(choice_selected)

        if not choice_selected:
            break


def demo_buttonbox_4():
    """ This demoes calbacks and choices as dictionaries"""

    def actualize(box):
        msg = "You have pushed button {} \nNotice the absence of flicking!!! ".format(box.choice_selected)
        box.set_msg(msg)

    buttonbox(
        title="This demoes interfacing with a callback",
        msg="This demoes interfacing WITH a callback \nYou haven't pushed a button",
        choices={"Button[1]":1, "Button[2]":2, "Button[3]":3},
        default_choice="Button[2]",
        callback=actualize)


if __name__ == '__main__':
    demo_buttonbox_1()
    demo_buttonbox_2()
    demo_buttonbox_3()
    demo_buttonbox_4()