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
  search_range.set_feasible_range(100, 2)

  # Solvers
  # brute_force_solver = BruteForceSolver(search_range)
  genetic_algorithm_solver = GeneticAlgorithmSolver(search_range)

  gui = Gui(polynomial, search_range)
  # benchmark = Benchmark([brute_force_solver, genetic_algorithm_solver])
  # benchmark = Benchmark([genetic_algorithm_solver])

  # Benchmark
  # benchmark.evaluate(polynomial)

  # Visualize Solvers
  # gui.create_animation(brute_force_solver)
  gui.create_animation(genetic_algorithm_solver)

  # Create Default Visual
  # gui.plot_problem()
  gui.show()

if __name__ == '__main__':
  setup_logging()
  main()
