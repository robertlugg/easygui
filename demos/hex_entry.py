from __future__ import print_function
"""
Dec 23, 2014

to robertlugg
Hello Robert,

please accept my big excuses for distrubance but simply I did not found answer on google, no one to ask. I want to make
simple GUI program to make things easier (my job is microcontrollers and electronic). Even I`m not so young neither
familiar with modern programming languages (especially with OOP), I started to learn Python before few months and
I must admit, so far so good :) ....in console, of course. It is not easy, but somehow I make some progress in learning.

Now I am trying to make simple GUI utility which generate 8 byte long commands (then I pass it to another program and
look how projected electronic responding). But, I am not sure is it possible to do it with Easygui :(
When I enter all values I would like to have button "generate" on this form and then all values in range
(depending on value of offset, I add some value on some of bytes...I will write code later for it) and to print all
values in file (in binary form).

At this moment I do not understand few thing:

is it possible to limit length of every input on only for chars?
can chars be limited only to HEX chars (0-9 and A-F , I work only with HEX values)
for example sometimes I need to forbid entering Byte3 and Byte4 (because in some cases it is constants,
for example hex values BB....). How to show them in form, but with disabled entering?
I mean this byte already have values so I do not need to enter them.

Is it possible to put simple button on form (later will write code what program must to do when button is pressed)?
Please, can You explain me more about my questions...if it is possible, how, if not why not ?
Please, I`m trying to learn...so need to know how it works.

Please, excuse me for maybe stupid questions....but I simple do not know :-/, I must to ask someone.

Here is code (to see what I`m trying to make):
"""

__author__ = 'begginer@users.sf.net via sourceforge.com'

import re
import sys
sys.path.append('..')
from easygui import multenterbox

title = "HEX values generator"
fieldNames = ["Byte1 start", "Byte1 end", "Byte2 start", "Byte2 end", "Byte3 start", "Byte3 end", "Byte4 start", "Byte4 end", "OFFSET"]
fieldShouldEnter = [True]*len(fieldNames)  # Assume all are required.  You can modify this to specify which ones!
fieldStatuses = ['Required']*len(fieldNames)
fieldValues = ['']*len(fieldNames)  # we start with blanks for the values

r = re.compile("^[0-9a-fA-F]{2,2}$")  # Hex validation

while 1:
    msg = list()
    msg.append("Enter starting and ending values")
    msg.append(" Field\t\tValue\tStatus")
    for fieldName, fieldValue, fieldStatus in zip(fieldNames, fieldValues, fieldStatuses):
        msg.append("  {0}\t{1}\t{2}".format(fieldName, fieldValue, fieldStatus))
    msg_text = '\n'.join(msg)

    previousFieldValues = fieldValues[:]  # Save values just in case user typed them incorrectly
    fieldValues = multenterbox(msg_text, title, fieldNames, fieldValues)
    if fieldValues is None:
        break  # User hit Cancel button

    # Clean fieldValues list
    temp = list()
    for fieldValue in fieldValues:
        temp.append(fieldValue.strip())
    fieldValues = temp

    # Validate entries
    for i, fieldValue in enumerate(fieldValues):
        # If left empty, require reentry
        if not len(fieldValue):
            fieldStatuses[i] = 'ERROR.  Required.'
            continue
        # If length is not exactly 2, re-enter:
        if len(fieldValue) != 2:
            fieldStatuses[i] = 'ERROR. Must be exactly 2 chars'
            continue
        if not r.match(fieldValue):
            fieldStatuses[i] = 'ERROR.  Must be a HEX number'
            continue
        if not fieldShouldEnter:
            fieldValues[i] = previousFieldValues # Always restore "READ ONLY" fields to their default
        fieldStatuses[i] = 'OK.'  # All checks passed
    if all([status == 'OK.' for status in fieldStatuses]):
        break  # no problems found, all statuses are 'OK'

print("Reply was:{}".format(fieldValues))