# this module will be imported in the into your flowgraph

import numpy as np

def nextPow(arg):
    return(int(2**np.ceil(np.log2(arg))))
