
import os
import sys
import operator

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PY3 = sys.version > '3'

KB = 1024.
MB = KB * 1024
GB = MB * 1024 

default_threshold = MB

def get_units_factor(threshold):  
  if threshold < KB:
    return ("B",1.)
  elif threshold < MB:
    return ("KB",KB)
  elif threshold < GB:
    return ("MB",MB)
  else:
    return ("GB",GB)
    
def gen_chart(logfile, threshold):
  cache = {}
  times = []
  
  name = os.path.splitext(logfile)[0]
  
  units,factor = get_units_factor(threshold)

  plt.close()
    
  ax = plt.subplot(1,1,1)  
  ax.set_xlabel('time (s)')
  ax.set_ylabel('memory (%s)' % units)
  ax.set_title('%s - memprof' % (name))
  ax.grid(True)
    
  f = open(logfile,"r")
  
  for line in f:
    line = line.strip()
    
    try:
      item,size = line.split('\t')
      size = float(size)
      
      if size >= threshold:
        size /= factor
        cache.setdefault(item,[]).append(size)        
      
        if len(cache[item]) < len(times):
          cache[item][-1:-1] = [0] * (len(times) - len(cache[item]))  
        
    except ValueError as e:
      if line == "RESTART":
        ax.axvspan(times[-2],times[-1], facecolor='#000000', alpha=0.5)
        ax.axvline(x=times[-2],color='#000000')
        ax.axvline(x=times[-1],color='#000000')
      else:
        times.append(float(line))
        
  f.close()
  
  for item,val in cache.items():
    # len(s) == len(t) has to be true
    s = val + [0] * (len(times) - len(val))
    ax.plot(times,s,linewidth = 1.5, label = item)

  handles, labels = ax.get_legend_handles_labels()
  hl = sorted(zip(handles, labels),key=operator.itemgetter(1))
  handles, labels = zip(*hl)

  plt.legend(handles,labels)
  
  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
  plt.legend(bbox_to_anchor=(0.5,-0.12), loc="upper center", ncol=5,borderaxespad=0.)
    
  plt.savefig("%s.png" % name)
      
