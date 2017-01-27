#!/usr/bin/python
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

import os
import sys
import logging
import unittest
import pdb
import time
import re
import optparse
import popen2

try:
    import pyxt
except ImportError:
    sys.path.append(os.path.realpath( "." ))
    sys.path.append(os.path.realpath("../rpms/BUILD/pyxt-1.0/build/lib.linux-i686-2.5/"))
    import pyxt


class TestXHash( unittest.TestCase ):
    debug_level = 2
    logger = None
    def setUp( self ):
        if TestXHash.logger is None:
            self.logger = logging.getLogger( "TestXHash.setUp" )
            self.logger.setLevel( 30 - TestXHash.debug_level * 10 )
            handler = logging.StreamHandler()
            formatter = logging.Formatter( "%(name)s() - %(filename)s:%(lineno)s\n %(message)s" )
            handler.setFormatter( formatter )
            self.logger.addHandler( handler )
        else:
            self.logger = TestXHash.logger
        
        self.xhash = pyxt.XHash( logger=self.logger )
        self.xhash.start()
        time.sleep( 3 )
        
    def tearDown( self ):
        self.xhash.end = True
        self.xhash.join( 2 )
        del( self.xhash )

    def test_init( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_init"
        time.sleep( 1 )
        self.assert_( len( self.xhash.xwindows ) > 2 )
        self.logger.name = old_logger_name

    def test_new( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_init"
        len_before = len( self.xhash.xwindows )
        p = popen2.Popen4( "/usr/X11R6/bin/xlogo" )
        time.sleep( 1 )
        len_during = len( self.xhash.xwindows )
        self.assert_( len_during != len_before )
        self.assert_( not self.xhash.xevent_queue.empty() )
        os.kill( p.pid,9 )
        time.sleep( 1 )
        self.assertNotEqual( len( self.xhash.xwindows ), len_during )
        self.logger.name = old_logger_name

    def test_getEventList( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_checkXEvent"
        p = popen2.Popen4( "sleep 1;/usr/X11R6/bin/xlogo" )
        wlist = self.xhash.getEventList() 
        self.logger.info( "getNextEvent returned: %s", wlist )
        found_window = False
        for w in wlist:
            if w.window_title == "xlogo":
                found_window = True
        self.assert_( found_window )
        (pout,pin) = popen2.popen4( "ps --ppid %s -o pid=" % p.pid )
        pids = pout.readlines()
        cmd = "sleep 1;kill -9 %s " % p.pid
        for pid in pids:
            cmd += "%s " % pid.strip()

        (pout,pin) = popen2.popen4( cmd )
        wlist = self.xhash.getEventList() 
        self.logger.info( "getNextEvent returned: %s", wlist )
        found_window = False
        for w in wlist:
            if w.window_title == "xlogo":
                found_window = True
        self.assert_( found_window )
        self.logger.name = old_logger_name

    def test_getEventListTimeout( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_checkXEventTimeout"
        p = popen2.Popen4( "sleep 3;/usr/X11R6/bin/xlogo" )
        wlist = self.xhash.getEventList( timeout=1 ) 
        #self.logger.info( "getNextEvent returned: %#x - %s", w.this_window, w.window_title )
        self.assertEqual( len( wlist), 0 )
        time.sleep( 3 )
        old_list = self.xhash.clearQueue()
        found_window = False
        for w in old_list:
            if w.window_title == "xlogo":
                found_window = True
        self.assert_( found_window )

        (pout,pin) = popen2.popen4( "ps --ppid %s -o pid=" % p.pid )
        pids = pout.readlines()
        cmd = "sleep 2;kill -9 %s " % p.pid
        for pid in pids:
            cmd += "%s " % pid.strip()

        (pout,pin) = popen2.popen4( cmd )
        wlist = self.xhash.getEventList( timeout=1 ) 
        self.assertEqual( len( wlist), 0 )
        
        self.logger.name = old_logger_name

    def test_getLock( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_getLock"
        self.logger.debug( "getting lock" )
        self.xhash.getLock()
        self.xhash.xwindow_lock.release()
        self.logger.name = old_logger_name

    def test_findEventXWindow( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_findEventXWindow"
        p = popen2.Popen4( "sleep 1;/usr/X11R6/bin/xlogo" )
        w = self.xhash.findEventXWindow( "xlogo" ) 
        self.logger.info( "getEventXWindow returned: %#x - %s", 
                           w.this_window, w.window_title )
        self.assertEqual( w.window_title, "xlogo" )
        
        (pout,pin) = popen2.popen4( "ps --ppid %s -o pid=" % p.pid )
        pids = pout.readlines()
        cmd = "sleep 1;kill -9 %s " % p.pid
        for pid in pids:
            cmd += "%s " % pid.strip()

        (pout,pin) = popen2.popen4( cmd )
        w = self.xhash.findEventXWindow( "xlogo" ) 
        self.logger.info( "getEventXWindow returned: %#x - %s", 
                           w.this_window, w.window_title )
        self.assertEqual( w.window_title, "xlogo" )
        self.logger.name = old_logger_name

    def test_findEventXWindowTimeout( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_findEventXWindow"
        p = popen2.Popen4( "sleep 2;/usr/X11R6/bin/xlogo" )
        w = self.xhash.findEventXWindow( "xlogo", 1 ) 
        self.assertEqual( w, None )
        time.sleep( 3 )
        old_list = self.xhash.clearEvents( 1 )
        found_window = False
        for w in old_list:
            if w.window_title == "xlogo":
                found_window = True
                break
        self.assert_( found_window )
        
        (pout,pin) = popen2.popen4( "ps --ppid %s -o pid=" % p.pid )
        pids = pout.readlines()
        cmd = "sleep 2;kill -9 %s " % p.pid
        for pid in pids:
            cmd += "%s " % pid.strip()

        (pout,pin) = popen2.popen4( cmd )

        w = self.xhash.findEventXWindow( "xlogo", 1 ) 
        self.assertEqual( w, None )
        self.logger.name = old_logger_name

    def test_findXWindowList( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXHash.test_findXWindowList"
        length = len( self.xhash.xwindows )
        l = self.xhash.findXWindowList()
        self.logger.debug( "list for all windows: %s", l )
        self.assert_( length >= len( l ) )
        l = self.xhash.findXWindowList( "aJAFasf" )
        self.logger.debug( "list for aJAFasf: %s", l )
        self.assertEqual( 0, len( l ) )
        l = self.xhash.findXWindowList( "metacity" )
        self.logger.debug( "list for metacity: %s", l )
        self.assert_( len( l ) >= 1 )
        
        self.logger.name = old_logger_name

def main( args ):
    sys.path.append( os.path.realpath( "." ) )
    base_name = os.path.splitext( os.path.basename(sys.argv[0]) )[0]
    usage = "usage: %prog -t TEST_CASE [-f FILENAME]"
    parser = optparse.OptionParser( usage=usage )
    parser.add_option("-f", "--file", dest="log_file", default=None,
                       help="Log file", metavar="FILENAME", action="store" )
    parser.add_option("-t", "--test", dest="test_case_list", default=[],
                       help="Test case", metavar="TEST_CASE", action="append" )
    parser.add_option("-v", "--verbose", action="count", dest="debug_level", 
                        default=0, help="Increase verbosity of debug output")
    (options,args) = parser.parse_args()
  
    logger = logging.getLogger( "pyxt_xhash_test" )
    logger.setLevel( 30 - options.debug_level * 10 )
    if options.log_file is None:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler( options.log_file, 'w' )

    formatter = logging.Formatter( "\n%(name)s(), %(threadName)s - %(filename)s:%(lineno)s\n %(message)s" )
    handler.setFormatter( formatter )
    logger.addHandler( handler )

    TestXHash.logger = logger
    TestXHash.debug_level = options.debug_level
    
    runner = unittest.TextTestRunner( sys.stdout, verbosity=2 )
    if len( options.test_case_list ) == 0:
        suite = unittest.makeSuite( TestXHash )
        runner.run( suite )
        #unittest.main( testRunner=runner )
    else:
        mainTestSuite = unittest.TestSuite()
        for test_case in options.test_case_list:
            mainTestSuite.addTest( TestXHash( test_case ) )
        
        #unittest.TextTestRunner(verbosity=2).run( mainTestSuite )
        runner.run( mainTestSuite )
                                                                    
    #suite = unittest.makeSuite(TestFilePropDiffDict)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()

if __name__ == '__main__':
    main( sys.argv[1:] )

