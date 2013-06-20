import os
from setuptools import setup
import sys
from distutils.command.install_scripts import install_scripts

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
  version = "0.2.1",
  author = "Jose M. Dana",
  description = ("A memory profiler for Python. As easy as adding a decorator."),
  license = "GNU General Public License v3 (GPLv3)",
  keywords = "memory usage profiler decorator variables charts plots graphical",
  url = "http://jmdana.github.io/memprof/",
  packages=['memprof'],
  scripts=['scripts/mp_plot.py'],
  cmdclass = {'install_scripts': md_install_scripts},
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
  requires=['argparse','matplotlib'],
  install_requires=['argparse','matplotlib'],
  provides=['memprof'],
)

print("\n\n")
print("*" * 80)
print("mp_plot.py has been copied to:\n\n%s\n\nPlease make sure that it is included in your PATH." % install_scripts_dest)
print("*" * 80)
print("\n\n")

