import numpy as np
import matplotlib.pyplot as plt 
import scipy as sp
from matplotlib import gridspec
import matplotlib.animation as animation
import time
from conditions_initial import T_init_cube_h


#Dimensions de la maison, [dm]
largeur = 100
longueur = 100
hauteur = 100
largeur_mur = 50
#Variables
temps_iter = 30
alpha = 22.5*1e-6 #du cahier de transfert thermique, à 300 K = 27 C, [m²/s] p.61
delta_x = 1
delta_t = (delta_x**2)/(6*alpha)    #Pour la stabilité, delta_t <= delta**2/6*alpha

def Gauss_Seidel_temporel(T, largeur, longueur, hauteur, temps_iter, delta_x):
    omega = 0.1
    target = 10e-5
    a = time.time()
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):

                    T_vieux = [k, d, l, h]    
                    T[k+1, d, l, h]  = (alpha*delta_t/delta_x**2)*(T[k][d+1][l][h] + T[k][d-1][l][h] 
                                                                  + T[k][d][l+1][h] + T[k][d][l-1][h] 
                                                                  + T[k][d][l][h+1] + T[k][d][l][h-1] 
                                                                  - 6*T[k][d][l][h]) + T[k][d][l][h]
                    
                    delta = np.max(abs(T[k+1, d, l, h]-T_vieux))

                    if target > delta:
                        b = time.time()
                        print(f"Temps de simulation: {b-a} s")
                        return (T, k)
        print(delta)
    print("Temps écoulé et aucune convergence trouvé")



def Gauss_Seidel_3D(T, largeur, longueur, hauteur, delta_x): 
    a = time.time()
    omega = 0.9
    T = T[0, :, :, :]
    Tprime=np.zeros_like(T)
    delta = 1
    target = 1e-2

    while delta > target:
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    T_vieux = T[d, l, h]

                    T_neuf = ((1+omega)/6) * (T[d+delta_x, l, h] + T[d-delta_x, l, h] + T[d, l+delta_x, h]
                                                        + T[d, l-delta_x, h] + T[d, l, h+delta_x] 
                                                        + T[d, l, h-delta_x]) \
                                                            -(omega*T_vieux)    
                    T[d, l, h] = T_neuf

        delta = np.max(abs(T_neuf-T_vieux))
    b = time.time()
    print(f"Temps de simulation: {b-a} s")
    return(T)
