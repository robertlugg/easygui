import distutils.core
## WARNING: Although the following import appears to do nothing, it is required for bdist_wheel to be recognized
from setuptools import setup, find_packages

version = "0.98.0"
release = "0.98.0"

desc = list()
desc.append('EasyGUI is a module for very simple, very easy GUI programming in Python.  ')
desc.append('EasyGUI is different from other GUI generators in that EasyGUI is NOT event-driven.  ')
desc.append('Instead, all GUI interactions are invoked by simple function calls.')

long_description = """
ABOUT EASYGUI
=============

EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.

Example Usage
-------------

    >>> import easygui
    >>> easygui.ynbox('Shall I continue?', 'Title', ('Yes', 'No'))
    1
    >>> easygui.msgbox('This is a basic message box.', 'Title Goes Here')
    'OK'
    >>> easygui.buttonbox('Click on your favorite flavor.', 'Favorite Flavor', ('Chocolate', 'Vanilla', 'Strawberry'))
    'Chocolate'

Full documentation is always available.

For the most-recent production version:
<http://easygui.readthedocs.org/en/master/>.


LICENSE INFORMATION
===================
EasyGui version |version|

Copyright (c) 2015, Easygui developers and Stephen Raymond Ferg

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
"""

distutils.core.setup(
    name='easygui',
    version=version,
    url='https://github.com/robertlugg/easygui',
    description=''.join(desc),
    long_description=long_description,
    author='easygui developers and Stephen Ferg',
    author_email='robert.lugg@gmail.com',
    license='BSD',
    keywords='gui linux windows graphical user interface',
    packages=['easygui', 'easygui.boxes'],
    package_data={
        'easygui': ['python_and_check_logo.*', 'zzzzz.gif']
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: User Interfaces',
        ]
    )

