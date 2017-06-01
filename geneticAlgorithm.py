# @author: Daniel Yuan (daniel1yuan@gmail.com)
# @file: geneticAlgorithm.py
# @brief: Script for executing the genetic algorithm to solve for global maxima of a given problem

#import statements
from random import randint, uniform
from problem import *
from globals import *

# Class Definitions

class GeneticAlgorithm(object):
  def __init__(self, problem = None):
    if (problem):
      self.problem = problem
    else:
      self.problem = Problem()
    self.maxRange = self.problem.range
    self.dimensions = self.problem.dimensions
    self.population = Population(None, self.dimensions, self.maxRange)

  def runGeneticAlgorithm(self):
    for i in range(500):
      self.population.getFitness(self.problem.function)
      print ("Current Total Fitness")
      print (self.population.overallFitness)
      print ("Max Fitness:")
      print (self.population.maxFitness)
      self.population = self.population.genNewPopulation()

# Class definition for a population
class Population(object):
  def __init__(self, population = None, dimension = None, maxRange = None, numVector = DEFAULT_POPULATION["NUM_VECTOR"]):
    if ((not dimension) and (not population)):
      raise ValueError("No dimension or population specified. Need to specify either dimension from problem or population")
    if (population):
      self.population = population
    else:
      # If no population is given, generate a random population with given dimension and range
      self.population = genRandomPopulation(numVector, dimension, maxRange)
    self.numVector = numVector
    self.dimension = dimension
    self.maxRange = maxRange
    self.mutationRate = DEFAULT_POPULATION["MUTATION_RATE"]

  # Calls getFitness on every vector in population
  def getFitness(self, function):
    overallFitness = 0
    minFitness = 0
    maxFitness = None
    for vector in self.population:
      fitness = vector.getFitness(function)
      overallFitness += fitness
      if (fitness < minFitness):
        minFitness = fitness
      if (maxFitness == None):
        maxFitness = fitness
      elif (maxFitness < fitness):
        maxFitness = fitness

    self.maxFitness = maxFitness
    # If Fitness is negative, shift everything up until it's positive
    if (minFitness < 0):
      overallFitness = 0
      for vector in self.population:
        vector.fitness -= minFitness
        overallFitness += vector.fitness

    self.overallFitness = overallFitness
    
  # Generates new population given that the fitness of 
  def genNewPopulation(self):
    # Generate new population for parents by selecting based on fitness function using pool selection
    newPopulation = []
    for i in range(self.numVector):
      parentA = pickVector(self.population, self.overallFitness)
      parentB = pickVector(self.population, self.overallFitness)
      newVector = parentA.crossover(parentB, self.mutationRate)
      newPopulation.append(newVector)

    # After new population is created, return new Population object
    return Population(newPopulation, self.dimension, self.maxRange, self.numVector) 
      

# Class definition of a vector
#   Vector.vector is Array of values for a problem (i.e. [1,2,3,4] for 4-dimensional problem)
class Vector(object):
  def __init__(self, vector = None, maxRange = None, dimension = None):
    if ((not maxRange) and not(dimension or vector)):
      raise ValueError("No vector &  range specified. Can not generate random vector or load a vector")
    self.range = maxRange
    if (vector):
      self.vector = vector
      if (dimension):
        self.dimension = dimension
      else:
        self.dimension = len(vector)
    else:
      # Dimension must be specified if vector is not
      self.dimension = dimension
      self.vector = genRandomVector(dimension, maxRange)
  
  # Crossover function for genetic algorithm to mix "genes" of two vectors
  # This function chooses a random point inbetween the two vectors and crosses them
  def crossover(self, otherVector, mutationRate):
    if (not (self.dimension is otherVector.dimension)):
      raise ValueError("Trying to crossover two vectors of different dimensions")
    else:
      crossIndex = randint(0, self.dimension - 1)
      newVector = []
      for i in range(self.dimension):
        randFloat = uniform(0, 1)
        # If the random float is less than our mutation rate, mutate current index of vector
        if (randFloat <= mutationRate):
          newVector.append(randint(-1 * self.range, self.range)) 
        else:
          if (i < crossIndex):
            newVector.append(self.vector[i])
          else:
            newVector.append(otherVector.vector[i])
      
      crossVector = Vector(newVector, self.range)
    return crossVector

  # Gets fitness of current vector given a function
  def getFitness(self, function):
    self.fitness = function.evaluate(self.vector)
    return self.fitness
  

# Helper Functions

# Given a dimension, generate a random vector 
def genRandomVector(dimension, maxRange):
  vector = []
  for i in range(dimension): 
    vector.append(randint(-1 * maxRange, maxRange))
  return vector

# Given # of vectors, dimension, and maximum range => generate a random population
def genRandomPopulation(numVector, dimension, maxRange):
  vectors = []
  for i in range(numVector):
    vectors.append(Vector(None, maxRange, dimension))
  return vectors

# Given a list of vectors and the total fitness, select a vector based on it's fitness (probability of selecting vector scales on fitness
def pickVector(vectorList, totalFitness):
  # Selects a value between 0 and total fitness randomly
  randomValue = uniform(0, totalFitness)

  # Subtract fitness of each vector until the value is negative
  for vector in vectorList:
    randomValue -= vector.fitness

    # If randomValue becomes negative, that means the current vector is chosen
    if (randomValue < 0):
      return vector
  
  # If the loop finishes and no return was set, that means the randomValue was totalFitness, and therefore the last vector is chosen
  return vectorList[-1]
