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

sys.path.append( os.path.realpath( "." ) )
try:
    import pyxt
except ImportError:
    sys.path.append(os.path.realpath( "." ))
    sys.path.append(os.path.realpath("../rpms/BUILD/pyxt-1.0/build/lib.linux-i686-2.5/"))
    import pyxt

class TestXWindow( unittest.TestCase ):
    debug_level = 2
    logger = None
    def setUp( self ):
        if TestXWindow.logger is None:
            self.logger = logging.getLogger( "TestXWindow.setUp" )
            self.logger.setLevel( 30 - TestXWindow.debug_level * 10 )
            handler = logging.StreamHandler()
            formatter = logging.Formatter( "%(name)s() - %(filename)s:%(lineno)s\n %(message)s" )
            handler.setFormatter( formatter )
            self.logger.addHandler( handler )
        else:
            self.logger = TestXWindow.logger
        
        self.xdisplay = pyxt.XDisplay()

    def tearDown( self ):
        pass

    def test_isValid( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXDisplay.test_isValid"
        #d = pyxt.XDisplay( ":0" )
        w = self.xdisplay.getActiveXWindow()
        self.assert_( w.isValid() )
        self.logger.name = old_logger_name

    def test_init_string( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXWindow.test_XDisplay"
        d = pyxt.XDisplay( ":0" )
        self.assertEqual( d.xdisplay_string, ":0" )
        self.logger.name = old_logger_name
        
    def test_init_no_string( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXDisplay.test_XDisplay"
        d = pyxt.XDisplay()
        self.assertEqual( d.xdisplay_string, ":0" )
        self.logger.name = old_logger_name
        
    def test_getActiveXWindow( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXDisplay.test_getActiveXWindow"
        d = pyxt.XDisplay()
        w = d.getActiveXWindow()
        self.assertEqual( w.window_title, "Terminal" )
        self.logger.name = old_logger_name
    
    def test_getRootXWindow( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXDisplay.test_getRootXWindow"
        d = pyxt.XDisplay()
        w = d.getRootXWindow()
        self.assertEqual( w.window_title, "" )
        self.logger.name = old_logger_name

    def test_type( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestXDisplay.test_type"
        d = pyxt.XDisplay()
        w = d.getActiveXWindow()
        w.type( "a" )
        self.logger.name = old_logger_name

def main( args ):
    sys.path.append( os.path.realpath( "." ) )
    import pyxt
    base_name = os.path.splitext( os.path.basename(sys.argv[0]) )[0]
    usage = "usage: %prog -t TEST_CASE"
    parser = optparse.OptionParser( usage=usage )
    parser.add_option("-t", "--test", dest="test_case_list", default=[],
                       help="Test case", metavar="TEST_CASE", action="append" )
    parser.add_option("-v", "--verbose",
                       action="count", dest="debug_level", default=0,
                        help="Increase verbosity of debug output")
    (options,args) = parser.parse_args()
   
    TestXWindow.debug_level = options.debug_level
    if len( options.test_case_list ) == 0:
        unittest.main()
    else:
        mainTestSuite = unittest.TestSuite()
        for test_case in options.test_case_list:
            mainTestSuite.addTest(TestXWindow( test_case ) )
        
        unittest.TextTestRunner(verbosity=2).run( mainTestSuite )
                                                                    
    #suite = unittest.makeSuite(TestFilePropDiffDict)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()

if __name__ == '__main__':
    main( sys.argv[1:] )

