import numpy as np

def length(x):
    return np.sqrt(x.dot(x))

def unit_vector(x):
    return x / np.linalg.norm(x)