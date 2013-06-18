#!/usr/bin/env python

from memprof import *
import time

MB = 1024 * 1024

class FooClass(object):
  def __init__(self):
    self.a = [1] * MB
    self.b = [1] * MB * 2
        
@memprof
def bar(limit = 10000):
  bar_a = [1] * MB * 10

  for i in range(limit):
    bar_a.append(1)
  
@memprof
def foo2():
  a = [1] * MB
  b = [1] * MB * 2
  c = [1] * MB * 3
  
@memprof
def foo(limit = 500000):
  a = []
  b = []
  c = [1] * MB
  
  for i in range(limit):
    a.append(1)
    b.append(1)
    b.append(1)
    
    if i == limit/2:
      del a[:]
      del c[:]
    elif i == (limit*3)/4:
      c = [1] * MB * 2 

@memprof
def fooObject(limit = 500000):
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
