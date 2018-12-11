# @file: Gui class for displaying problem
# @author: Daniel Yuan

import pdb
import sys
import itertools
import logging as log
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from utils.math_utils import normalize
from constants import GUI_DEFAULT_PLOT_RESOLUTION

class Gui(object):
  def __init__(self, search_range, plot_resolution=GUI_DEFAULT_PLOT_RESOLUTION):
    self.search_range = search_range
    self.plot_resolution = plot_resolution
    self.fig = plt.figure()

  def set_problem(self, problem):
    self.problem = problem

  def set_solvers(self, solvers):
    self.solvers = solver

  def _create_subplot(self):
    plot = self.fig.add_subplot(122, projection='3d')
    plot.set_xlabel('X Axis')
    plot.set_ylabel('Y Axis')
    plot.set_zlabel('Z Axis')
    plot.set_xlim([-1, 1])
    plot.set_ylim([-1, 1])
    plot.set_zlim([-1, 1])
    return plot

  def plot_problem(self, problem):
    self.set_problem(problem)
    dimensions = problem.dimensions

    if dimensions > 2:
      log.warning('Can\'t plot problem as it is greater than 3 spacial dimensions')
      return

    if dimensions is 2:
      self.plot = self.fig.add_subplot(121, projection='3d')
      self.plot.set_xlabel('X Axis')
      self.plot.set_ylabel('Y Axis')
      self.plot.set_zlabel('Z Axis')
    else:
      self.plot = self.fig.add_subplot(121)

    x_points = []
    y_points = []
    z_points = []

    min_index = self.search_range.get_min()
    max_index = self.search_range.get_max()
    num_points = float(abs(max_index - min_index))/self.plot_resolution
    x = np.arange(min_index, max_index, num_points, dtype=float)
    y = np.arange(min_index, max_index, num_points, dtype=float)

    for idx in itertools.product(*[x,y]):
      x_points.append(idx[0])
      y_points.append(idx[1])
      z_points.append(problem.eval(list(idx)))

    z_points = np.array(normalize(z_points))

    self.plot.plot_trisurf(x_points,y_points,z_points)

  def save(self, name):
    filename = '{}_animation.gif'.format(name)
    log.info('Saving Animation to {}'.format(filename))

  def show(self):
    plt.show()

  def update(self, i):
    plots = []

    for _, storage in self.storage.iteritems():
      solver = storage['solver']
      plot, = storage['plot']
      max_plot, = storage['max_plot']
      solution = solver.get_storage(i)

      if solution:
        x = []
        y = []
        z = []

        max_value = -1 * np.Inf
        max_solution = None
        for point in solution:
          vector = point[0]
          value = point[1]
          is_current_max = point[2]

          x.append(vector[0])
          y.append(vector[1])
          z.append(value)

          if value > max_value:
            max_value = value
            max_solution = (vector[0], vector[1], value)

        plot.set_data(x,y)
        plot.set_3d_properties(z)

        if max_solution:
          max_plot.set_data(max_solution[0], max_solution[1])
          max_plot.set_3d_properties(max_solution[2])
          plots.append(max_plot)

        plots.append(plot)
    return plots

  def create_animation(self, problem, solvers):
    self.plot_problem(problem)
    self.solvers = solvers
    self.storage = {}
    for solver in solvers:
      plot = self._create_subplot()
      self.storage[solver._id] = {
        'solver': solver,
        'plot': plot.plot([],[],[], linestyle="", marker="o", label=str(solver), alpha=0.3),
        'max_plot': plot.plot([],[],[],linestyle="", marker="o", color='red')
      }
      solver.solve(problem, True)

    self.title = self.plot.set_title('')

    self.anim = FuncAnimation(self.fig, self.update, frames=1000, interval=20, blit=True)

    plt.show()
