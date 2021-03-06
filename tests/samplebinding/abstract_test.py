#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Shiboken Python Bindings Generator project.
#
# Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation. Please
# review the following information to ensure the GNU Lesser General
# Public License version 2.1 requirements will be met:
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
# #
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

'''Test cases for Abstract class'''

import sys
import unittest

from sample import Abstract

class Incomplete(Abstract):
    def __init__(self):
        Abstract.__init__(self)

class Concrete(Abstract):
    def __init__(self):
        Abstract.__init__(self)
        self.pure_virtual_called = False
        self.unpure_virtual_called = False

    def pureVirtual(self):
        self.pure_virtual_called = True

    def pureVirtualReturningVoidPtr(self):
        return 42

    def unpureVirtual(self):
        self.unpure_virtual_called = True

    def virtualGettingAEnum(self, enum):
        self.virtual_getting_enum = True


class AbstractTest(unittest.TestCase):
    '''Test case for Abstract class'''

    def testAbstractPureVirtualMethodAvailability(self):
        '''Test if Abstract class pure virtual method was properly wrapped.'''
        self.assert_('pureVirtual' in dir(Abstract))

    def testAbstractInstanciation(self):
        '''Test if instanciation of an abstract class raises the correct exception.'''
        self.assertRaises(NotImplementedError, Abstract)

    def testUnimplementedPureVirtualMethodCall(self):
        '''Test if calling a pure virtual method raises the correct exception.'''
        i = Incomplete()
        self.assertRaises(NotImplementedError, i.pureVirtual)

    def testPureVirtualReturningVoidPtrReturnValue(self):
        '''Test if a pure virtual method returning void ptr can be properly reimplemented'''
        # Note that the semantics of reimplementing the pure virtual method in
        # Python and calling it from C++ is undefined until it's decided how to
        # cast the Python data types to void pointers
        c = Concrete()
        self.assertEqual(c.pureVirtualReturningVoidPtr(),42)

    def testReimplementedVirtualMethodCall(self):
        '''Test if instanciation of an abstract class raises the correct exception.'''
        i = Concrete()
        self.assertRaises(NotImplementedError, i.callPureVirtual)

    def testReimplementedVirtualMethodCall(self):
        '''Test if a Python override of a virtual method is correctly called from C++.'''
        c = Concrete()
        c.callUnpureVirtual()
        self.assert_(c.unpure_virtual_called)

    def testImplementedPureVirtualMethodCall(self):
        '''Test if a Python override of a pure virtual method is correctly called from C++.'''
        c = Concrete()
        c.callPureVirtual()
        self.assert_(c.pure_virtual_called)

    def testEnumParameterOnVirtualMethodCall(self):
        '''testEnumParameterOnVirtualMethodCall'''
        c = Concrete()
        c.callVirtualGettingEnum(Abstract.Short)
        self.assert_(c.virtual_getting_enum)

if __name__ == '__main__':
    unittest.main()

