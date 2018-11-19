# @author: Daniel Yuan
# @file: problems.py
# @brief: Generates problems for global max problems
#         Temporarily only dealing with polynomials

# IMPORTS
import pdb
from random import randint
import math
from globals import *

# Class definiton of a problem
class Problem(object):
  
  # Constructor
  # @params: function object (if there is no function given, generate a random one)
  def __init__(self, params = None):
    if (params):
      self.function = params.function
    else:
      self.function = Function()
    self.dimensions = self.function.dimensions
    self.range = getFeasibleRange(self.dimensions)

  # Uses brute force to find the true global Max contstrained by range
  def solveProblem(self):
    vector = []
    for i in range(self.dimensions):
      vector.append(-1 * self.range)
    maxSolution, maxVector =bruteForceSolve(1, vector, self.dimensions, self.range, self.function)
    self.globalMaxVector = maxVector
    self.globalMax = maxSolution
    return self.globalMax

# Class definition for a function
# Default Parameters taken from DEFAULT_FUNCTION
# terms are array of Term objects, which must all have same dimensions
class Function(object):
  def __init__(self, terms = None):
    if (terms):
      self.terms = terms
    else:
      self.terms = genRandomFunction()
    self.setDimension()
  
  # Apply given array to all terms to solve for solution to the function
  # (i.e.) Term1 + Term2 + Term3 + ... + TermN 
  def evaluate(self, arr):
    solution = 0
    for term in self.terms:
      solution += term.evaluate(arr) 
    return solution
 
  # Set dimension attribute by extracting from first term
  def setDimension(self):
    self.dimensions = self.terms[0].dimensions
    

# Class definition for a term of a function
# Default Parameters taken from DEFAULT_TERM
# Each term in the form k*b0^e0*b1^e1*...bA^eA
# Represented as: {k: k_value, term:{
# b0: e0,
# ...
# bA, eA
# }}
class Term(object):
  def __init__(self, dimensions = None, term = None):
    if (dimensions and term):
      self.term = term
      self.dimensions = dimensions
    else:
      if (dimensions):
        randParams = genRandomTerm(dimensions)
      else:
        randParams = genRandomTerm()
        
      self.term = randParams["term"]
      self.constant = randParams["constant"]
      self.dimensions = len(self.term.keys())
  
  # Given an array of that matches the dimensions, evaulate based on the definiton of the term
  # Assumes that the array stores the variables form b0 - bN in order
  def evaluate(self, arr):
    solution = None
    term = self.term
    constant = self.constant
    for index, value in enumerate(arr):
      baseKey = "b%d" %index
      if (solution):
        solution *= value ** term[baseKey]
      else:
        solution = float(value) ** term[baseKey]

    return constant*solution

# Helper Functions

# Generates a random term 
def genRandomTerm(dimension = None):
  if (dimension):
    numTerms = dimension
  else:
    numTerms = randint(1, DEFAULT_TERM["MAX_DIMENSIONS"])
  term = {}
  for i in range(numTerms):
    baseKey = "b%d" %i
    exp = randint(0, DEFAULT_TERM["MAX_POWER"])
    term[baseKey] = exp
  constant = randint(DEFAULT_TERM["MIN_CONSTANT"], DEFAULT_TERM["MAX_CONSTANT"])

  return {"term": term, "constant": constant} 

# Generates a random Function by generating random terms
def genRandomFunction():
  numTerms = randint(1, DEFAULT_FUNCTION["MAX_TERMS"])
  numDimensions = randint(1, DEFAULT_TERM["MAX_DIMENSIONS"])
  terms = []
  for i in range(numTerms):
    curTerm = Term(numDimensions)
    terms.append(curTerm)
  return terms

# Calculate range that we should iterate through to find max using brute force to verify the GA solution using parameter 
# set in DEFAULT_PROBLEM as the absolute value of the total number of iterations that should be done.
# I assumed that the ideal range is equally distrubuted between negative and positives (i.e. 2000 range is from -1000 to 1000)
def getFeasibleRange(dimensions):
  return int(((DEFAULT_PROBLEM["MAX_ITERATION"] ** (1/float(dimensions))-1)/2))

# Recursive formulation for going through every possible point combination of n dimensions to solve for global maxium
def bruteForceSolve(curDimension, vector, maxDimension, maxRange, function):
  # Base case
  if (curDimension > maxDimension):
    return function.evaluate(vector), vector

  # Recursively call all possible values for vector
  globalMax = None
  globalMaxVector = None
  while (vector[curDimension -1] <= maxRange):
    newVector = list(vector)
    maxSolution, maxVector = bruteForceSolve(curDimension + 1, newVector, maxDimension, maxRange, function)
    if (not globalMax):
      globalMax = maxSolution
      globalMaxVector = maxVector
    elif (maxSolution > globalMax):
      globalMax = maxSolution
      globalMaxVector = maxVector
    vector[curDimension - 1] += 1

  return globalMax, globalMaxVector

