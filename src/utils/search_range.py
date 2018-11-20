# @file: Describes Search Range
# @author: Daniel Yuan

import math

class SearchRange(object):
  def __init__(self, dimension_min=-1.0, dimension_max=1.0):
    self.dimension_min = dimension_min
    self.dimension_max = dimension_max

  def set_feasible_range(self, iterations, dimensions):
    self.dimension_resolution = math.ceil(iterations ** float(1.0/dimensions))

  def get_dimension_resolution(self):
    return self.dimension_resolution

  def get_min(self):
    return self.dimension_min

  def get_max(self):
    return self.dimension_max
