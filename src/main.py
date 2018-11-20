# @file: Main file for running GlobalMax Simulation
# @author: Daniel Yuan
import logging as log
import math
from datetime import datetime
from problem.term import Term
from problem.polynomial import Polynomial
from benchmark import Benchmark
from algos.brute_force import BruteForceSolver

def get_feasible_range(iterations, dimensions):
  return math.ceil(iterations ** float(1.0/dimensions))

def setup_logging():
  dateString = datetime.now().strftime('%m-%d-%y-%H-%M')
  log.basicConfig(
    format='%(levelname)s - %(asctime)s| %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=log.INFO
  )

def main():
  polynomial = Polynomial(num_terms=2, num_dimensions=2)
  search_range = get_feasible_range(100000, 2)
  brute_force_solver = BruteForceSolver(search_range)
  benchmark = Benchmark([brute_force_solver])

  benchmark.evaluate(polynomial)


  print polynomial
  print polynomial.eval([1,2])

if __name__ == '__main__':
  setup_logging()
  main()
