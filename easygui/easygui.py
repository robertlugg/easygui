"""

.. moduleauthor:: easygui developers and Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|

ABOUT EASYGUI
=============

EasyGUI provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.

.. warning:: Using EasyGUI with IDLE

    You may encounter problems using IDLE to run programs that use EasyGUI. Try it
    and find out.  EasyGUI is a collection of Tkinter routines that run their own
    event loops.  IDLE is also a Tkinter application, with its own event loop.  The
    two may conflict, with unpredictable results. If you find that you have
    problems, try running your EasyGUI program outside of IDLE.

.. note:: EasyGUI requires Tk release 8.0 or greater.

LICENSE INFORMATION
===================
EasyGUI version |version|

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
| See http://www.gnu.org/licenses/license-liglobal_state.html#GPLCompatibleLicenses
|
| The BSD License is less restrictive than GPL.
| It allows software released under the license to be incorporated into proprietary products.
| Works based on the software may be released under a proprietary license or as closed source software.
| `<http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29>`_

API
===
"""


if __name__ == '__main__':
    from boxes.demo import easygui_demo
    easygui_demo()

    # from boxes.alt_text_box import demo_textbox
    # demo_textbox()
