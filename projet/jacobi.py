import numpy as np
import matplotlib.pyplot as plt
from main import *

plate_length = 100
def conditions_init2D(u_top, u_gauche, u_droit, u_bas):
    u = np.zeros([plate_length + 1, plate_length + 1], float)

    # Conditions initials

    # Imposer les conditions limites a U 
    u[(plate_length):, :] = u_top
  #  u[:, :1] = u_gauche
    u[:1, :] = u_bas
  #  u[:, (plate_length):] = u_droit
    u_prime = np.zeros([plate_length+1, plate_length+1])
    return u, u_prime

def jacobi(u, u_prime, n):
    x = 0    

    while x < n:
        for i in range(1, plate_length + 1):
            for j in range(1, plate_length + 1):
                if i == 0 or i == plate_length or j == 0 or j == plate_length:
                    u_prime[i,j]=u[i,j]
                else:
                    u_prime[i, j] =  (u[i+1, j] + u[i-1, j] + u[i, j+1] + u[i, j-1])/4
        u, u_prime = u_prime.copy(), u.copy()  
        x += 1
    return u

def plot(u):
  plt.clf()
  plt.title(f"Temperature")
  plt.xlabel("x")
  plt.ylabel("y")
  plt.pcolormesh(u, cmap=plt.cm.jet, vmin=0, vmax=100)
  plt.colorbar()
  plt.show()
  return plt

u_ini, u_prime = conditions_init2D(100, 0, 0, 0)
u = jacobi(u_ini, u_prime, 1000)
plot(u)