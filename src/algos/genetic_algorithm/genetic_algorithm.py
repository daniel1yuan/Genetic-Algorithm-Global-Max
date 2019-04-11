# @file: Genetic Algorithm Solver
# @author: Daniel Yuan

import numpy as np
from population import Population
from ..solver import Solver

class GeneticAlgorithmSolver(Solver):
  def __init__(self, search_range=None, problem=None, threads=1):
    Solver.__init__(self, search_range, problem, threads)
    self.solver_name = 'Genetic Algorithm Solver'
    self.max_iteration = self.search_range.get_max_iteration()

  def solve(self, problem=None, should_store=False):
    if should_store:
      self.storage = []

    self.max_individual = None
    self.max_fitness = -1 * np.Inf
    self.count = 0
    self.iter_count = 0
    self.threshold = 0.05

    if problem:
      return self._solve(problem, should_store)
    else:
      return self._solve(self.problem, should_store)

  def _solve(self, problem, should_store):
    max_individual = None
    max_fitness = -1 * np.Inf

    population = Population(self.search_range, problem.dimensions)
    while self._should_continue(max_fitness, max_individual):
      self.iter_count += 1
      overall_fitness, max_fitness, max_individual = population.calculate_fitness(problem)

      if should_store:
        self._store(problem, population, max_individual)

      population.generate_new_population()

    return self.max_fitness, self.max_individual.vector

  def _should_continue(self, fitness, max_individual):
    if self.iter_count >= self.max_iteration:
      return False

    if fitness > self.max_fitness:
      self.max_fitness = fitness
      self.max_individual = max_individual
      self.count = 0
      return True

    if 1.0 - float(fitness)/self.max_fitness < self.threshold:
      self.count += 1

    if self.count >= 100:
      return False

    return True

  def _store(self, problem, population, max_individual):
    storage_vector = []
    for individual in population.population:
      storage_vector.append((individual.get_vector(), individual.get_fitness(problem), individual is max_individual))

    self.storage.append(storage_vector)

  def get_storage(self, index=None):
    if index is not None and self.storage is not None:
      if index < len(self.storage) and index >= 0:
        return self.storage[index]
    return self.storage
