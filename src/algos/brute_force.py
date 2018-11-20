# @file: Brute force solver for global max
# @author: Daniel Yuan

import itertools
import numpy as np
from solver import Solver

class BruteForceSolver(Solver):
  def __init__(self, search_range=None, problem=None, threads=1):
    Solver.__init__(self, search_range, problem, threads)
    self.solver_name = 'Brute Force Solver'

  def solve(self, problem=None):
    if problem:
      return self._solve(problem)
    else:
      return self._solve(self.problem)

  def _solve(self, problem):
    dimensions = problem.dimensions
    max_solution = -1 * np.Inf
    max_vector = None

    for idx in itertools.product(*[range(0, int(self.search_range)) for _ in range(dimensions)]):
      vector = list(idx)
      solution = problem.eval(vector)
      if solution > max_solution:
        max_solution = solution
        max_vector = vector

    return max_solution, max_vector
