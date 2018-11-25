# @file: Individual that contains the 'DNA' for each individual in the population
# @author: Daniel Yuan

from random import randint, uniform

class Individual(object):
  def __init__(self, vector, search_range, dimension=None):
    # Ensure that Indidual has
    assert(search_range and (vector or dimension))
    self.search_range = search_range

    if vector:
      self.vector = vector
      self.dimension = len(vector)
    else:
      self.dimension = dimension
      self.vector = self._generate_random_vector()

  def get_vector(self):
    return self.vector

  def crossover(self, other_vector, mutation_rate):
    if self.dimension is not other_vector.dimension:
      raise Exception('Trying to cross over vectors of different dimensions')

    cross_index = randint(0, self.dimension - 1)
    new_vector = []

    for i in range(self.dimension):
      should_mutate = uniform(0, 1) <= mutation_rate

      value = 0
      if should_mutate:
        value = uniform(self.search_range.get_min(), self.search_range.get_max())
      elif i < cross_index:
        value = self.vector[i]
      else:
        value = other_vector.vector[i]

      new_vector.append(value)

    return Individual(new_vector, self.search_range)


  def get_fitness(self, problem):
    self.fitness = problem.eval(self.vector)
    return self.fitness

  def _generate_random_vector(self):
    vector = []
    for _ in range(self.dimension):
      min_value = self.search_range.get_min()
      max_value = self.search_range.get_max()
      vector.append(uniform(min_value, max_value))

    return vector
