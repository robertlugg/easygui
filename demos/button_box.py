import os

from easygui import buttonbox


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