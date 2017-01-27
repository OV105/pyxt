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
import glob

try:
    from popen2 import
except ImportError:
    from subprocess import call as run

def appBrowserSetup(*var):
   return Application()

def appBrowserCleanup(*var):
    var[0].die()
    try:
        for filename in var[1]:
            os.path.ulink(filename)
    except:
        pass

def appBrowserRunApp(link_text):
    try:
        app = appBrowserSetup()
        ab = app.run('application-browser', \
                     {'Application Browser':'AppBrowserDialogTemplate'},
                     ignore_exit=True)
        criteria = PyxtCriteria()
        w = ab[0].enterText(link_text+key_rtrn, criteria)
        #ab[0].enterText(key_rtrn, criteria)
    except Exception, e:
        appBrowserCleanup(app) 
        raise e 
    finally:
        appBrowserCleanup(app) 


def runCmd(cmd, app):
    ab = app.run(cmd, {".*":'AppWindowTemplae'}, ignore_exit=True)

def main(desktop_dir="/usr/share/applications"):
    dialogs = {'search settings':'Search', 'about':'About '}
    name_re = re.compile("^Name=(.*)")
    cmd_re = re.compile("^Exec=(.*)")
    app = Application()
    desktop_files = glob.glob(os.path.join(desktop_dir, "*.desktop"))
    for file in files:
        cmd = None
        for line in open(file, 'r'):
            m = name_re.search(line)
            if m:
                name = m.group(1)
                continue 

            m = cmd_re.search(line)
            if m:
                cmd = m.group(1)
                continue 

        if cmd is not None:
            runCmd(cmd, app)
                        
        #if has_category:
        #    appBrowserRunApp(name)

if __name__ == "__main__":
    main()
    sys.exit(0)
