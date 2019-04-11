# @file: Benchmarks Different Algorithms

import logging as log
from timeit import default_timer as timer

class Benchmark(object):
  def __init__(self, solvers):
    assert(solvers and len(solvers) > 0)
    self.solvers = solvers
    self.benchmark = {}

  def evaluate(self, problem=None):
    assert(problem)
    for solver in self.solvers:
      log.info('Benchmarking: {}'.format(solver.solver_name))
      start_time = timer()
      max_solution, max_vector = solver.solve(problem)
      end_time = timer()
      log.info('Max Solution: {} - Max Vector: {}'.format(max_solution, max_vector))
      log.info('{} took: {}s'.format(solver.solver_name, end_time - start_time))

      id = solver._id

      self.benchmark[id] = {
        'solver': solver,
        'problem': problem,
        'max_solution': max_solution,
        'max_vector': max_vector,
        'time': end_time - start_time
      }

  def get_metrics(self, id):
    if id in self.benchmark:
      return self.benchmark[id]
    return None
