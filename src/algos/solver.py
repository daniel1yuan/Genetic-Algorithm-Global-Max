# @file: Generic solver class
# @author: Daniel Yuan
import math

class Solver(object):
  def __init__(self, search_range=None, problem=None, threads=1):
    self.range = None
    self.problem = None
    self.search_range = search_range
    self.threads = threads

  def solve(self):
    pass

  def set_range(self, search_range):
    self.search_range = search_range

  def set_problem(self, problem):
    self.problem = problem
