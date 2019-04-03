# @file: Describes Search Range
# @author: Daniel Yuan

import math

class SearchRange(object):
  def __init__(self, dimension_min=-1.0, dimension_max=1.0, max_iteration=100000000000):
    self.dimension_min = dimension_min
    self.dimension_max = dimension_max
    self.max_iteration = max_iteration

  def set_feasible_range(self, iterations, dimensions):
    self.max_iteration = iterations
    self.dimension_resolution = math.ceil(iterations ** float(1.0/dimensions))

  def get_dimension_resolution(self):
    return self.dimension_resolution

  def get_max_iteration(self):
    return self.max_iteration

  def get_min(self):
    return self.dimension_min

  def get_max(self):
    return self.dimension_max
