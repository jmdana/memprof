#!/usr/bin/env python

from memprof.mp_utils import *

import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  parser.add_argument('-t','--threshold',type=int, default=default_threshold, action='store', help='threshold (default: %d bytes)' % default_threshold)
  parser.add_argument('logfiles', type=str, default=None, nargs='+', help='the logfiles')

  args, unknown = parser.parse_known_args()
  
  if not args.logfiles:
    parser.print_help()
    sys.exit(1)
  
  units,factor = get_units_factor(args.threshold)
  
  for logfile in args.logfiles:
    print("Processing %s with threshold = %.2f %s" % (logfile, args.threshold / factor, units))
    try:
      gen_chart(logfile,args.threshold)
    except IOError as e:
      print(e)
    
    
  
