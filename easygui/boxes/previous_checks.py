"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|
"""

import sys
import boxes.utils as ut

# -------------------------------------------------------
# check python version to share with the rest of modules
# -------------------------------------------------------
"""
From the python documentation:

sys.hexversion contains the version number encoded as a single integer. This is
guaranteed to increase with each version, including proper support for non-
production releases. For example, to test that the Python interpreter is at
least version 1.5.2, use:

if sys.hexversion >= 0x010502F0:
    # use some advanced feature
    ...
else:
    # use an alternative implementation or warn the user
    ...
"""

runningPython26 = True
runningPython3 = False

if sys.hexversion >= 0x020600F0:
    runningPython26 = True
else:
    runningPython26 = False

if sys.hexversion >= 0x030000F0:
    runningPython3 = True
else:
    runningPython3 = False

# --------------------------------------------------
# check tkinter version and take appropriate action
# --------------------------------------------------

if runningPython3:
    import tkinter as tk   # python3
else:
    import Tkinter as tk   # python2


if tk.TkVersion < 8.0:
    stars = "*" * 75
    ut.writeln("""\n\n\n""" + stars + """
You are running Tk version: """ + str(tk.TkVersion) + """
You must be using Tk version 8.0 or greater to use EasyGui.
Terminating.
""" + stars + """\n\n\n""")
    sys.exit(0)
