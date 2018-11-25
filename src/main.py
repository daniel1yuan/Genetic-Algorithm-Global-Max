# @file: Main file for running GlobalMax Simulation
# @author: Daniel Yuan
import logging as log
import math
from datetime import datetime
from problem.term import Term
from problem.polynomial import Polynomial
from benchmark import Benchmark
from algos.brute_force import BruteForceSolver
from algos.genetic_algorithm.genetic_algorithm import GeneticAlgorithmSolver
from gui.gui import Gui
from utils.search_range import SearchRange

def setup_logging():
  dateString = datetime.now().strftime('%m-%d-%y-%H-%M')
  log.basicConfig(
    format='%(levelname)s - %(asctime)s| %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=log.INFO
  )

def main():
  # Create Problem
  polynomial = Polynomial(num_terms=5, num_dimensions=2)
  log.info(polynomial)

  # Define Search Range
  search_range = SearchRange()
  search_range.set_feasible_range(10000000, 2)

  # Solvers
  brute_force_solver = BruteForceSolver(search_range)
  genetic_algorithm_solver = GeneticAlgorithmSolver(search_range)

  gui = Gui(search_range)
  benchmark = Benchmark([brute_force_solver, genetic_algorithm_solver])
  # benchmark = Benchmark([genetic_algorithm_solver])

  # Visualize Solvers
  # gui.create_animation(polynomial, [brute_force_solver])

  # Benchmark
  benchmark.evaluate(polynomial)

  # Create Default Visual
  gui.plot_problem(polynomial)
  gui.show()

if __name__ == '__main__':
  setup_logging()
  main()
