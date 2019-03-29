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
from setuptools import setup, Extension
from setuptools.command.easy_install import easy_install

try:
    from Cython.Distutils import build_ext
except ImportError:
    from setuptools.command import easy_install as easy_install_module  # noqa
    import pkg_resources
    # Install cython
    easy_install_module.main(["Cython"])
    pkg_resources.require("Cython")
    from Cython.Distutils import build_ext

getsize = Extension(
    'memprof.getsize',
    sources=['memprof/getsize.pyx']
)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class md_easy_install(easy_install):

    def run(self):
        easy_install.run(self)
        install_scripts_dest = list(filter(lambda x: x.endswith(
            "mp_plot") and "EGG-INFO" not in x, self.outputs))
        install_scripts_dest = os.path.dirname(install_scripts_dest[0]) if len(
            install_scripts_dest) else os.path.join(sys.prefix, "bin")

        if install_scripts_dest not in os.environ["PATH"]:
            print("\n\n")
            print("*" * 80)
            print("mp_plot has been copied to:\n\n%s\n" % install_scripts_dest)
            print("Which is NOT in your PATH! Please modify your PATH conveniently.")
            print("*" * 80)
            print("\n\n")


setup(
    name="memprof",
    version="0.3.5",
    author="Jose M. Dana",
    description="A memory profiler for Python. As easy as adding a decorator.",
    license="GNU General Public License v3 (GPLv3)",
    keywords="memory usage profiler decorator variables charts plots graphical",
    url="http://jmdana.github.io/memprof/",
    packages=['memprof'],
    scripts=['scripts/mp_plot'],
    cmdclass={'easy_install': md_easy_install, 'build_ext': build_ext},
    zip_safe=False,
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
    requires=['argparse', 'matplotlib', 'cython'],
    install_requires=['argparse', 'matplotlib', 'cython'],
    provides=['memprof'],
    test_suite="testsuite",
)
