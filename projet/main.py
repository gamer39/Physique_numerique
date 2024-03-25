import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

max_iter_time = 1000
plate_length = 50

alpha = 2.0
delta_x = 1

delta_t = (delta_x ** 2)/(4 * alpha)
gamma = (alpha * delta_t) / (delta_x ** 2)

def conditions_init2D(u_top, u_gauche, u_droit, u_bas, u_init):
    u = np.empty((max_iter_time, plate_length, plate_length))

    # Conditions initials
    u.fill(u_init)

    # Imposer les conditions limites a U 
    u[:, (plate_length-1):, :] = u_top
    u[:, :, :1] = u_gauche
    u[:, :1, 1:] = u_bas
    u[:, :, (plate_length-1):] = u_droit
    return u

