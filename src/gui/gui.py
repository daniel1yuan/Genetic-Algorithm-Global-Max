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
from constants import GUI_DEFAULT_PLOT_RESOLUTION, GUI_DEFAULT_FRAMES, GUI_DEFAULT_MAX_POINTS

class Gui(object):
  def __init__(self, problem, search_range, plot_resolution=GUI_DEFAULT_PLOT_RESOLUTION, num_frames=GUI_DEFAULT_FRAMES):
    self.search_range = search_range
    self.set_problem(problem)
    self.plot_resolution = plot_resolution
    self.num_frames = num_frames
    self.figures = []

  def set_problem(self, problem):
    self.problem = problem
    self.dimensions = problem.dimensions

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

  def plot_problem(self):
    figure, plot = self.create_plot()

    # Calculate points for the problem
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
      z_points.append(self.problem.eval(list(idx)))

    z_points = np.array(normalize(z_points))

    plot.plot_trisurf(x_points,y_points,z_points)

    return figure, plot

  def create_plot(self):
    figure = plt.figure()
    if self.dimensions > 2:
      log.warning('Can\'t plot problem as it is greater than 3 spacial dimensions')
      return

    if self.dimensions is 2:
      plot = figure.add_subplot(111, projection='3d')
      plot.set_xlabel('X Axis')
      plot.set_ylabel('Y Axis')
      plot.set_zlabel('Z Axis')

      plot.set_xlim(-1, 1)
      plot.set_ylim(-1, 1)
      plot.set_zlim(-2, 2)
    else:
      plot = self.fig.add_subplot(111)

    self.figures.append(figure)
    return figure, plot

  def save(self, name):
    filename = '{}_animation.gif'.format(name)
    log.info('Saving Animation to {}'.format(filename))

  def show(self):
    plt.show()

  def close(self):
    plt.close()
    plt.clf()

    for figure in self.figures:
      plt.close(figure)

  def create_animation(self, solver):
    self.storage = {}

    figure, plot = self.create_plot()
    scatter = plot.scatter([],[],[])
    solver.solve(self.problem, True)
    title = plot.set_title('')
    solution_length = solver.get_storage_length()
    frames = min(solution_length, self.num_frames)

    def update(i):
      # Scale index to length
      index = int(i * float(solution_length)/frames)
      solution = solver.get_storage(index)
      num_points = min(GUI_DEFAULT_MAX_POINTS, len(solution))

      title.set_text('{} - {}'.format(solver.solver_name, index))

      if solution:
        x = []
        y = []
        z = []

        for index in range(num_points):
          solution_index = int(index * float(len(solution))/num_points)
          point = solution[solution_index]

        # for point in solution:
          vector = point[0]
          value = point[1]
          is_current_max = point[2]

          x.append(vector[0])
          y.append(vector[1])
          z.append(value)

        scatter._offsets3d = (x,y,z)

      return [scatter]

    return FuncAnimation(figure, update, frames=frames, interval=5/frames*1000, blit=False)
