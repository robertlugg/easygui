"""
Hello from easygui/__init__.py

"""

# __all__ must be defined in order for Sphinx to generate the API automatically.
__all__ = ['buttonbox',
           'diropenbox',
           'fileopenbox',
           'filesavebox',
           'textbox',
           'ynbox',
           'ccbox',
           'boolbox',
           'indexbox',
           'msgbox',
           'integerbox',
           'multenterbox',
           'enterbox',
           'exceptionbox',
           'choicebox',
           'codebox',
           'passwordbox',
           'multpasswordbox',
           'multchoicebox',
           'EgStore',
           'eg_version',
           'egversion',
           'abouteasygui',
           'egdemo',
]

# Import all functions that form the API
from .boxes.button_box import buttonbox
from .boxes.diropen_box import diropenbox
from .boxes.fileopen_box import fileopenbox
from .boxes.filesave_box import filesavebox

from .boxes.text_box import textbox

from .boxes.derived_boxes import ynbox
from .boxes.derived_boxes import ccbox
from .boxes.derived_boxes import boolbox
from .boxes.derived_boxes import indexbox
from .boxes.derived_boxes import msgbox
from .boxes.derived_boxes import integerbox
from .boxes.multi_fillable_box import multenterbox
from .boxes.derived_boxes import enterbox
from .boxes.derived_boxes import exceptionbox
from .boxes.choice_box import choicebox
from .boxes.derived_boxes import codebox
from .boxes.derived_boxes import passwordbox
from .boxes.multi_fillable_box import multpasswordbox
from .boxes.choice_box import multchoicebox
from .boxes.egstore import EgStore, read_or_create_settings
from .boxes.about import eg_version, egversion, abouteasygui
from .boxes.demo import easygui_demo as egdemo

