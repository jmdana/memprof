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

import os
import sys
import operator

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa

PY3 = sys.version > '3'

KB = 1024.
MB = KB * 1024
GB = MB * 1024

default_threshold = MB


def get_units_factor(threshold):
    if threshold < KB:
        return ("B", 1.)
    elif threshold < MB:
        return ("KB", KB)
    elif threshold < GB:
        return ("MB", MB)
    else:
        return ("GB", GB)


def gen_plot(logfile, threshold):
    cache = {}
    times = []

    figure = plt.Figure()
    canvas = FigureCanvasAgg(figure)

    name = os.path.splitext(logfile)[0]

    units, factor = get_units_factor(threshold)

    ax = figure.add_subplot(1, 1, 1)
    ax.set_xlabel('time (s)')
    ax.set_ylabel('memory (%s)' % units)
    ax.set_title('%s - memprof' % (name))
    ax.grid(True)

    f = open(logfile, "r")

    for line in f:
        line = line.strip()

        try:
            item, size = line.split('\t')
            size = float(size)

            if size >= threshold:
                size /= factor
                cache.setdefault(item, []).append(size)

                if len(cache[item]) < len(times):
                    cache[item][-1:-1] = [0] * (len(times) - len(cache[item]))

        except ValueError:
            if line == "RESTART":
                ax.axvspan(times[-2], times[-1], facecolor='#000000', alpha=0.5)
                ax.axvline(x=times[-2], color='#000000')
                ax.axvline(x=times[-1], color='#000000')
            else:
                times.append(float(line))

    f.close()

    if not cache.items():
        print("\nNothing with more than %.2f %ss found!" % (threshold / factor, units))
        print("There is nothing to plot... Exiting")
        return

    for item, val in cache.items():
        # len(s) == len(t) has to be true
        s = val + [0] * (len(times) - len(val))
        ax.plot(times, s, linewidth=1.5, label=item)

    handles, labels = ax.get_legend_handles_labels()
    hl = sorted(zip(handles, labels), key=operator.itemgetter(1))
    handles, labels = zip(*hl)

    maxy = max(map(max, cache.values()))
    gapy = (maxy - threshold / factor) / 40
    ax.set_ylim(max(0, threshold / factor - gapy), maxy + gapy)

    gapx = (times[-1] - times[0]) / 40
    ax.set_xlim(times[0], times[-1] + gapx)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.15 , box.width, box.height * 0.85])
    figure.legend(handles, labels, bbox_to_anchor=(0.5, 0.13), loc="upper center", ncol=5, borderaxespad=0.0)

    canvas.print_figure("%s.png" % name)

    return figure
