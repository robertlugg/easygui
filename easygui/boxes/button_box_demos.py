import os

try:
    from .button_box import buttonbox
except (SystemError, ValueError, ImportError):
    from button_box import buttonbox


def demo_buttonbox_simple():
    value = buttonbox(
        title="Simple demo",
        msg="Simple demo, choose a button",
        choices=["Button[1]", "Button[2]", "Button[3]"],
        default_choice="Button[2]")
    print("Return: {}".format(value))


def demo_buttonbox_cancel():
    value = buttonbox(
        title="Demo with cancel",
        msg="Demo with cancel button, choose a button",
        choices=["Button[1]", "Button[2]", "Button[3]", "Cancel-[x]"],
        default_choice="Button[2]",
        cancel_choice="Cancel[q]")
    print("Return: {}".format(value))


def demo_grid_of_images():
    package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  ;# My parent's directory
    images = list()
    images.append(os.path.join(package_dir, "python_and_check_logo.gif"))
    images.append(os.path.join(package_dir, "zzzzz.gif"))
    images.append(os.path.join(package_dir, "python_and_check_logo.png"))
    images = [images, images, images, images, ]
    value = buttonbox(
        title="Demo with images",
        msg="Demo with images, press buttons or images and show images",
        choices=['ok', 'cancel'],
        images=images)
    print("Return: {}".format(value))


def demo_without_callback():
    msg = "This demoes interfacing without a callback \nYou haven't pushed a button"
    while True:
        choice_selected = buttonbox(
            title="This demoes interfacing without a callback",
            msg=msg,
            choices=["Button[1]", "Button[2]", "Button[3]", "Cancel-[x]"],
            default_choice="Button[2]",
            cancel_choice="Cancel-[x]")

        msg = "This demoes interfacing WITHOUT a callback. \nYou have pushed button {} \nNotice the flicking".format(choice_selected)

        if not choice_selected:
            break


def demo_with_callback():
    """ This demoes calbacks and choices as dictionaries"""

    def actualize(box):
        msg = "You have pushed button {} \nNotice the absence of flicking!!! ".format(box.get_selected_choice())
        box.set_msg(msg)

    buttonbox(
        title="This demoes interfacing with a callback",
        msg="You haven't pushed a button \nPush a button",
        choices={"Button[1]":1, "Button[2]":2, "Button[3]":3},
        default_choice="Button[2]",
        callback=actualize)


if __name__ == '__main__':
    demo_buttonbox_simple()
    demo_buttonbox_cancel()
    demo_grid_of_images()
    demo_without_callback()
    demo_with_callback()
