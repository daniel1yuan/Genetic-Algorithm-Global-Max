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

  def solve(self):
    pass

  def set_range(self, search_range):
    self.search_range = search_range

  def set_problem(self, problem):
    self.problem = problem

  def get_storage_length(self):
    return len(self.storage) if self.storage else None

  def get_storage(self, index=None):
    if index and self.storage is not None:
      if index < len(self.storage) and index >= 0:
        return self.storage[:index]
      return None
    else:
      return self.storage
