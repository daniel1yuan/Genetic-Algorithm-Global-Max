# @file: Generic math functions
# @author: Daniel Yuan

def normalize(arr):
  max_value = max(map(lambda x: abs(x), arr))
  return map(lambda x: x/float(max_value), arr)
