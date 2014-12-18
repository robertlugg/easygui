EasyGui 

Product.: EasyGui
Version.: 0.96
Released: 2010-08-29
Author..: Stephen Raymond Ferg
HomePage: http://easygui.sourceforge.net 
About...: EasyGUI is a module for simple, easy GUI programming in Python. 
License.: modified BSD


========================================================================
LICENSE - Executive summary
========================================================================

This license is generally known as the "modified BSD license".
It is also known as "revised BSD", "new BSD", and "3-clause BSD".

This license is GPL-compatible.

This license is less restrictive than GPL. It allows software released under 
the license to be incorporated into proprietary products. Works based on the 
software may be released under a proprietary license or as closed-source software.

See:
http://www.opensource.org/licenses/bsd-license.php
http://en.wikipedia.org/wiki/License_compatibility
http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses
http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29

========================================================================
LICENSE  
========================================================================

EasyGui version0.96
Copyright (c) 2010, Stephen Raymond Ferg
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer. 

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution. 

3. The name of the author may not be used to endorse or promote products derived 
from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED 
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
OF SUCH DAMAGE.

========================================================================
VERSION HISTORY 
========================================================================


========================================================================
0.96(2010-08-29)
========================================================================
This version fixes some problems with version independence.

BUG FIXES
------------------------------------------------------
 * A statement with Python 2.x-style exception-handling syntax raised
   a syntax error when running under Python 3.x.
   Thanks to David Williams for reporting this problem.

 * Under some circumstances, PIL was unable to display non-gif images
   that it should have been able to display.
   The cause appears to be non-version-independent import syntax.
   PIL modules are now imported with a version-independent syntax.
   Thanks to Horst Jens for reporting this problem.

LICENSE CHANGE
------------------------------------------------------
Starting with this version, EasyGui is licensed under what is generally known as
the "modified BSD license" (aka "revised BSD", "new BSD", "3-clause BSD").
This license is GPL-compatible but less restrictive than GPL.
Earlier versions were licensed under the Creative Commons Attribution License 2.0.


========================================================================
0.95(2010-06-12)
========================================================================

ENHANCEMENTS
------------------------------------------------------
 * Previous versions of EasyGui could display only .gif image files using the
   msgbox "image" argument. This version can now display all image-file formats
   supported by PIL the Python Imaging Library) if PIL is installed.
   If msgbox is asked to open a non-gif image file, it attempts to import
   PIL and to use PIL to convert the image file to a displayable format.
   If PIL cannot be imported (probably because PIL is not installed)
   EasyGui displays an error message saying that PIL must be installed in order
   to display the image file.

   Note that
   http://www.pythonware.com/products/pil/
   says that PIL doesn't yet support Python 3.x.


========================================================================
0.94(2010-06-06)
========================================================================

ENHANCEMENTS
------------------------------------------------------
 * The codebox and textbox functions now return the contents of the box, rather
   than simply the name of the button ("Yes").  This makes it possible to use
   codebox and textbox as data-entry widgets.  A big "thank you!" to Dominic
   Comtois for requesting this feature, patiently explaining his requirement,
   and helping to discover the tkinter techniques to implement it.

   NOTE THAT in theory this change breaks backward compatibility.  But because
   (in previous versions of EasyGui) the value returned by codebox and textbox
   was meaningless, no application should have been checking it.  So in actual
   practice, this change should not break backward compatibility.

 * Added support for SPACEBAR to command buttons.  Now, when keyboard
   focus is on a command button, a press of the SPACEBAR will act like
   a press of the ENTER key; it will activate the command button.

 * Added support for keyboard navigation with the arrow keys (up,down,left,right)
   to the fields and buttons in enterbox, multenterbox and multpasswordbox,
   and to the buttons in choicebox and all buttonboxes.

 * added highlightthickness=2 to entry fields in multenterbox and
   multpasswordbox.  Now it is easier to tell which entry field has
   keyboard focus.


BUG FIXES
------------------------------------------------------
 * In EgStore, the pickle file is now opened with "rb" and "wb" rather than
   with "r" and "w".  This change is necessary for compatibility with Python 3+.
   Thanks to Marshall Mattingly for reporting this problem and providing the fix.

 * In integerbox, the actual argument names did not match the names described
   in the docstring. Thanks to Daniel Zingaro of at University of Toronto for
   reporting this problem.

 * In integerbox, the "argLowerBound" and "argUpperBound" arguments have been
   renamed to "lowerbound" and "upperbound" and the docstring has been corrected.

   NOTE THAT THIS CHANGE TO THE ARGUMENT-NAMES BREAKS BACKWARD COMPATIBILITY.
   If argLowerBound or argUpperBound are used, an AssertionError with an
   explanatory error message is raised.

 * In choicebox, the signature to choicebox incorrectly showed choicebox as
   accepting a "buttons" argument.  The signature has been fixed.


========================================================================
0.93(2009-07-07)
========================================================================

ENHANCEMENTS
------------------------------------------------------

 * Added exceptionbox to display stack trace of exceptions

 * modified names of some font-related constants to make it
   easier to customize them


========================================================================
0.92(2009-06-22)
========================================================================

ENHANCEMENTS
------------------------------------------------------

 * Added EgStore class to to provide basic easy-to-use persistence.

BUG FIXES
------------------------------------------------------

 * Fixed a bug that was preventing Linux users from copying text out of
   a textbox and a codebox.  This was not a problem for Windows users.

