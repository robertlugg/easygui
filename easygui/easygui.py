"""

.. moduleauthor:: Stephen Raymond Ferg and Robert Lugg (active)
.. default-domain:: py
.. highlight:: python

Version |release|

ABOUT EASYGUI
=============

EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.

.. warning:: Using EasyGui with IDLE

    You may encounter problems using IDLE to run programs that use EasyGui. Try it
    and find out.  EasyGui is a collection of Tkinter routines that run their own
    event loops.  IDLE is also a Tkinter application, with its own event loop.  The
    two may conflict, with unpredictable results. If you find that you have
    problems, try running your EasyGui program outside of IDLE.

.. note:: EasyGui requires Tk release 8.0 or greater.

LICENSE INFORMATION
===================
EasyGui version |version|

Copyright (c) 2014, Stephen Raymond Ferg

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
| See http://www.opensource.org/licenses/bsd-license.php
|
| This license is GPL-compatible.
| See `<http://en.wikipedia.org/wiki/License_compatibility>`_
| See http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses
|
| The BSD License is less restrictive than GPL.
| It allows software released under the license to be incorporated into proprietary products.
| Works based on the software may be released under a proprietary license or as closed source software.
| `<http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29>`_

API
===
"""

__all__ = [
    'ynbox', 'ccbox', 'boolbox', 'indexbox', 'msgbox', 'buttonbox',
    'integerbox', 'multenterbox', 'enterbox', 'exceptionbox',
    'choicebox', 'codebox', 'textbox', 'diropenbox',
    'fileopenbox', 'filesavebox', 'passwordbox',
    'multpasswordbox', 'multchoicebox', 'abouteasygui',
    'eg_version', 'egversion', 'egdemo', 'EgStore'
]

# Refs:
#   https://www.python.org/dev/peps/pep-0366
#   http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py
if __name__ == "__main__" and __package__ is None:
    from os import path, sys
    sys.path.append(path.dirname(path.abspath(__file__)))
# Import all functions that form the API
from boxes.base_boxes import buttonbox
from boxes.diropen_box import diropenbox
from boxes.fileopen_box import fileopenbox
from boxes.filesave_box import filesavebox

from boxes.text_box import textbox

from boxes.derived_boxes import ynbox
from boxes.derived_boxes import ccbox
from boxes.derived_boxes import boolbox
from boxes.derived_boxes import indexbox
from boxes.derived_boxes import msgbox
from boxes.derived_boxes import integerbox
from boxes.derived_boxes import multenterbox
from boxes.derived_boxes import enterbox
from boxes.derived_boxes import exceptionbox
from boxes.derived_boxes import choicebox
from boxes.derived_boxes import codebox
from boxes.derived_boxes import passwordbox
from boxes.derived_boxes import multpasswordbox
from boxes.derived_boxes import multchoicebox

from boxes.egstore import EgStore

from boxes.about import eg_version, egversion, abouteasygui


from boxes.demo import egdemo

if __name__ == '__main__':
    egdemo()
