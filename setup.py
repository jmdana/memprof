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
from setuptools import setup, Extension
import sys
from distutils.command.install_scripts import install_scripts
from Cython.Distutils import build_ext

getsize = Extension('memprof.getsize',
    sources = ['memprof/getsize.pyx'])

install_scripts_dest = "%s/bin" % sys.prefix

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

class md_install_scripts(install_scripts):
  def run(self):
    global install_scripts_dest
    
    install_scripts.run(self)

    if "install" in self.distribution.command_options and 'install_scripts' in self.distribution.command_options['install']:
      install_scripts_dest = self.distribution.command_options['install']['install_scripts'][1]
      

setup(
  name = "memprof",
  version = "0.3",
  author = "Jose M. Dana",
  description = ("A memory profiler for Python. As easy as adding a decorator."),
  license = "GNU General Public License v3 (GPLv3)",
  keywords = "memory usage profiler decorator variables charts plots graphical",
  url = "http://jmdana.github.io/memprof/",
  packages=['memprof'],
  scripts=['scripts/mp_plot'],
  cmdclass = {'install_scripts': md_install_scripts, 'build_ext': build_ext},
  zip_safe=False,
  long_description=read('README.md'),
  classifiers=[
      "Development Status :: 4 - Beta",
      "Topic :: Utilities",
      "Topic :: Software Development",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 2.6",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.1",
      "Programming Language :: Python :: 3.2",
      "Programming Language :: Python :: 3.3",
      "Operating System :: Unix",
      "Operating System :: MacOS",
      "Operating System :: POSIX",
      "Intended Audience :: Developers",
      "Intended Audience :: Information Technology",
      "Intended Audience :: Science/Research",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  ],
  ext_modules=[getsize],
  requires=['argparse','matplotlib','cython'],
  install_requires=['argparse','matplotlib','cython'],
  provides=['memprof'],
)

print("\n\n")
print("*" * 80)
print("mp_plot has been copied to:\n\n%s\n\nPlease make sure that it is included in your PATH." % install_scripts_dest)
print("*" * 80)
print("\n\n")

