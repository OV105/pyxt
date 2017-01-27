import exceptions
###############################################################################
#
# Copyright (c) 2009 Novell, Inc.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public License 
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact Novell, Inc.
#
# To contact Novell about this file by physical or electronic mail,
# you may find current contact information at www.novell.com
#
###############################################################################

class PyxtError(exceptions.Exception):
    __name__ = "PyxtError"
    """Base class for all exceptions raised by pyxt
    """
    #def __init__(self, args=None):
    #    self.args = args

class PyxtUnmatchedXWindow(PyxtError):
    __name__ = "PyxtUnmatchedXWindow"
    """Error when unexpected XWindow appears.
    """
    def __init__(self, xwindow):
        self.xwindow = xwindow

    def __str__(self):
        return repr(self.xwindow)

class PyxtNoMenuFound(PyxtError):
    __name__ = "PyxtNoMenuFound"  
    """Error no menu item found.
    """
    def __init__(self, *var):
        self.menu = ",".join(var)

    def __str__(self):
        return repr(self.menu)

class PyxtNoWidgetFound(PyxtError):
    __name__ = "PyxtNoWidgetFound"  
    """Error no widget found.
    """
    def __init__(self, name):
        self.widget = name

    def __str__(self):
        return repr(self.widget)


class PyxtTestFailed(PyxtError):
    __name__ = "PyxtTestFailed"  
    """Test criteria failed.
    """

class Timeout(PyxtError):
    __name__ = "Timeout"
    """Function call timed out error class.
    """
    def __init__( self, args=None ):
        self.args = args

