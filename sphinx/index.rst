.. easygui documentation master file, created by
   sphinx-quickstart on Wed Nov 19 17:44:42 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EasyGUI
=======

EasyGUI is a module for simple GUI programming in Python. EasyGUI is different from other GUI generators in that EasyGUI is NOT event-driven. Instead, all GUI interactions are invoked by function calls that display dialog boxes. It does not require the programmer to know anything about Tkinter, frames, widgets, callbacks or lambda.

EasyGUI runs on Python 2 and 3, and does not have any dependencies outside the Python standard library. (Linux Python 2 users will have to run `sudo apt-get install python-tk` and Linux Python 3 users will have to run `sudo apt-get install python3-tk` to install Tkinter.)


Example Usage
-------------

    >>> import easygui
    >>> easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))  # click Yes
    True
    >>> easygui.msgbox('This is a basic message box.', 'Title Goes Here')  # click OK
    'OK'
    >>> easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))  # click Chocolate
    'Chocolate'

How to get easygui
------------------

You can install EasyGUI using pip::

    pip install --user easygui

You may also download the file yourself by looking for the latest release in PyPI:

`PyPI Releases page <https://pypi.org/project/easygui/#history>`_

Linux Python 2 users will have to run `sudo apt-get install python-tk` and Linux Python 3 users will have to run `sudo apt-get install python3-tk` to install Tkinter.

Table of Contents
-----------------

.. toctree::

   Support, Contacts <support>
   API <api>
   Tutorial <tutorial>
   FAQ <faq>
   Cookbook <cookbook>
   Links <links>
   GitHub Site <https://github.com/robertlugg/easygui>
   Sourceforge Site <http://sourceforge.net/projects/easygui>
   Documentation Site <http://easygui.readthedocs.org/en/master>
   Development Docs Site <http://easygui.readthedocs.org/en/develop>

* :ref:`genindex`
* :ref:`search`

**Background**

EasyGUI was started by `Stephen Ferg <http://www.ferg.org/>`_ and
was developed and supported by him through 2013. From there, work was restarted circa 2014. The first goal
was to update the then four year old release and address some bugs and minor enhancements.
That first release was 0.97

LICENSE INFORMATION
===================
EasyGUI version |version|

Copyright (c) -2016, Stephen Raymond Ferg

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution.

    3. The name of the author may not be used to endorse or promote products derived
       from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


ABOUT THE EASYGUI LICENSE
-------------------------
| This license is what is generally known as the "modified BSD license",
| aka "revised BSD", "new BSD", "3-clause BSD".
| See http://opensource.org/licenses/bsd-license.php
|
| This license is GPL-compatible.
| See `<http://en.wikipedia.org/wiki/License_compatibility>`_
| See http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses
|
| The BSD License is less restrictive than GPL.
| It allows software released under the license to be incorporated into proprietary products.
| Works based on the software may be released under a proprietary license or as closed source software.
| `<http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29>`_





