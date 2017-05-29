# @author: Daniel Yuan
# @file: problems.py
# @breif: Generates problems for global max problems

# Class definiton of a problem
class Problem(object):
  
  # Constructor
  # @params: parameters used to generate a problem in the structure of:
  #   nu
  def __init__(self, params):
    self.params = params
    if (params):
      self.formula = genFormula(params)

  def genFormula(params):
    print "test"
  
