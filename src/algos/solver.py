# @file: Generic solver class
# @author: Daniel Yuan
import math
import uuid

class Solver(object):
  def __init__(self, search_range=None, problem=None, threads=1):
    self._id = uuid.uuid4()
    self.problem = problem
    self.search_range = search_range
    self.threads = threads
    self.storage = None
    self.max_iteration = self.search_range.get_max_iteration() if self.search_range else 1000

  def solve(self):
    pass

  def set_range(self, search_range):
    self.search_range = search_range

  def set_problem(self, problem):
    self.problem = problem

  def get_storage_length(self):
    return len(self.storage) if self.storage else None

  def get_storage(self, index=None):
    pass
