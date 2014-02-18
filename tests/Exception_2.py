# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#

import unittest

import lsst.pex.exceptions
import failer

class ExceptionTestCase(unittest.TestCase):
    """A test case for C++/Python LsstCppExceptions."""
    def setUp(self):
        """Create a wrapped C++ instance that throws an exception."""
        self.x = failer.Failer()

    def tearDown(self):
        del self.x

    def testHierarchy(self):
        """Check that the LsstCppException class hierarchy is correct and that
        the C++ exception is a subclass of lsst.pex.exceptions.Exception."""
        self.assert_(issubclass(lsst.pex.exceptions.LsstException, Exception))
        self.assert_(issubclass(lsst.pex.exceptions.LsstCppException,
            lsst.pex.exceptions.LsstException))
        self.assert_(issubclass(failer.MyException,
            lsst.pex.exceptions.Exception))

    def testThrow(self):
        """Check that the exception thrown is a Python Exception, an
        LsstException, and an LsstCppException."""
        self.assertRaises(Exception, self.x.fail)
        self.assertRaises(lsst.pex.exceptions.LsstException, self.x.fail)
        self.assertRaises(lsst.pex.exceptions.LsstCppException, self.x.fail)

    def testValue(self):
        """Check that the exception value is a proper SWIGged C++ exception
        with appropriate message."""
        try:
            self.x.fail()
        except Exception, e:
            self.assert_(e is not None)
            self.assertEqual(len(e.args), 1)
            self.assert_(isinstance(e, Exception))
            self.assert_(isinstance(e, lsst.pex.exceptions.LsstException))
            self.assert_(isinstance(e, lsst.pex.exceptions.LsstCppException))
            self.assert_(isinstance(e.args[0], lsst.pex.exceptions.Exception))
            self.assert_(isinstance(e.args[0], failer.MyException))
            self.assertEqual(e.args[0].what(),
                    "0: failer::MyException thrown at tests/Failer.cc:29 " +
                    "in void failer::Failer::fail()\n0: Message: message\n")
            self.assertEqual(str(e),
                    "0: failer::MyException thrown at tests/Failer.cc:29 " +
                    "in void failer::Failer::fail()\n0: Message: message\n")
            self.assertEqual(e.args[0].getType(), "failer::MyException *")

    def testTraceback(self):
        """Check that the traceback is accessible and correct."""
        try:
            self.x.fail()
        except lsst.pex.exceptions.LsstCppException, e:
            t = e.args[0].getTraceback()
            self.assert_(len(t), 1)
            self.assert_(isinstance(t[0], lsst.pex.exceptions.Tracepoint))
            self.assertEqual(t[0]._file, "tests/Failer.cc")
            self.assertEqual(t[0]._line, 29)
            self.assertEqual(t[0]._func, "void failer::Failer::fail()")
            self.assertEqual(t[0]._msg, "message")

    def testAssertEqual(self):
        """Test that the LSST_ASSERT_EQUAL macro works as expected"""
        try:
            self.x.fail3(4, 5)
        except lsst.pex.exceptions.LsstCppException as e:
            self.assert_("a=4" in str(e))
            self.assert_("b=5" in str(e))
            self.assert_(isinstance(e.args[0], lsst.pex.exceptions.RuntimeErrorException))

if __name__ == '__main__':
    unittest.main()
