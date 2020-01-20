from math import *
import matplotlib 
from matplotlib import pyplot as pp
import numpy as np

empty_canvas = np.zeros((1000,2000)) # 1mm x 1mm grid of surface

light_map_origin = empty_canvas

pp.figure(figsize=(16,9))
pp.axis("off")
pp.imshow(light_map_origin)
pp.show()