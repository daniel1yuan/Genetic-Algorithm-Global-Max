# @file: Polynomial Definition for problems
# @author: Daniel Yuan

import random

from constants import POLYNOMIAL_DEFAULT_MAX_DIMENSIONS, POLYNOMIAL_DEFAULT_MAX_TERMS

class Polynomial(object):
  def __init__(self, terms=None, polynomial=None, num_terms=None, num_dimensions=None, seed=None):
    self.seed = seed
    random.seed(seed)

    self.terms = terms if terms else self._generate_random_polynomial(num_terms, num_dimensions)

  def _generate_random_polynomial(self, num_terms=None, num_dimensions=None):
    terms = []
