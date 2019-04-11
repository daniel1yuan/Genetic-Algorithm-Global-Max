# @file: Main file for running GlobalMax Simulation
# @author: Daniel Yuan
import logging as log
import os
import math
import argparse
import pickle
from numpy import median, average
from datetime import datetime
from problem.term import Term
from problem.polynomial import Polynomial
from benchmark import Benchmark
from algos.brute_force import BruteForceSolver
from algos.genetic_algorithm.genetic_algorithm import GeneticAlgorithmSolver
from gui.gui import Gui
from utils.search_range import SearchRange

parser = argparse.ArgumentParser(description="Global Max Benchmark")
parser.add_argument('-f', '--folder', default="storage", help="folder to store benchmark data")

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
  search_range.set_feasible_range(10000, 2)

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
  animation = gui.create_animation(genetic_algorithm_solver)

  # Create Default Visual
  # gui.plot_problem()
  gui.show()

def add_to_benchmark_payload(storage, solver, metric):
  name = solver.solver_name

  if name not in storage:
    storage[name] = {
      'time': {
        'data': [],
        'median': None,
        'average': None,
        'min': None,
        'max': None
      },
      'max_solution': {
        'data': [],
        'median': None,
        'average': None,
        'min': None,
        'max': None
      }
    }

  if metric:
    for key, value in storage[name].iteritems():
      storage[name][key]['data'].append(metric[key])
      data = storage[name][key]['data']
      storage[name][key]['average'] = average(data)
      storage[name][key]['median'] = median(data)
      storage[name][key]['min'] = min(data)
      storage[name][key]['max'] = max(data)

def run_benchmark(root_folder, times, feasible_ranges):
  if not os.path.exists(root_folder):
    log.info('Creating Folder')
    os.makedirs(root_folder)

  for feasible_range in feasible_ranges:
    search_range = SearchRange()
    search_range.set_feasible_range(feasible_range, 2)
    folder = os.path.join(root_folder, 'feasible_range_{}'.format(feasible_range))
    solution_payload = {}

    if not os.path.exists(folder):
      os.mkdir(folder)

    for i in range(times):
      # Create Folder
      run_folder = os.path.join(folder, 'run_{}'.format(i))

      if not os.path.exists(run_folder):
        os.mkdir(run_folder)

        # Create Problem
        polynomial = Polynomial(num_terms=5, num_dimensions=2)
        log.info(polynomial)

        # Solvers
        brute_force_solver = BruteForceSolver(search_range)
        genetic_algorithm_solver = GeneticAlgorithmSolver(search_range)

        solvers = [brute_force_solver, genetic_algorithm_solver]

        # Benchmark
        benchmark = Benchmark(solvers)
        benchmark.evaluate(polynomial)

        # Add to Benchmark
        for solver in solvers:
          metric = benchmark.get_metrics(solver._id)
          add_to_benchmark_payload(solution_payload, solver, metric)

        # Save Animations
        gui = Gui(polynomial, search_range)
        genetic_animation = gui.create_animation(genetic_algorithm_solver)
        genetic_animation.save(os.path.join(run_folder, 'genetic.gif'), writer='imagemagick', fps=30)

        brute_animation = gui.create_animation(brute_force_solver)
        brute_animation.save(os.path.join(run_folder, 'brute.gif'), writer='imagemagick', fps=30)

        # Save Problem
        figure, plot = gui.plot_problem()
        figure.savefig(os.path.join(run_folder, 'problem.png'))

        # Pickle benchmark && solvers && polynomial
        pickle_object(genetic_algorithm_solver, os.path.join(run_folder, 'genetic_solver.pickle'))
        pickle_object(brute_force_solver, os.path.join(run_folder, 'brute_solver.pickle'))
        pickle_object(benchmark, os.path.join(run_folder, 'brute_solver.pickle'))
        pickle_object(gui, os.path.join(run_folder, 'gui.pickle'))

        # Clear Matplotlib figures
        gui.close()

      pickle_object(solution_payload, os.path.join(folder, 'benchmark.pickle'))

def pickle_object(object, filename):
  with open(filename, 'w') as file:
    pickle.dump(object, file)

if __name__ == '__main__':
  setup_logging()
  args = parser.parse_args()
  run_benchmark(args.folder, 1, [100, 500, 1000, 2500, 5000, 7500, 10000])
  # main()
