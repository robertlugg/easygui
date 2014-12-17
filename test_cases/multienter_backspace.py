__author__ = 'Robert'

"""
from:
http://stackoverflow.com/questions/26200738/how-to-add-backspace-event-to-easygui-multenterbox-fileds

"""
import sys

sys.path.append('..')
from easygui import *

msg         = "Enter name"
title       = "New name"
fieldName  = ['name']


newTitle= 'NewName'

fieldValue = [newTitle]
fieldValue = multenterbox(msg,title, fieldName,fieldValue)

# make sure that none of the fields were left blank
while 1:  # do forever, until we find acceptable values and break out
    if fieldValue == None:
        break
    errmsg = ""
    # look for errors in the returned values
    for i in range(len(fieldName)):
        if fieldValue[i].strip() == "":
            errmsg = errmsg + '"{}" is a required field.\n\n'.format(fieldName[i])
    if errmsg == "":
        # no problems found
        print ("Reply was:", fieldValue)
        break
    else:
        # show the box again, with the errmsg as the message
        fieldValue = multenterbox(errmsg, title, fieldName, fieldValue)