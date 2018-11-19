# @file: Term of a Polynomial
# @author: Daniel Yuan

import random
import logging as log
from constants import TERM_DEFAULT_MIN_POWER, TERM_DEFAULT_MAX_POWER, TERM_DEFAULT_MIN_K, TERM_DEFAULT_MAX_K

# Class definition for a Term of a funcion
# Given a generic term is: k*(b0^e0)*(b1^e1)*....(bn^en)
# Where k = constant
# Where b = dimension variable
# Where e = power of dimension
# Example Representation:
#   9x^3y^5:
#    - k = 9
#    - e = [3, 5]
class Term(object):
  def __init__(self, dimensions=None, term=None, seed=None):
    # Check valid parameters
    assert(dimensions or term)

    # Load term from existing term
    if term:
      self._parse_term(term)
    else:
      self.seed = seed
      random.seed(seed)
      self.k = random.randint(TERM_DEFAULT_MIN_K, TERM_DEFAULT_MAX_K)
      self.dimensions = dimensions
      self.exponents = self._generate_random_exponents(dimensions)

  def eval(self, values):
    assert(values and len(values) == len(self.exponents))
    solution = 1

    for i, val in enumerate(values):
      solution *= float(value) ** self.exponents[i]

    return self.k * solution

  def __repr__(self):
    repr_str = 'TERM: {}'.format(self.k)
    for i, exp in enumerate(self.exponents):
      repr_str += '(b{}^{})'.format(i, exp)

    return repr_str

  def _parse_term(self, term):
    self.k = term.k
    self.dimensions = term.dimensions
    self.exponents = term.exponents

  def _generate_random_exponents(self, dimensions):
    exponents = []
    for _ in range(dimensions):
      exponents.append(random.randint(TERM_DEFAULT_MIN_POWER, TERM_DEFAULT_MAX_POWER))

    return exponents
