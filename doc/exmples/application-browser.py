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


def appBrowserRunApps(desktop_dir="/usr/share/applications"):
    apps = {'gftp':'gFTP', 'gedit':'.* - gedit'}
    dialogs = {'search settings':'Search', 'about':'About '}
    name_re = re.compile("^Name=(.*)")
    cat_re = re.compile("^Categories=(.*)")
    files = glob.glob(os.path.join(desktop_dir, "*.desktop"))
    for file in files:
        has_category = False
        for line in open(file, 'r'):
            m = name_re.search(line)
            if m:
                name = m.group(1)
                continue 

            m = cat_re.search(line)
            if m:
                cats = m.group(1).split(';')
                for cat in cats:
                    if cat in categories:
                        has_category = True
                        break
                        
        if has_category:
            appBrowserRunApp(name)

if __name__ == "__main__":
    appBrowserRunApps()
    sys.exit(0)
