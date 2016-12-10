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

import sys
import time
import argparse
import types

from .mp_utils import *  # noqa
from .getsize import getSize, isInteresting


def memprof(*args, **kwargs):
    def inner(func):
        return MemProf(func, *args, **kwargs)

    # To allow @memprof with parameters
    if len(args) and callable(args[0]):
        func = args[0]
        args = args[1:]
        return inner(func)
    else:
        return inner


class MemProf(object):
    def __init__(self, func, threshold=default_threshold, plot=False):
        self.func = func
        self.__locals = {}
        self.__start = -1
        self.__prev = -1
        self.__cache = {}
        self.__refresh = 500000
        self.__ticks = 0
        self.__checkTimes = []
        self.__logfile = "%s.log" % self.func.__name__

        self.__plot = self.func.__globals__["memprof_plot"] if "memprof_plot" in self.func.__globals__ else plot
        self.threshold = self.func.__globals__["memprof_threshold"] if "memprof_threshold" in self.func.__globals__ else threshold

        self.__units, self.__factor = get_units_factor(self.threshold)

        self.__log = None

    def __get__(self, obj, type=None):
        if obj is None:
            func = self.func
            if not hasattr(func, "__call__"):
                self.func = func.__get__(None, ownerClass)
                return self
        else:
            # Return a wrapper that binds self as a method of obj (!)
            return types.MethodType(self, obj)

    def tracer(self, frame, event, arg):
        if event not in ["line", "call", "return"]:
            return

        self.__ticks += 1

        if (event in ["call", "return"] and frame.f_code.co_name == self.func.__name__) or self.__ticks >= self.__refresh:
            self.__ticks = 0
            self.__locals = dict(list(frame.f_locals.items()) + list(frame.f_globals.items()))

            self.__locals.pop('__builtins__', None)
            self.__locals.pop('__loader__', None)
            self.__locals.pop('__cached__', None)
            self.__locals.pop('__package__', None)
            self.__locals.pop('__doc__', None)
            self.__locals.pop('__name__', None)
            self.__locals.pop('__file__', None)
            self.checkMem()

        return self.tracer

    def checkMem(self):
        now = time.time()

        self.__prev, elapsed = now, now - self.__prev
        from_start = now - self.__start

        print("\n")
        print("*" * 12)
        print("%ds (+%ds)" % (from_start, elapsed))
        print("*" * 12)

        self.__checkTimes.append(from_start)

        self.__log.write("%f\n" % from_start)

        for item, value in filter(lambda x: (x[1] is not self.__class__) and isInteresting(x[1]), self.__locals.items()):
            size = getSize(value)

            self.__log.write("%s\t%d\n" % (item, size))

            if size > self.threshold:
                size /= self.__factor

                try:
                    prev = self.__cache[item][-1]
                except (IndexError, KeyError):
                    prev = 0

                self.__cache.setdefault(item, []).append(size)

                if len(self.__cache[item]) < len(self.__checkTimes):
                    self.__cache[item][-1:-1] = [0] * (len(self.__checkTimes) - len(self.__cache[item]))

                print("%s: %.2f %s%s" % (item, size, self.__units, "\t(%s%.2f %s)" % ("+" if size - prev > 0 else "", size - prev, self.__units) if prev > 0 else ""))

    def __call__(self, *args, **kwargs):
        print("memprof starting (min. size: %d)" % (self.threshold))

        if self.__start == -1:
            self.__prev = self.__start = time.time()
            self.__log = open(self.__logfile, "w")
        else:
            self.__log = open(self.__logfile, "a")

            self.__checkTimes.append(self.__prev - self.__start + 0.00000001)
            self.__log.write("%f\n" % (self.__prev - self.__start + 0.00000001))

            self.__checkTimes.append(time.time() - self.__start)
            self.__log.write("%f\n" % (time.time() - self.__start))

            self.__log.write("RESTART\n")

            for key in self.__cache.keys():
                self.__cache[key].append(0)
                self.__cache[key].append(0)

        curr_tracer = sys.gettrace()
        sys.settrace(self.tracer)

        res = self.func(*args, **kwargs)

        sys.settrace(curr_tracer)

        self.__log.close()
        self.__ticks = 0

        if self.__plot:
            gen_plot(self.__logfile, self.threshold)

        print("memprof done")

        return res


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--threshold', type=int, default=default_threshold, action='store', help='threshold (default: %d bytes)' % default_threshold)
    parser.add_argument('-p', '--plot', action='store_true', default=False, help='Generate plots (default: False)')

    args, unknown = parser.parse_known_args()

    sys.argv = unknown

    if sys.argv == []:
        parser.print_help()
        sys.exit(1)

    __file__ = sys.argv[0]

    ns_globals = {}
    ns_globals["memprof_plot"] = args.plot
    ns_globals["memprof_threshold"] = args.threshold

    if PY3:
        with open(__file__) as f:
            code = compile(f.read(), __file__, 'exec')
            exec(code, ns_globals)
    else:
        execfile(__file__, ns_globals)

if __name__ == '__main__':
    main()
