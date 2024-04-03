import numpy as np
import matplotlib.pyplot as plt
from main import *

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

def relaxation(u): 
    for k in range(0, max_iter_time-1, 1):
        for i in range(1, plate_length-1, delta_x):
            for j in range(1, plate_length-1, delta_x):
                u[k + 1, i, j] = gamma * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]
    return u

def plot(u_k, k):
  plt.clf()
  plt.title(f"Temperature = {k*delta_t:.3f}")
  plt.xlabel("x")
  plt.ylabel("y")
  plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
  plt.colorbar()
  plt.show()
  return plt

u_ini = conditions_init2D(100, 0, 0, 0, 0)
u = relaxation(u_ini)
k = 9
plot(u[k], k)
