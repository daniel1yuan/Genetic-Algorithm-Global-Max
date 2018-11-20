# @file: Gui class for displaying problem
# @author: Daniel Yuan

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
    plt.show()

  def update(self, i):
    pass

  def create_animation(self, solvers):
    label = '{}: {}'
