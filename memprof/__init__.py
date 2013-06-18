from .memprof import *
import pkg_resources

__version__ = pkg_resources.require("memprof")[0].version
