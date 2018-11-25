# @file: Brute force solver for global max
# @author: Daniel Yuan

import itertools
import numpy as np
import uuid
from solver import Solver

class BruteForceSolver(Solver):
  def __init__(self, search_range=None, problem=None, threads=1):
    Solver.__init__(self, search_range, problem, threads)
    self.solver_name = 'Brute Force Solver'

  def solve(self, problem=None, storage=False):
    if storage:
      self.storage = []

    if problem:
      return self._solve(problem, storage)
    else:
      return self._solve(self.problem, storage)

  def _solve(self, problem, storage):
    dimensions = problem.dimensions
    max_solution = -1 * np.Inf
    max_vector = None

    min_index = self.search_range.get_min()
    max_index = self.search_range.get_max()
    search_resolution = self.search_range.get_dimension_resolution()
    num_points = float(abs(max_index - min_index))/search_resolution

    search_space = []


    for _ in range(dimensions):
      search_space.append(np.arange(min_index, max_index, num_points, dtype=float))

    for idx in itertools.product(*search_space):
      vector = list(idx)
      solution = problem.eval(vector)

      # Show Currently searched points
      if solution > max_solution:
        max_solution = solution
        max_vector = vector

        if self.storage is not None:
          self.storage.append((vector, solution, True))
      elif self.storage is not None:
        self.storage.append((vector, solution, False))

    return max_solution, max_vector, storage
