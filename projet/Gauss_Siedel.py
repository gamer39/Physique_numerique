import numpy as np
import matplotlib.pyplot as plt 
import scipy as sp
from matplotlib import gridspec
import matplotlib.animation as animation




def Gauss_Siedel_surrelax(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur):
    omega = 0.1
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    T[k+1, d, l, h] = (1+omega) * ((T[k, d+delta_x, l, h] + T[k, d-delta_x, l, h] + T[k, d, l+delta_x, h]
                                                     + T[k, d, l-delta_x, h] + T[k, d, l, h+delta_x] 
                                                     + T[k, d, l, h-delta_x])/6-(omega*T[k, d, l, h]))
    return T


