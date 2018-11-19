# @file: Polynomial Definition for problems
# @author: Daniel Yuan

import random
from term import Term
from constants import POLYNOMIAL_DEFAULT_MAX_DIMENSIONS, POLYNOMIAL_DEFAULT_MAX_TERMS

class Polynomial(object):
  def __init__(self, terms=None, polynomial=None, num_terms=None, num_dimensions=None, seed=None):
    self.seed = seed
    random.seed(seed)

    self.terms = terms if terms else self._generate_random_polynomial(num_terms, num_dimensions)

  def __repr__(self):
    repr_str = 'Polynomial: '
    for i, term in enumerate(self.terms):
      if i is not 0:
        repr_str += '+ '
      repr_str += '{} '.format(str(term))

    return repr_str

  def eval(self, values):
    solution = 0
    for term in self.terms:
      solution += term.eval(values)

    return solution

  def _generate_random_polynomial(self, num_terms=None, num_dimensions=None):
    if not num_terms:
      num_terms = random.randint(1, POLYNOMIAL_DEFAULT_MAX_TERMS)

    if not num_dimensions:
      num_dimensions = random.randint(1, POLYNOMIAL_DEFAULT_MAX_DIMENSIONS)

    terms = []
    for i in range(num_terms):
      term = Term(num_dimensions)
      terms.append(term)
    return terms
