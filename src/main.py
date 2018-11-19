# @file: Main file for running GlobalMax Simulation
# @author: Daniel Yuan

from problem.term import Term
from problem.polynomial import Polynomial

def main():
  polynomial = Polynomial(num_terms=1, num_dimensions=2)

  print polynomial
  print polynomial.eval([1,2])

if __name__ == '__main__':
  main()
