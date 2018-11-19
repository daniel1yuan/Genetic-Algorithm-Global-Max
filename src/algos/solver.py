# @file: Generic solver class
# @author: Daniel Yuan
import math

class Solver(object):
  def __init__(self, problem=None, threads=1):
    self.range = None
    self.problem = None
    self.threads = 1

  def solve(self):
    assert(self.range and self.problem)

  def set_range(self, range):
    self.range = range

  def feasible_range(self, iterations, dimensions):
    return math.log(iterations, dimensions)
