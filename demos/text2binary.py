__author__ = 'Robert'
"""
from:
http://stackoverflow.com/questions/27393751/converting-text-to-binary-2-part-issue
"""
import sys

sys.path.append('..')
import easygui

Plain = easygui.textbox(msg='Enter Message', title='OTP', text=u'Hi', codebox=1)
print(repr(Plain)) #If there is no trailing newline, its OK