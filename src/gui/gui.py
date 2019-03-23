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
    self.num_frames = 200
    self.plot_resolution = plot_resolution

  def set_problem(self, problem):
    self.problem = problem

  def set_solvers(self, solvers):
    self.solvers = solvers

  def plot_problem(self, problem):
    self.set_problem(problem)
    dimensions = problem.dimensions

    if dimensions > 2:
      log.warning('Can\'t plot problem as it is greater than 3 spacial dimensions')
      return

    if dimensions is 2:
      self.plot = self.fig.add_subplot(111, projection='3d')
      self.plot.set_xlabel('X Axis')
      self.plot.set_ylabel('Y Axis')
      self.plot.set_zlabel('Z Axis')
    else:
      self.plot = self.fig.add_subplot(111)

    return

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
      plot = storage['plot']
      solution_length = solver.get_storage_length()
      index = int(float(i)/self.num_frames*solution_length)
      print(index)
      solution = solver.get_storage(index)
      self.title.set_text('{}'.format(i))

      if solution:
        x = []
        y = []
        z = []
        for point in solution:
          vector = point[0]
          value = point[1]
          is_current_max = point[2]

          x.append(vector[0])
          y.append(vector[1])
          z.append(value)

        plot._offsets3d = (x,y,z)
        plots.append(plot)

    return plots

  def create_animation(self, problem, solvers):
    self.fig = plt.figure()
    self.plot_problem(problem)
    self.solvers = solvers
    self.storage = {}

    for solver in solvers:
      self.storage[solver._id] = {
        'solver': solver,
        'plot': self.plot.scatter([],[],[])
      }
      solver.solve(problem, True)

    self.title = self.plot.set_title('')

    self.anim = FuncAnimation(self.fig, self.update, frames=self.num_frames, interval=40, blit=False)

    plt.show()
