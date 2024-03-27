import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

max_iter_time = 20000
plate_length = 100

alpha = 2.0
delta_x = 1

delta_t = (delta_x ** 2)/(4 * alpha)
gamma = 1/ (delta_x ** 2)
k = 0.024 


