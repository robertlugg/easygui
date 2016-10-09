import os
import random

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
        cancel_choice="Cancel-[x]")
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
        images=images,
        default_choice="ok",
        cancel_choice="Cancel-[x]")
    print("Return: {}".format(value))


def demo_without_callback():
    msg = "This demoes interfacing without a callback \nPush to get a random number between 1 and 10"
    while True:
        selected_choice = buttonbox(
            msg=msg,
            choices=["Get me a number", "[C]ancel"],
            default_choice="Get me a number",
            cancel_choice="[C]ancel")
        number = random.randint(1, 10)
        msg = "This demoes interfacing WITHOUT a callback. \nYou got number {} \nNotice the flicking".format(number)

        if not selected_choice:
            break


def demo_with_callback():
    """ This demoes calbacks and choices as dictionaries"""

    def update(box):
        number = random.randint(1, 10)
        msg = "This demoes interfacing WITH a callback. \nYou got number {} \nNotice the absence of flicking".format(number)
        box.set_msg(msg)

    msg = "This demoes interfacing with a callback \nPush to get a random number between 1 and 10"

    buttonbox(
        title="This demoes interfacing with a callback",
        msg=msg,
        choices=["Get me a number", "[C]ancel"],
        default_choice="Get me a number",
        cancel_choice="[C]ancel",
        callback=update)


if __name__ == '__main__':
    demo_buttonbox_simple()
    demo_buttonbox_cancel()
    demo_grid_of_images()
    demo_without_callback()
    demo_with_callback()
