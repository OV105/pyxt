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

class TestPyxt( unittest.TestCase ):
    debug_level = 2
    logger = None
    def setUp( self ):
        if TestPyxt.logger is None:
            self.logger = logging.getLogger("TestPyxt.setUp")
            self.logger.setLevel(30 - TestPyxt.debug_level * 10)
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(name)s() - %(filename)s:%(lineno)s\n %(message)s" )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            self.logger = TestPyxt.logger
        
        self.p = pyxt.Pyxt(logger=self.logger)
        time.sleep(3)
        
    def tearDown( self ):
        self.p.die()

    def test_kill( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestPyxt.test_init"
        time.sleep(1)
        self.assert_(len(self.p.xhash.xwindows) > 2)
        self.p.die()
        self.logger.name = old_logger_name
    
    def test_criteria( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestPyxt.test_criteria"
        crit = pyxt.PyxtCriteria()
        self.assertEqual(len(crit.trials), 0)
        crit.addTrial(pyxt.event_all, "gedit")
        self.assertEqual(len(crit.trials), 1)
        self.assertEqual(crit.trials['gedit'].re_string, "gedit")
        crit = pyxt.PyxtCriteria(reg_expr=["gedit", "test"])
        self.assertEqual(len(crit.trials), 2)
        self.assertEqual(crit.trials['gedit'].re_string, "gedit")
        self.assertEqual(crit.trials['test'].re_string, "test")
        crit.addTrial(pyxt.event_all, match_xwin=123)
        self.assertEqual(len(crit.trials), 3)
        self.logger.name = old_logger_name

    def test_command( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestPyxt.test_command"
        d = pyxt.XDisplay()
        w = d.getActiveXWindow()
        cmd = pyxt.PyxtCommand(w, "abc")
        self.assertEqual(cmd.xwindow, w)
        self.assertEqual(cmd.cmd_strings[0], "abc")
        cmd.addStrings("def")
        self.assertEqual(cmd.cmd_strings[1], "def")
        self.logger.name = old_logger_name

    def test_send( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestPyxt.test_send"
        d = pyxt.XDisplay()
        p = popen2.Popen4( "zenity --info --title='test_send'" )
        time.sleep( 1 )
        w = d.getActiveXWindow()
        c = pyxt.PyxtCommand(w, pyxt.key_alt + 'o')
        self.p.send(c) 
        time.sleep(1)
        po = p.poll()
        self.assertNotEqual( po, -1 )
        self.logger.name = old_logger_name

    def test_expect( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestPyxt.test_expect"
       
        criteria = pyxt.PyxtCriteria( "test_title" )
        proc = popen2.Popen4( "zenity --info --title='test_title'" )
        rn = self.p.expect(criteria)
        self.assertEqual(rn[0].window_title, "test_title")
        time.sleep(1)
        #proc = popen2.popen4("killall -9 zenity")
        os.kill( proc.pid, 9 )
        self.logger.name = old_logger_name
        
    def test_send_expect( self ):
        old_logger_name = self.logger.name
        self.logger.name = "TestPyxt.test_send_expect"
       
        c1 = pyxt.PyxtCriteria( "test_title" )
        proc = popen2.Popen4( "zenity --info --title='test_title'" )
        time.sleep( 1 )
        r1 = self.p.expect(c1)
        self.assertEqual( r1[0].window_title, "test_title" )
        
        c2 = pyxt.PyxtCriteria(match_xwindow=r1[0],
                               event_type=pyxt.event_all) 
        cmd = pyxt.PyxtCommand(r1[0], pyxt.key_alt + 'o')
        self.p.send(cmd) 
        r2 = self.p.expect(c2)
        self.assertEqual(r1[0].this_window, r2[0].this_window)
        po = proc.poll()
        if po == -1:
            os.kill( proc.pid, 9 )
        else:
            self.assertNotEqual( po, -1 )

        time.sleep( 1 )
        self.logger.name = old_logger_name

def main( args ):
    sys.path.append( os.path.realpath( "." ) )
    base_name = os.path.splitext( os.path.basename(sys.argv[0]) )[0]
    usage = "usage: %prog -t TEST_CASE"
    parser = optparse.OptionParser( usage=usage )
    parser.add_option("-f", "--file", dest="log_file", default=None,
                       help="Log file", metavar="/PATH/FILE", action="store" )
    parser.add_option("-t", "--test", dest="test_case_list", default=[],
                       help="Test case", metavar="TEST_CASE", action="append" )
    parser.add_option("-v", "--verbose", action="count", dest="debug_level", 
                        default=0, help="Increase verbosity of debug output")
    (options,args) = parser.parse_args()
  
    logger = logging.getLogger( "pyxt_pyxt_test" )
    logger.setLevel( 30 - options.debug_level * 10 )
    if options.log_file is None:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler( options.log_file, 'w' )

    formatter = logging.Formatter( "\n%(name)s(), %(threadName)s [%(created)f] - %(filename)s:%(lineno)s\n %(message)s" )
    handler.setFormatter( formatter )
    logger.addHandler( handler )

    TestPyxt.logger = logger
    TestPyxt.debug_level = options.debug_level
    
    runner = unittest.TextTestRunner( sys.stdout, verbosity=2 )
    if len( options.test_case_list ) == 0:
        suite = unittest.makeSuite( TestPyxt )
        runner.run( suite )
    else:
        mainTestSuite = unittest.TestSuite()
        for test_case in options.test_case_list:
            mainTestSuite.addTest( TestPyxt( test_case ) )
        
        runner.run( mainTestSuite )

if __name__ == '__main__':
    main( sys.argv[1:] )

