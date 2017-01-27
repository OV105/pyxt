
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
from _pyltfx import *
from pyxt_exceptions import *
#from pyxt import *
from _pyxt import *
import os
import sys
import glob

class Application(Pyxt):
    __name__ = "Application"
    DEFAULT_CONF_DIR_LIST = ["/etc/pyxt", os.path.expanduser("~/pyxt")]
    OPT_NAME = "modules"
    def __init__(self, display_string=None, logger=None, debug_level=0):
        self.logger = getLogger(logger, debug_level)
        self.default_mod_dirs = [os.path.join(os.path.dirname(os.path.abspath(\
                          sys.modules[self.__module__].__file__)),'templates')]
        self.cmd = None
        self.modules = {}
        self.classes = {}
        self.current_sect = None
        if os.access(os.getcwd(), os.W_OK):
            log_name = time.strftime("%d-%b-%H:%M.%S")
            self.log_file_name = os.path.join(os.getcwd(), log_name)
        else:
            self.log_file_name = None

        for mod_dir in self.default_mod_dirs:
            file_list = glob.glob(os.path.join(mod_dir, "*.py*"))
            for file in file_list:
                if os.path.basename(file) == "__init__.py":
                    continue

                self.addModule(file)
                
        config_files = []
        for dir in self.DEFAULT_CONF_DIR_LIST:
            if os.path.isdir(dir):
                for file in os.listdir(dir):
                    if file[0] != '.':
                        config_files.append(os.path.join(dir, file))

        for config_file in config_files:
            self.parseConfig(config_file)

        Pyxt._start(self, display_string)

    def run(self, cmd, test_dict, ignore_exit=False):
        self.cmd = cmd
        self.criteria = PyxtCriteria(reg_expr=test_dict.keys(), \
                            logger=self.logger)
        if cmd is None:
            self.proc = None
            self.search(self.criteria)
        else:
            self.proc = popen2.Popen3(cmd)
            time.sleep(.5)
            try:
                self.expect(self.criteria) 
            except:
                pass
            else:
                pass

            if self.proc.poll() != -1:
                if self.proc.poll() != 0 and not ignore_exit:
                    self.die()
                    raise PyxtError, "Command exited: %s, status: %d\n%s" % \
                         (cmd, self.proc.poll(), self.proc.fromchild.read())
                else:
                    self.proc = None

        if self.criteria.hasMatch():
            time.sleep(.2)
            self.criteria.validateMatches()
        else:
            self.die()
            raise PyxtError, "Cannot find window matching: %s" % test_dict.keys() 

        result = []
        for key in self.criteria.matches.iterkeys():
            result.append(self.getWindowTemplate(test_dict[key],
                          self.criteria.matches[key]))

        return result

    def getWindowTemplate(self, template_name, xwindows):
        if self.classes.has_key(template_name):
            win = self.classes[template_name](xwindows, self, self.logger)
        else:
            win = self.classes['WindowTemplate'](xwindows, self, self.logger)

        return win

    def parseConfig(self, config_file):
        parse = ConfigParser.SafeConfigParser()
        try:
            parse.read(config_file)
        except ConfigParser.MissingSectionHeaderError, e:
            pass
            #FIXME raise error ?
        
        for sect in parse.sections():
            if self.modules.has_key(sect):
                raise PyxtError, "Duplicate section name: %s in %s"\
                        % (sect, config_file)

            if not parse.has_option(sect, self.OPT_NAME):
                raise PyxtError, "File %s missing option %s in section %s "\
                        % (config_file, self.OPT_NAME, sect)
            
            module_names = parse.get(sect, self.OPT_NAME).split(':')
            for mod_file in module_names:
                if os.path.isfile(mod_file):
                    self.addModule(mod_file, sect)
                elif os.path.isdir(mod_file):
                    #FIXME recursively add modules in directory
                    file_list = glob.glob(os.path.join(mod_file, "*.py*"))
                    for file in file_list:
                        self.addModule(file, sect)


    def addModule(self, mod_file, sect="default"):
        if not self.modules.has_key(sect):
            self.modules[sect] = []

        if os.path.isabs(mod_file):
            mod_file = os.path.abspath(mod_file)

        (mod_path, file_name) = os.path.split(mod_file)
        if file_name[-3:] == '.py':
            mod_name = file_name[:-3]
        elif file_name[-4:] == '.pyc':
            mod_name = file_name[:-4]
        else:
            mod_name = file_name
        
        if sys.path.count(mod_path) == 0:
            sys.path.append(mod_path)


        try:
            mod = __import__(mod_name)
        except ImportError, e:
            raise PyxtError, "Cannot import %s from %s\n %s" %\
                    (name, config_file, e)

        self.modules[sect].append(mod)
        mod_members = inspect.getmembers(mod)
        for mem in mod_members:
            if mem[0] == '__builtins__':
                continue

            if not inspect.isclass(mem[1]):
                continue

            try:
                if inspect.getmro(mem[1])[-1].__name__ == 'WindowTemplate':
                    if self.classes.has_key(mem[0]):
                        if self.classes[mem[0]] is not mem[1]:
                            raise PyxtError, "Duplicate template: %s, in %s"\
                                        % (mem[0], sect)
                    else: 
                        self.classes[mem[0]] = mem[1]

            except AttributeError:
                pass

    def _writeLog(self):
        if self.popen_obj is not None:
            lines = self.self.popen_obj.fromchild.readlines()
            try:
                open(self.log_file_name, 'a').write(lines)
            except IOError, e:
                print "Error writing %s, %s" % (self.log_file_name, e)
                self.log_file_name = None
            #self.log_file.write(lines)

    def kill(self):
        self.die()
        os.kill(self.proc.pid, signal.SIGABRT)
        time.sleep(1)
        if self.proc.poll() != -1:
            os.kill(self.proc.pid, signal.SIGKILL)
            time.sleep(1)
        
        if self.proc.poll() != -1:
            raise PyxtError, "Unable to kill %d" % self.proc.pid
        
class MenuItem:
    __name__ = "MenuItem"
    ########################################################################
    # tests format
    #   'window title regular expression':<window_template or event_type>
    #    key of None is assumed to refer to window that string was sent to.
    #    value of event_type only valid when key is None
    ########################################################################
    def __init__(self, string=None, parent=None, shortcut=None):
        self.string = string
        self.parent = parent
        self.shortcut = shortcut

    def getString(self):
        if self.shortcut is None:
            if self.parent is None:
                result = self.string
            else:
                result = self.parent.getString()
                result += self.string
        else:
            result = self.shortcut

        return result

class Widget:
    __name__ = "Widget"
    def __init__(self, shortcut, tab_count=0):
        self.shortcut = shortcut
        self.tab_count = tab_count
        self.selection_count = 0

    def getString(self, selection_count=0):
        cmd_string = self.shortcut
        if self.tab_count > 0:
            tab_string = key_tab 
        else:
            tab_string = "%s%s" % (key_shift, key_tab)
        
        for cnt in range(abs(self.tab_count)):
            cmd_string += tab_string

        if selection_count > self.selection_count: 
            for cnt in range(self.selection_count, selection_count):
                cmd_string += key_up
        else:
            for cnt in range(selection_count, self.selection_count):
                cmd_string += key_down

        self.selection_count = selection_count
        return cmd_string

class WindowTemplate:
    __name__ = "WindowTemplate"
    def __init__(self, xwin_list, application, logger):
        self.xwin_list = xwin_list
        self.menu_delay = .1 
        self.text_delay = .1
        self.widget_delay = 0
        self.delay = 0
        self.application = application
        self.logger = logger
        self.menu_items = {}
        self.widgets = {}
        self.tests = {}
        self.criteria = None
        self.build()

    def build(self):
        pass

    def selectMenu(self, *menu_strings):
        cmd = self.getCmd(self.getMenuString(*menu_strings))
        result = None
        self.delay = self.menu_delay
        if cmd is not None:
            result = self.runCmd(cmd, *menu_strings)
        else:
            raise PyxtNoMenuFound(*menu_strings)

        return result

    def clickWidget(self, widget_name, count=0):
        cmd = self.getCmd(self.getWidgetString(widget_name, count))
        result = None
        self.delay = self.widget_delay
        if cmd is not None:
            result = self.runCmd(cmd, widget_name)
        else:
            raise PyxtNoWidgetFound(widget_name)

        return result

    def enterText(self, text, criteria=None):
        cmd = self.getCmd(text)
        if criteria is None:
            cmd.execute(delay=self.text_delay)
            result = [] 
        else:
            self.criteria = criteria
            result = self.runCmd(cmd)
        
        return result

    def runCmd(self, cmd, *var):
        self.criteria = None
        try:
            test_dict = self.tests[var]
        except KeyError:
            #If no tests match all event windows
            test_dict = {'.*':WindowTemplate}

        if test_dict.has_key(self):
            self.criteria = PyxtCriteria(match_xwindow=self.xwin_list,
                                        event_type = test_dict[self],
                                        start_time=cmd.started)
        else:
            self.criteria = PyxtCriteria(reg_expr=test_dict.keys(), \
                                    start_time=cmd.started)

        #return self._runCmd(cmd)

    #def _runCmd(self, cmd):
        result = []
        cmd.execute(delay=self.delay)
        self.application.expect(self.criteria)
        time.sleep(.2)
        self.criteria.validateMatches()
        for key, win_list in self.criteria.matches.iteritems():
            if type(key) is str:
                result.append(self.application.getWindowTemplate(test_dict[key],
                                         self.criteria.matches[key]))
            else:
                result.append(self)

        return result

    def getCmd(self, cmd_string): 
        cmd = None
        if cmd_string is not None:
            for xwin in self.xwin_list:
                if xwin.isValid():
                    cmd = PyxtCommand(xwin, cmd_string)
                    break
       
        return cmd

    def getMenuString(self, *menu_names):
        try:
            result = self.menu_items[menu_names].getString()
        except KeyError:
            #FIXME raise PyxtError, "No menu found for: %s" % ','.join(menu_key)
            result = None
        
        return result

    def getWidgetString(self, widget_name, count):
        if not type(widget_name) is str:
            raise TypeError, "Widget name not string: %s" % type(widget_name)
        
        try:
            result = self.widgets[widget_name].getString(count)
        except KeyError:
            #FIXME raise PyxtError, "No widget found for: %s" % widget_name
            result = None

        return result

    def getTests(self, *kybd_cmds):
        try:
            result = self.tests[kybd_cmds]
        except KeyError:
            result = {}
            #FIXME raise error ?

        return result
        
