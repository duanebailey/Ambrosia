from ambrosia import *
from math import sin,cos
from random import random

def rand(low,high):
  range = high-low
  return low + range*random()

def plasterMat(hue):
  mat = Material()
  mat.type('plaster')
  mat.color(hsv2rgb((hue,1,1)))
  return mat

def length(l):
  if l == []:
    return 0
  else:
    return 1+length(l[1:])

def lastElement(l):
  if l == []:
    return None
  elif length(l) == 1:
    return l[0]
  else:
    return lastElement(l[1:])


