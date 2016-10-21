#!/usr/bin/env python

# Copyright (c) 2013 Jose M. Dana
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

from memprof import memprof
import time

MB = 1024 * 1024


class FooClass(object):
    def __init__(self):
        self.a = [1] * MB
        self.b = [1] * MB * 2


@memprof
def bar(limit=10000):
    bar_a = [1] * MB * 10

    for i in range(limit):
        bar_a.append(1)


@memprof
def foo2():
    a = [1] * MB      # noqa
    b = [1] * MB * 2  # noqa
    c = [1] * MB * 3  # noqa


@memprof
def foo(limit=500000):
    a = []
    b = []
    c = [1] * MB

    for i in range(limit):
        a.append(1)
        b.append(1)
        b.append(1)

        if i == limit / 2:
            del a[:]
            del c[:]
        elif i == (limit * 3) / 4:
            c = [1] * MB * 2


@memprof
def fooObject(limit=500000):
    a = FooClass()

    for i in range(limit):
        a.a.append(1)
        a.b.append(1)


foo()
time.sleep(2)
foo(500000 * 2)
bar()
foo2()
fooObject()
