#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: X-ray image reader
#             https://github.com/silx-kit/fabio
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Unit tests for nexus file reader
"""

from __future__ import print_function, with_statement, division, absolute_import
import unittest
import sys
import os
if __name__ == '__main__':
    import pkgutil
    __path__ = pkgutil.extend_path([os.path.dirname(__file__)], "fabio.test")
from .utilstest import UtilsTest

logger = UtilsTest.get_logger(__file__)

import numpy
from .. import nexus


class testNexus(unittest.TestCase):

    def test_nexus(self):
        "Test creation of Nexus files"
        fname = os.path.join(UtilsTest.tempdir, "nexus.h5")
        nex = nexus.Nexus(fname)
        entry = nex.new_entry("entry")
        nex.new_instrument(entry, "ID00")
        nex.new_detector("camera")
        self.assertEqual(len(nex.get_entries()), 2, "nexus file has 2 entries")
        nex.close()
        self.assertTrue(os.path.exists(fname))
        os.unlink(fname)

    def test_from_time(self):
        """"""
        fname = os.path.join(UtilsTest.tempdir, "nexus.h5")
        nex = nexus.Nexus(fname)
        entry = nex.new_entry("entry")
        time1 = nexus.from_isotime(entry["start_time"].value)
        entry["bad_time"] = [entry["start_time"].value]  #this is a list !!!
        time2 = nexus.from_isotime(entry["bad_time"].value)
        self.assertEqual(time1, time2, "start_time in list does not works !")
        nex.close()
        self.assertTrue(os.path.exists(fname))
        os.unlink(fname)


def suite():
    testsuite = unittest.TestSuite()
    if nexus.h5py is None:
        logger.warning("h5py library is not available. Skipping Nexus test")
    else:
        testsuite.addTest(testNexus("test_nexus"))
        testsuite.addTest(testNexus("test_from_time"))
#         testsuite.addTest(testNexus("test_invert"))
    return testsuite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

