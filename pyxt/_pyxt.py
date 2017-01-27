### python module
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
import _pyltfx
import threading
import time
import popen2
import re
import pyxt_exceptions
import logging
import Queue
import copy
import os
import ConfigParser
import inspect
from pyxt_exceptions import *

def compileREString(re_list):
    if len(re_list) == 0:
        re_string =  " "
    else:
        re_string = ""
        for re_item in re_list:
            if type(re_item) == str:
                re_string += "(%s)|" % (re_item)
            else:
                raise TypeError, "Only list of strings allowed, not:  %s",\
                                  type( reg_expr_item )
    return re_string[:-1]

def getLogger(logger=None, debug_level=0):
    if logger is None:
        result = logging.getLogger("pyxt")
        if len(result.handlers) == 0:
            if debug_level > 2:
                debug_level = 2

            result.setLevel( 30 - debug_level * 10 )
            handler = logging.StreamHandler()
            s = "\n%(module)s:%(lineno)d - %(threadName)s - %(asctime)s\n %(message)s"
            f = logging.Formatter(s)
            handler.setFormatter(f)
            result.addHandler(handler)
    else:
        result = logger

    return result

class PyxtCommand:
    __name__ = "PyxtCommand"
    def __init__(self, xwindow, strings=None, type_char_delay=.05):
        self.type_char_delay = type_char_delay
        self.last_time = time.time()
        self.cmd_strings = []
        self.started = 0
        self.finished = 0
        #if type(xwindow ) is not _pyltfx.XWindow:
        #    raise TypeError, "%s is not a pyxt XWindow" % type( xwindow )
        if xwindow.__class__ != _pyltfx.XWindow:
            raise TypeError, "%s is not a pyxt XWindow" % xwindow.__class__ 
            
        self.xwindow = xwindow 
        self.addStrings(strings)

    def __repr__(self):
        return "<PyxtCommand: %#x>" % self.xwindow.this_window
  
    def __str__(self):
        return self.__repr__()

    def addStrings(self, strings):
        if type(strings) is list:
            self.cmd_strings.extend(strings)
        elif type(strings) is str:
            self.cmd_strings.append(strings) 
        elif strings is not None:
            raise TypeError, "Cannot process type: %s" % type(strings)

        #if type( string ) is not str:
        #    raise TypeError, "Cannot add type: %s" % type( string )
        
        #self.cmd_strings.append(string)

    def execute(self, delay=None):
        if delay is None:
            delay = self.type_char_delay

        cmd_str = "".join(self.cmd_strings)
        self.started = time.time()
        for char in cmd_str:
            self.xwindow.type(char)
            time.sleep(delay)

        self.finished = time.time()
            
class PyxtCriteria:
    __name__ = "PyxtCriteria"
    def __init__(self, 
                 reg_expr=None, 
                 start_time=None,
                 end_time=None,
                 timeout=10,
                 match_xwindow=None,
                 raise_timeout=True,
                 event_type=_pyltfx.event_except_destroyed,
                 logger=None,
                 debug_level=0,
                 result_window_name=None):
        self.logger = getLogger(logger, debug_level)
        if timeout is None:
            self.timeout = PyxtCriteria.default_timeout
        else:
            self.timeout = timeout

        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

        self.match_wait = .2
        self.trials = {}
        self.result_window_names = {}
        self.matches = {}
        self.removed = []
        self.rejected= []
        #self.sect_name = sect_name
        self.addTrial(event_type, reg_expr, match_xwindow, result_window_name)

    def __repr__(self):
        result = "<PyxtCriteria "
        for re_string in self.trials.keys():
           result += "'%s' " % re_string

        result += ">"
        return result

    def addTrial(self, event_type, reg_expr=None, match_xwin=None, 
                 result_win_name=None):
        if type(reg_expr) == list:
            if len(reg_expr) == 0:
                self._addTrial(event_type, None, None, result_win_name)
            else:
                for reg_expr_item in reg_expr:
                    self._addTrial(event_type, reg_expr_item, None,\
                                   result_win_name)
        elif reg_expr is not None:
            self._addTrial(event_type, reg_expr, None, result_win_name)

        
        if type(match_xwin) == list:
            for xwin in match_xwin:
                self._addTrial(event_type, None, xwin, result_win_name)
        elif match_xwin is not None:
            self._addTrial(event_type, None, match_xwin, result_win_name)
        elif reg_expr is None:
            self._addTrial(event_type, ".*", None, result_win_name)
    
    def hasTrials(self):
        return len(self.trials) != 0

    def _addTrial(self, event_type, reg_expr, match_xwin, result_window_name):
        if reg_expr is not None and not self.trials.has_key(reg_expr):
            trial = PyxtTrial(event_type, reg_expr, None, self.logger)
            self.trials[reg_expr] = trial
            self.result_window_names[reg_expr] = result_window_name

        if match_xwin is not None and not self.trials.has_key(match_xwin):
            trial = PyxtTrial(event_type, None, match_xwin, self.logger)
            self.trials[match_xwin] = trial
            self.result_window_names[match_xwin] = result_window_name

        #if match_xwin is None and reg_expr is None:
        #    trial = PyxtTrial(event_type, None, None, self.logger)

    def reset(self):
        self.matches = {}
        self.removed = []
        
    def test(self, xwin):
        if xwin.timestamp < self.start_time:
            self.logger.debug("Xwin timestamp: %s, before start_time: %s"\
                            % (xwin.timestamp, self.start_time))
        result = False
        if xwin is None:
            return result
            
        for (key, trial) in self.trials.iteritems():
            if trial.test(xwin):
                self.logger.debug("Matched window: %#x - %s\nTrial: %s"\
                        % (xwin.this_window, xwin.getTitle(), trial))
                result = True
                if self.matches.has_key(key):
                    self.matches[key].append(xwin)
                else:
                    self.matches[key] = [xwin]

        if not result:
            self.rejected.append(xwin)

        return result

    def validateMatches(self):
        self.removed = []
        for (key, match_list) in self.matches.iteritems():
            if not self.trials[key].event_type & _pyltfx.event_destroyed:
                for i in range(len(match_list))[:-1]:
                    if not match_list[i].isValid():
                        self.logger.debug("removing window: %#x - %s"\
                                % (match_list[i].this_window, 
                                   match_list[i].getTitle()))
                        self.removed.append(match_list.pop(i))
                        if len(match_list) == 0:
                            self.matches.pop(trial)

    def hasMatch(self, key=None):
        if key is None:
            return len(self.matches) > 0
        else:
            return self.matches.has_key(key)

    def getEndTime(self):
        return time.time() + self.timeout

    def findWindowClosed( self, xwindow=None ):
        if xwindow is None:
            if self.match_xwindow is None:
                raise PyxtError, "No xwindown entered"
        else:
            self.match_xwindow = xwindow

        self.setRegExpr( None )
        self.event_type = _pyltfx.event_destroyed 
        
    def findWindowEvent( self, xwindow=None ):
        if xwindow is None:
            if self.match_xwindow is None:
                raise PyxtError, "No xwindown entered"
        else:
            self.match_xwindow = xwindow

        self.match_xwindow = xwindow
        self.setRegExpr( None )
        self.event_type = _pyltfx.event_all
   
    def findClosedEvents( self, reg_expr=".*" ):
        self.match_xwindow = None
        self.setRegExpr( reg_expr )
        self.event_type = _pyltfx.event_destroyed 
        
    def findNewEvemts( self, reg_expr=".*" ):
        self.match_xwindow = None
        self.setRegExpr( reg_expr )
        self.event_type = _pyltfx.event_new
        
    def findAllEvents( self, reg_expr=".*" ):
        self.match_xwindow = None
        self.setRegExpr( reg_expr )
        self.event_type = _pyltfx.event_all

class PyxtTrial:
    def __init__(self, event_type, reg_expr=None, match_xwin=None, logger=None):
        self.logger = getLogger(logger)
        self.re_string = None
        self.reg_expr = None 
        self.re_obj = None 
        self.match_xwin = match_xwin
        self.event_type = event_type
        if type(reg_expr) is str:
                ##FIXME check for () in string
                self.re_string = reg_expr
                self.re_obj = re.compile(reg_expr)
        elif reg_expr is None:
            if match_xwin is None:
                self.re_string = ".*"
                self.re_obj = re.compile(self.re_string)
        else:
            try:
                reg_expr.search("aaa")
            except AttributeError:
                raise TypeError, "Must be string or re object, not %s"\
                        % type(reg_expr)
            else:
                self.re_obj = reg_expr
                
    def __repr__(self):
        if self.re_string is not None:
            return "<pyxt.PyxtTrial: '%s'>" % self.re_string
        elif self.match_xwin is not None:
            return "<pyxt.PyxtTrial: %#x>" % self.match_xwin.this_window
        else:
            return "<pyxt.PyxtTrial>"
        
    def __str__( self ):
        #result = " re_string:\t%s\n" % self.re_string
        #result += " xwindow:\t\t%s\n" % self.match_xwindow
        #result += " timeout:\t\t%s\n" % self.timeout
        return self.__repr__()

    def test(self, xwin):
        result = False
        if xwin.isValid() and (xwin.event_type & self.event_type) != 0:
            if xwin == self.match_xwin:
                self.logger.info( "Event xwindow %#x - %s matches", 
                                    (xwin.this_window, xwin.getTitle()))
                result = True
            elif self.re_obj is not None and xwin.getTitle() is not None:
                #if self.re_obj.search(xwin.getTitle()):
                if self.re_obj.search(xwin.getTitle()):
                    self.logger.info( "Event xwindow %#x - %s matches", 
                                    (xwin.this_window, xwin.getTitle()))
                    result = True

        return result
   
class Pyxt:
    __name__ = "Pyxt"
    WAIT_FOR_WINDOWS = 2
    def __init__( self, display_string=':0', logger=None, debug_level=0 ):
        self.logger = getLogger(logger, debug_level)
        old_logger_name = self.logger.name
        self.logger.name = "Pyxt.__init__"

        self.criteria = None
        self._start(display_string)

    def _start(self, display_string):
        self.latest_timestamp = 0
        self.delay = .1
        self.display_string = display_string
        self.xhash = XHash(display_string, logger=self.logger)
        self.logger.debug("Starting xhash thread")
        self.xhash.start()
        if self.xhash.isAlive():
            self.logger.debug( "XHash thread is alive" )
        else:
            self.logger.error( "XHash thread is not alive" )

        self.most_recent_events = []

    def die( self ):
        old_logger_name = self.logger.name
        self.logger_name = "Pyxt.die"
        self.xhash.die()
        #self.xhash.clearAllLocks()
        self.logger.debug( "trying xhash.join" )
        self.xhash.join(5)
        if self.xhash.isAlive():
            self.logger.error( "xhash tread is still alive" )
            self.logger.name = old_logger_name
            raise PyxtError, "xhash tread is still alive"

        self.logger.name = old_logger_name
    
    def execute(self, command, criteria):
        if type(criteria) is str:
            criteria = PyxtCriteria(criteria, logger=self.logger)
        
        criteria.start_time = time.time()
        self.send(command)
        result = self.expect(criteria)
        return result

    def send(self, command):
        old_logger_name = self.logger.name
        self.logger_name = "Pyxt.send"
        if command.xwindow == None:
            #FIXME raise error ?
            self.logger.warning( "No XWindow for command" )
        else:
            for string in command.cmd_strings:
                self.logger.debug( "Sending string: %s", string )
                command.last_time = time.time()
                for char in string:
                    try:
                        command.xwindow.activate()
                        command.xwindow.type(char)
                    except Exception, e:
                        self.logger.error( "Error %s typing char %s", e, char )
                        self.logger.name = old_logger_name
                        raise PyxtError("%s" % e)
        
                time.sleep(self.delay)
            
        self.logger.name = old_logger_name
        #return result
    
    def _matchWindow(self, xwin, criteria):
        result = None
        if xwin.timestamp > self.latest_timestamp:
            self.latest_timestamp = xwin.timestamp

        if xwin.timestamp < criteria.start_time:
            self.logger.debug("Xwin timestamp: %s, before start_time: %d"\
                            % (xwin.timestamp, criteria.start_time))
        elif (xwin.event_type & criteria.event_type) != 0:
            if criteria.match_xwindow == xwin:
                self.logger.info( "Event xwindow %#x matches", 
                                    xwin.this_window )
                #result = (xwin, 0, None)
                self.xwindow_match.append(xwin)
                result = xwin
            elif criteria.re_obj is not None and \
                            xwin.getTitle() is not None:
                match = criteria.re_obj.search(xwin.getTitle())
                if match:
                    result = xwin
                    i = 1
                    for g in match.groups():
                        if g is not None:
                            #result = (xwin, i, match.group( i ))
                            break
                        i += 1
                    self.logger.debug("Match re: %#x - %s, pattern %d", 
                                       xwin.this_window, xwin.getTitle(), i)
                    if self.re_match.has_key(i):
                        self.logger.debug("Appending re match")
                        self.re_match[i].append(xwin)
                    else:
                        self.logger.debug("New re match")
                        self.re_match[i] = [xwin]
                    #self.re_match[i] = xwin
            #FIXME add criteria.exit_first match
            #break
        else:
            self.logger.debug("event win: %#x - %s does not match" %\
                                (xwin.this_window, \
                                xwin.getTitle()))

        if result is not None:
            self.logger.debug("result: %#x - %s" %\
                                (result.this_window, result.getTitle()))
        return result

    def expect(self, criteria=None):
        def addWindow(list, window):
            #Only return the most recent event on a window.
            if list.count(window) > 0:
                list.remove(window)

            list.append(window)

        old_logger_name = self.logger.name
        self.logger.name = "Pyxt.expect"
        result = []
        if type(criteria) is str:
            criteria = PyxtCriteria(criteria, logger=self.logger)
       
        if criteria is None and self.criteria is None:
            raise PyxtError, "No criteria for expect call"

        self.criteria = criteria
        end_time = criteria.getEndTime()
        criteria.reset()
        rejects = []
        while criteria.hasTrials():
            timeout = end_time - time.time()
            if timeout < 0:
                timeout = 0

            event_win = self.xhash.getEvent(timeout)
            if event_win is not None:
                self.logger.debug("event_win.event_type: %i, title: %s, window: %#x" % \
                                   (event_win.event_type,
                                    event_win.getTitle(),
                                    event_win.this_window ))
                
            if event_win is None:
                self.logger.debug("event_win is None")
                break
            elif event_win.timestamp > end_time:
                self.logger.debug("event_win.timestamp > end_time %#x - %s" % (\
                                    event_win.this_window, 
                                    event_win.getTitle()))
                break
            else:
                self.logger.debug("event_win: %#x - %s, event_type: %s" % (\
                                    event_win.this_window, 
                                    event_win.getTitle(), 
                                    event_win.event_type))

                if criteria.test(event_win):
                    addWindow(result, event_win)
                    #result.append(event_win)
                    self.logger.debug("win matched: %#x - %s" % (\
                                event_win.this_window, event_win.getTitle()))

                    new_end_time = event_win.timestamp + self.WAIT_FOR_WINDOWS
                    if new_end_time < end_time:
                        end_time = new_end_time
                else:
                    #rejects.append(event_win)
                    addWindow(rejects, event_win)

        time.sleep(.2)
        criteria.validateMatches()
        # A hack since some apps change their window title after creating it.
        for rejected in rejects:
            if rejected.isValid():
                if criteria.test(rejected):
                    #result.append(rejected)
                    addWindow(result, rejected)

        if not criteria.hasMatch() and criteria.hasTrials():
            self.logger.error("expect timed out")
            self.logger.name = old_logger_name
            #if criteria.raise_timeout:
            raise PyxtError, "Timeout waiting for %s" % criteria

        self.logger.name = old_logger_name
        return result
        
    def search(self, criteria):
        old_logger_name = self.logger.name
        self.logger.name = "Pyxt.search"
        #result = findXWindows( criteria.re_obj, criteria.match_xwindow ) 
        if type(criteria) == str:
            #result = self.xhash.getXWindows(criteria)
            criteria = PyxtCriteria(criteria)

        result = []
        for win in self.xhash.getXWindows():
            if criteria.test(win):
                result.append(win)

        self.logger.debug( "result: %s", result )
        self.logger.name = old_logger_name
        return result

class XHash(threading.Thread):
    __name__ = "XHash"
    timeout = 9
    DEFAULT_TIMEOUT = 9
    default_sleep = 1
    queue_max = 300
    wait_time = .02

    def __init__(self, display_string=None, logger=None, debug_level=0):
        if logger is not None:
            self.logger = logger
            old_logger_name = self.logger.name
            self.logger.name = "XHash.__init__"
        else:
            self.logger = logging.getLogger( "XHash.__init__" )
            old_logger_name = self.logger.name
            self.logger.setLevel( 30 - debug_level * 10 )
            handler = logging.StreamHandler()
            formatter = logging.Formatter( "\n%(name)s() - %(filename)s:%(lineno)s\n %(message)s" )
            handler.setFormatter( formatter )
            self.logger.addHandler( handler )
        
        self.default_timeout = XHash.timeout
        self.default_sleep = XHash.default_sleep
        self.display_string = display_string
        
        self.xwindows = {}
        #FUTURE
        #self.title_dict = {}
        self.xevent_queue = Queue.Queue( XHash.queue_max )
        self.xwindows_lock = threading.RLock()
        #self.xevent = threading.Event()

        self.xdisplay = None
        self.end = False
        self.window_manager = None
        self.win_manager_re = re.compile('metacity')
        try:
            self.xdisplay = _pyltfx.XDisplay( display_string )
            self.logger.debug( "Opened display: %s", self.xdisplay.xdisplay_string )
            #self.display_string = self.xdisplay.xdisplay_string
        except: 
            self.logger.error( "Error open in display: %s", display_string )

        self.addXWindowTree(self.xdisplay.root_xwindow)
        threading.Thread.__init__( self )
        self.setName( "XHashThread")
        self.logger.name = old_logger_name

    def die(self):
        self.end = True 

    def run(self):
        old_logger_name = self.logger.name
        self.logger.name = "XHash.run" 
        self.logger.info( "XHash thread started" )
        while not self.end:
            xwindow_list = self.xdisplay.checkXEvent()    
            for xwin in xwindow_list:
                old_logger_name = self.logger.name
                self.logger.name = "XHash.run" 
                self.logger.debug( "Processing XEvent xwindow: %#x, title: %s", 
                                    xwin.this_window,
                                    xwin.getTitle() )
                self.processXWindow( xwin )
                self.logger.name = old_logger_name
                if self.end:
                    self.logger.debug( "breaking out of for loop" )
                    break
            #time.sleep( self.default_sleep )
        self.logger.name = "XHash.run" 
        self.logger.info( "Main xhash loop done" )
        self.logger.name = old_logger_name
   
    def addXWindowTree( self, xwindow ):
        old_logger_name = self.logger.name
        self.logger.name = "XHash.addXWindowTree"
        self.logger.debug( "Adding xwindow: %#x - %s\n parent: %#x", 
                            xwindow.this_window,
                            xwindow.getTitle(),
                            xwindow.parent_window )
        xwindow_list = xwindow.getTree()
        self.xwindows_lock.acquire()
        self.logger.info( "Acquired xwindows_lock for window: %#x", 
                           xwindow.this_window)
        for xwindow in xwindow_list:
            if xwindow.isValid() or xwindow.isNew():
                self.xwindows[xwindow] = xwindow
            #self.processXWindow( xwindow )
        
        self.xwindows_lock.release()
        self.logger.info( "released xwindows_lock for window: %#x", 
                            xwindow.this_window)
        self.logger.name = old_logger_name
    
    def processXWindow( self, xwindow ):
        old_logger_name = self.logger.name
        self.logger.name = "XHash.processXWindow"
        self.logger.info( "xwindow: %#x - %s", xwindow.this_window, \
                                               xwindow.getTitle() )
        try:
            #FIXME add __hash__ function to xwindow object
            #key = createKey( xwindow )
            #self.logger.debug( "Trying to acquire xwindows_lock for window: %#x", 
            #                    xwindow.this_window)
            self.xwindows_lock.acquire()
            #self.logger.info( "Acquired xwindows_lock for window: %#x", 
            #                   xwindow.this_window)
            if self.window_manager is None and \
                     self.win_manager_re.search(xwindow.getTitle()):
                self.window_manager = xwindow
                
            if self.xwindows.has_key(xwindow):
                if xwindow.isDestroyed():
                    #tmp_xwindow = self.xwindows.pop( xwindow )
                    #xwindow.window_title = tmp_xwindow.getTitle()
                    xwindow.window_title = self.xwindows.pop(xwindow).getTitle()
                    self.logger.debug("Removed window: %s - %#x", 
                                       xwindow.getTitle(), 
                                       xwindow.this_window)
                    #self.xevent.set()
                    #FIXME time.sleep( XHash.wait_time )
                    #self.xwin_cv.wait( XHash.wait_time )
                else:
                    self.logger.debug( "Event for existing window: %s - %#x", 
                                        xwindow.getTitle(), 
                                        xwindow.this_window )
                    self.xwindows[xwindow] = xwindow
                    #self.logger.debug( "Existing xwindow %#x", xwindow.this_window )
                    #FIXME report other window events?
                    #self.logger.info( "Already have window %s - %#x", 
                                       #xwindow.getTitle(), 
                                       #xwindow.this_window )
            else:
                #self.logger.debug( "New xwindow: %#x", xwindow.this_window )
                #if xwindow.isValid() or xwindow.isNew():
                self.logger.debug( "New window: %s - %#x", 
                                    xwindow.getTitle(), 
                                    xwindow.this_window )
                self.xwindows[xwindow] = xwindow
                #self.xevent_queue.put( xwindow, True, XHash.timeout )
                    #self.xevent.set()
                    #FIXME time.sleep( XHash.wait_time )
                    #self.xevent_cv.notifyAll()
                    #self.xevent_cv.wait( .01 )
                    #FUTURE
                    #if self.title_dict.has_key( xwindow.getTitle() ):
                    #    self.title_dict[xwindow.getTitle()].append( xwindow )
                    #else:
                    #    self.title_dict[xwindow.getTitle()] = [xwindow]
                
                #else:
                    #self.logger.debug( "Window not Valid and not New: %s - %#x",
                                        #xwindow.getTitle(), 
                                        #xwindow.this_window )
            self.xevent_queue.put(xwindow, True, XHash.timeout)
        except Exception, err:
            self.logger.info( "Error processing window %s - %#x\n %s", 
                               xwindow.getTitle(), 
                               xwindow.this_window,
                               err )
            
        self.xwindows_lock.release()
        #self.logger.info( "released xwindows_lock for window: %#x", 
        #                    xwindow.this_window)

        self.logger.name = old_logger_name

    def getEvent(self, get_timeout=None):
        if get_timeout is None:
            get_timeout = self.DEFAULT_TIMEOUT
        
        event_xwindow = None
        try:
            event_xwindow = self.xevent_queue.get(timeout=get_timeout)
        except Queue.Empty:
            self.logger.info("xevent_queue.get timed out")
        else:
            self.logger.debug( "xwindow from xevent_queue: %s - %#x", 
                                event_xwindow.getTitle(), 
                                event_xwindow.this_window )
        
        return event_xwindow

    def getXWindows(self, filter=None):
        self.logger.name = "XHash.processXWindow"
        self.xwindows_lock.acquire()
        self.logger.info( "Acquired xwindows_lock for")
        if filter is None:
            result = self.xwindows.values()
        else:
            result = []
            regexpr = re.compile(filter)
            for xwindow in self.xwindows.itervalues():
                if xwindow.getTitle() is not None:
                    if regexpr.search(xwindow.getTitle()):
                        result.append(xwindow)

        self.xwindows_lock.release()
        self.logger.info( "released xwindows_lock.")
        return result
