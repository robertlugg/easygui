"""

.. moduleauthor:: shanmugam
.. default-domain:: py
.. highlight:: python
.. added-features:: popup box with timeout function

Version |release|
"""

import os
import re

try:
    from . import global_state
    from . import utils as ut
    from .text_box import textbox
except (SystemError, ValueError, ImportError):
    import global_state
    import utils as ut
    from text_box import textbox

try:
    import tkinter as tk  # python 3
    import tkinter.font as tk_Font
except (SystemError, ValueError, ImportError):
    import Tkinter as tk  # python 2
    import tkFont as tk_Font





def popupmsg(msg, timeout, title="Popup", padx=None, pady=None, ipadx=None, ipady=None):
    popup = tk.Tk()
    popup.wm_title(title)

    # Set default values if parameters are not provided
    if padx is not None :
        padx = padx
    else :
        padx = 70

    if pady is not None :
        pady = pady
    else :
        pady = 70

    if ipadx is not None :
        ipadx = ipadx
    else :
        ipadx = 0

    if ipady is not None :
        ipady = ipady
    else :
        ipady = 0
        
    
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

    # Function to destroy the popup after the specified timeout
    def destroy_popup():
        popup.destroy()

    # Schedule the destruction of the popup after the specified timeout
    popup.after(timeout, destroy_popup)

    popup.mainloop()

# Example usage:
# popupmsg("Hello, this is a custom popup!", 3000, title="Custom Title", padx=20, pady=20, ipadx=5, ipady=5)


# Example usage:
dude = "Hello, this is a popup message!"

if __name__ == '__main__':
    popupmsg(dude,5000)
