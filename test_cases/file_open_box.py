__author__ = 'Robert'
"""
from:
http://stackoverflow.com/questions/25087169/python-easygui-cant-select-file

"""
import sys
sys.path.append('..')
import easygui
f = easygui.fileopenbox()
print(f)