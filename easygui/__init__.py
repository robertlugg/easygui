"""
easygui/__init__.py

__all__ must be defined in order for Sphinx to generate the API automatically.

"""

__all__ = [
    # boxes using the ButtonBox class
    "buttonbox", "msgbox", "boolbox", "ynbox", "ccbox", "indexbox",
    # boxes using the ChoiceBox class
    "choicebox", "multchoicebox",
    # filedialog boxes that directly use existing tkinter implementation
    "fileopenbox", "filesavebox", "diropenbox",
    # boxes using the FillableBox class
    "fillablebox", "enterbox", "passwordbox", "integerbox",
    # boxes using the MultiBox class
    "multenterbox", "multpasswordbox",
    # boxes using the TextBox class
    "textbox", "codebox", "exceptionbox",
    # errata
    'EgStore', 'version'
]

from .button_box import buttonbox, msgbox, boolbox, ynbox, ccbox, indexbox
from .choice_box import choicebox, multchoicebox
from .egstore import EgStore
from .file_boxes import fileopenbox, filesavebox, diropenbox
from .fillable_box import fillablebox, enterbox, passwordbox, integerbox
from .multi_fillable_box import multenterbox, multpasswordbox
from .text_box import textbox, codebox, exceptionbox
import tkinter as tk  # python 3

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
version = "0.98.3"