# @file: Population class for Genetic Algorithm
# @author: Daniel Yuan

from random import uniform
import numpy as np
from individual import Individual
from constants import DEFAULT_POPULATION_SIZE

class Population(object):
  def __init__(self, search_range, dimension, population_size=DEFAULT_POPULATION_SIZE, mutation_rate=0.05):
    assert(search_range and dimension)

    self.mutation_rate = mutation_rate
    self.search_range = search_range
    self.dimension = dimension
    self.population_size = population_size
    self.population = self._generate_random_population()

  def calculate_fitness(self, problem):
    max_individual = None
    min_fitness = np.Inf
    max_fitness = -1 * np.Inf

    # Calculate Fitness
    for individual in self.population:
      fitness = individual.get_fitness(problem)

      if fitness < min_fitness:
        min_fitness = fitness
      if fitness > max_fitness:
        max_fitness = fitness
        max_individual = individual

    # Normalize Fitness
    overall_fitness = 0

    translate_fitness = min_fitness if min_fitness < 0 else -1 * min_fitness
    scale_fitness = max_fitness - min_fitness
    for individual in self.population:
      individual.fitness += translate_fitness
      individual.fitness /= (scale_fitness if scale_fitness != 0 else 1)

      overall_fitness += individual.fitness

    return overall_fitness, max_fitness, max_individual

  def generate_new_population(self):
    new_population = []
    self.population.sort(key=lambda x: x.fitness)

    for _ in range(self.population_size):
      parent_a = self._pick_vector()
      parent_b = self._pick_vector()
      new_vector = parent_a.crossover(parent_b, self.mutation_rate)
      new_population.append(new_vector)

    self.overall_fitness = None
    self.population = new_population


  def _generate_random_population(self):
    vectors = []
    for i in range(self.population_size):
      vectors.append(Individual(None, self.search_range, self.dimension))
    return vectors


  def _pick_vector(self):
    target_fitness = uniform(0,1)
    for individual in self.population:
      target_fitness -= individual.fitness

      if target_fitness < 0:
        return individual

    return self.population[-1]
