#!/usr/bin/env python
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
from pyxt import *
from pyxt.templates import *
import os
import string
import sys
import tempfile

def geditSetup(*var):
   return Application()

def geditCleanup(*var):
    var[0].die()
    try:
        for filename in var[1]:
            os.path.ulink(filename)
    except:
        pass

def geditStartQuit():
    try:
        import pdb;pdb.set_trace()
        app = geditSetup()
        #w = app.run('gedit','GNOMEAppWindowTemplate','gedit')
        w = app.run('gedit',{'gedit':'GNOMEAppWindowTemplate'})
        #w.selectMenu('file','quit')
        w[0].selectMenu('file','quit')
    except Exception, e:
        geditCleanup(app) 
        raise e 
    finally:
        geditCleanup(app) 

def geditFileSave(filename=None):
    file_text = "Text for geditFileSave text."
    if filename is None:
        (fd, filename) = tempfile.mkstemp(".txt", "gedit-test-")
        os.close(fd)
        os.unlink(filename)

    try:
        app = geditSetup()
        #w = app.run('gedit','GNOMEAppWindowTemplate','gedit')
        w = app.run('gedit',{'gedit':'GNOMEAppWindowTemplate'})
        w[0].enterText(file_text)
        d = w[0].selectMenu('file','save')
        d[0].enterText(filename)
        d[0].clickWidget('Save')
        w[0].selectMenu('file','quit')
    except Exception, e:
        geditCleanup(app, [filename]) 
        raise e 

    try:
        lines = open(filename, 'r').readlines()
        if string.strip(lines[0]) != file_text:
            raise PyxtTestFailed, "Text does not match.\nsaved: %s\nref: %s" %\
                                    (lines[0], file_text)
        os.unlink(filename)
    except Exception, e:
        geditCleanup(app, [filename]) 
        raise e 


def geditFileOpen(filename=None):
    file_text = "Text for geditFileOpen test."
    if filename is None:
        (fd, filename_ref) = tempfile.mkstemp(".txt", "geditFileOpen-")
        os.write(fd, file_text)
        os.close(fd)

    (fd, filename_save) = tempfile.mkstemp(".txt", "geditFileOpen-")
    os.close(fd)
    os.unlink(filename_save)
    try:
        app = geditSetup()
        #w = app.run('gedit','GNOMEAppWindowTemplate','gedit')
        w = app.run('gedit',{'gedit':'GNOMEAppWindowTemplate'})
        d = w[0].selectMenu('file','open')
        d[0].textField(filename_ref)
        #d[0].enterText(filename_ref)
        d[0].clickWidget("Open")
        d = w[0].selectMenu('file','save as')
        #d[0].clearTextField()
        d[0].textField(filename_save)
        #d[0].enterText(key_home+key_shift+key_end+filename_save)
        d[0].clickWidget('Save')
        w[0].selectMenu('file','quit')
    except Exception, e:
        geditCleanup(app, [filename_save, filename_ref]) 
        raise e 

    try:
        lines = open(filename_save, 'r').readlines()
        if string.strip(lines[0]) != file_text:
            raise PyxtTestFailed, "Text does not match.\nsaved: %s\nref: %s" %\
                                    (lines[0], file_text)
        os.unlink(filename_save)
    except Exception, e:
        geditCleanup(app, [filename]) 
        raise e 

def geditHelpAbout():
    try:
        app = geditSetup()
        #w = app.run('gedit','GNOMEAppWindowTemplate','gedit')
        w = app.run('gedit',{'gedit':'GNOMEAppWindowTemplate'})
        d = w[0].selectMenu('help','about')
        d[0].clickWidget('Close')
        w[0].selectMenu('file','quit')
    except Exception, e:
        geditCleanup(app) 
        raise e 
    finally:
        geditCleanup(app) 

def geditHelpAboutCredits():
    try:
        app = geditSetup()
        #w = app.run('gedit','GNOMEAppWindowTemplate','gedit')
        w = app.run('gedit',{'gedit':'GNOMEAppWindowTemplate'})
        d = w[0].selectMenu('help','about')
        dc = d[0].clickWidget('Credits')
        dc[0].clickWidget('Close')
        d[0].clickWidget('Close')
        w[0].selectMenu('file','quit')
    except Exception, e:
        geditCleanup(app) 
        raise e 
    finally:
        geditCleanup(app) 

if __name__ == "__main__":
    #geditStartQuit()
    #import pdb;pdb.set_trace()
    #geditFileSave()
    #geditFileOpen()
    #geditHelpAbout()
    #geditHelpAboutCredits()
    if len(sys.argv) == 1:
        to_run = ['geditStartQuit','geditFileSave','geditFileOpen',\
                  'geditHelpAbout','geditHelpAboutCredits']
    else:
        to_run = sys.argv[1:]

    for func in to_run:
        globals()[func]()

    sys.exit(0)
