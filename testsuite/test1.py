# Copyright (c) 2013 Javi Merino
#
# This file is part of memprof.
#
# memprof is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation (version 3 of the License only).
#
# memprof is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with memprof.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import os
import sys

sys.path.insert(0, "../memprof")
from memprof import memprof

class Test(unittest.TestCase):
    # Rough test: just run the example
    def test_demo(self):
        root = os.getcwd()
        examples_path = os.path.join(os.getcwd(), "examples")
        sys.path.append(examples_path)
        os.chdir(examples_path)
        import demo
        os.chdir(root)

    def test_class(self):
        """memprof works with classes"""
        MB = 1024 * 1024

        @memprof
        class FooClass(object):
            def __init__(self):
                self.a = [1] * MB
                self.b = [1] * MB * 2

            def append(self, limit=500000):
                for _ in range(limit):
                    self.a.append(1)
                    self.b.append(1)

        foo = FooClass()
        foo.append()
