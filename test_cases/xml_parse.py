__author__ = 'Robert'
"""
from:
http://stackoverflow.com/questions/27003762/python-displaying-variable-with-multiple-xml-tags-inside-message-box

"""
import sys

sys.path.append('..')

# Import our modules here.

import easygui as eg
import lxml.etree as etree

# Get our XML file here.
# From: http://msdn.microsoft.com/en-us/library/ms762271%28v=vs.85%29.aspx
doc = etree.parse('books.xml')

# Grab the item tag and display the child tags name, description, and status.
for catalog in doc.getiterator('catalog'):
    books = list()
    for item in catalog.getiterator('book'):
        item_name = item.findtext('title')
        item_desc = item.findtext('description')
        item_status = item.findtext('publish_date')

        # Create a variable that adds the above child tags together.
        books.append('{0} | {1} | {2}'.format(item_name, item_desc, item_status))

    # Create message box to display print_xml.
    eg.msgbox('\n'.join(books), title="XML Reader")