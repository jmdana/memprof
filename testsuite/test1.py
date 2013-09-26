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

class Test(unittest.TestCase):
  # Rough test: just run the example
  def test_demo(self):
    root = os.getcwd()
    examples_path = os.path.join(os.getcwd(), "examples")
    sys.path.append(examples_path)
    os.chdir(examples_path)
    import demo
    os.chdir(root)
