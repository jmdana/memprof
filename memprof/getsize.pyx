
import types
import io
import memprof
from .mp_utils import *

if PY3:
  builtin = (int,float,str,complex)
else:
  builtin = (int,float,str,long,complex)


def isInteresting(x):
  if isinstance(x,(types.ModuleType,types.FunctionType,types.LambdaType,io.IOBase,type(None),memprof.MemProf,types.MethodType,types.GetSetDescriptorType,types.GeneratorType,types.BuiltinFunctionType,types.BuiltinMethodType)) or x in builtin:
    return False
  return True

def getSize(x):    
  ids = set()

  def size_of(x):
    if id(x) in ids:
      return 0
      
    ids.add(id(x))

    try:
      nbytes = x.nbytes
      return nbytes if isinstance(nbytes,int) else 0
    except:
      size = sys.getsizeof(x)

    if isinstance(x,builtin):
      return size

    items = []
  
    # Go through objects (avoiding modules, MemProf, functions and methods thanks to isInteresting)
    if isinstance(x,object) and hasattr(x,"__dict__"):
      items = x.__dict__.values()
    elif isinstance(x,dict):
      items = x.values()
    # Go through iterables skipping strings (and files, thanks to isInteresting)
    elif hasattr(x, '__iter__'):
      items = x
    
      
    for it in items:
      if not isinstance(it,builtin) and isInteresting(it):
        size += size_of(it)
                    
    return size
  return size_of(x)