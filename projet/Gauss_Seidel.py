import numpy as np
import matplotlib.pyplot as plt 
import scipy as sp
from matplotlib import gridspec
import matplotlib.animation as animation
import time
from conditions_initial import T_init_cubiques_tridimension
#Dimensions de la maison, [dm]
largeur = 100
longueur = 100
hauteur = 100

largeur_mur = 50
#Variables
temps_iter = 2
alpha = 22.5*1e-6 #du cahier de transfert thermique, à 300 K = 27 C, [m²/s] p.61
delta_x = 1
delta_t = (delta_x**2)/(6*alpha)    #Pour la stabilité, delta_t <= delta**2/6*alpha

def Gauss_Seidel_temporel(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur):
    omega = 0.1
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    T[k+1, d, l, h] = (1+omega) * ((T[k, d+delta_x, l, h] + T[k, d-delta_x, l, h] + T[k, d, l+delta_x, h]
                                                     + T[k, d, l-delta_x, h] + T[k, d, l, h+delta_x] 
                                                     + T[k, d, l, h-delta_x])/6-(omega*T[k, d, l, h]))
    return T


def larger(a, b):
    if a >= b:
        return a
    else:
        return b

def Gauss_Seidel_convergeance(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur): 
    omega = 0.35
    T = T[0, :, :, :]
    Tprime=np.zeros_like(T)
    delta = 1
    target = 10e-5

    while delta > target:
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):

                    Tprime[d, l, h] = (1+omega) * ((T[d+delta_x, l, h] + T[d-delta_x, l, h] + T[d, l+delta_x, h]
                                                        + T[d, l-delta_x, h] + T[d, l, h+delta_x] 
                                                        + T[d, l, h-delta_x])/6-(omega*T[d, l, h]))    
                    T[d, l, h] = Tprime[d, l, h]

        delta = np.max(abs(Tprime-T))
        print(delta)
    return(T)

T = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur)

T = Gauss_Seidel_convergeance(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur)