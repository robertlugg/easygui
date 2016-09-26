__author__ = 'Future Engineer'

"""
from:
http://stackoverflow.com/questions/27873818/easygui-and-simplecv-typeerror-module-object-is-not-callable

Note: this module has a lot of dependencies: SimpleCV, OpenCV, PIL
"""
import sys

sys.path.append('..')
import code
import easygui as eg
from easygui import *
from SimpleCV import *
from cv2 import *
from cv import *
from PIL import *
import time
import sys

# Set a breakpoint
code.interact("Code paused.  Hit ctrl-D when ready to continue", local=dict(globals(), **locals()))
while True:
    eg.msgbox("""Welcome to my program!""", image = "pi.jpg")
    msgbox("Select img ")
    nam=fileopenbox(filetypes=['*'])
    print(nam)
    img=Image.open(nam)
    img1=img.convert('1')
    time.sleep(1)
    img1.save("result.png")
    msgbox("This is the result", image = "result.png")
    msg = "Do you want to continue?"
    title = "Please Confirm"
    if ccbox(msg, title): # show continue/cancle dialog
        print("okk") # user chose continue
    else:
        sys.exit(0) # user chose cancle