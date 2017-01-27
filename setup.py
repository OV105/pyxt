
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
from distutils.core import setup, Extension
from distutils.command.bdist_rpm import bdist_rpm

NAME = "pyxt"

LIBRARIES = ["X11"]

###############################################################
# Macros for run time logging
# copy and paste in _pyltfx constructor.
###############################################################

         #define_macros=[('USE_TRACE_KYBD','1')]
         #define_macros=[('USE_TRACE_ALL','1')],
         #define_macros=[('USE_TRACE_EVENTS','1')],
         #define_macros=[('USE_TRACE_NEW_WIN','1')],

_pyltfx = Extension('pyxt._pyltfx',
         library_dirs = ["/usr/X11/lib"],
         libraries = ["X11", "glib-2.0"],
         include_dirs = ["/usr/include/glib-2.0", "/usr/lib/glib-2.0/include"],
         sources = ['src/pyltfxmodule.c'])

setup (
    name = NAME,
    version = '1.0',
    description = 'GUI automation package',
    author = """Tim Lee <timlee@novell.com>""",
    author_email = 'timelee@novell.com',
    url = 'http://www.novell.com',            
    packages = [NAME, NAME+".templates"],
    ext_modules = [_pyltfx],
    cmdclass =  {
                'bdist_rpm': bdist_rpm
                }
)
from distutils.core import setup, Extension
from distutils.command.bdist_rpm import bdist_rpm

NAME = "pyxt"

LIBRARIES = ["X11"]

