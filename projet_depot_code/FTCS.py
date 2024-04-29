import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def FTCS_temporel(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur):
    start = time.perf_counter()
    for k in range(0, temps_iter-1, 1):  #dt
        for d in range(1, largeur-1, delta_x): #dx
            for l in range(1, longueur-1, delta_x): #dy
                for h in range(1, hauteur-1, delta_x): #dz
                    if d in range(largeur_mur+1, hauteur-largeur_mur-1) and l in range(largeur_mur+1, hauteur-largeur_mur-1) and h in range(largeur_mur+1, hauteur-largeur_mur-1):
                        pass
                    else:
                        T[k+1, d, l, h] = (alpha*delta_t/delta_x**2)*(T[k][d+1][l][h] + T[k][d-1][l][h] #Algorithme FCTS
                                                                  + T[k][d][l+1][h] + T[k][d][l-1][h] 
                                                                  + T[k][d][l][h+1] + T[k][d][l][h-1] 
                                                                  - 6*T[k][d][l][h]) + T[k][d][l][h]
                    T[k+1, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur]=273+20
        print(f"Itérations cubique temporelle {k}/{temps_iter-1}")
    end = time.perf_counter()
    return T, round(end-start,2)


def FTCS_temporel_cyl(T_cyl, longueur_r, hauteur, temps_iter, alpha, delta_r, delta_t, largeur_mur):
    start = time.perf_counter()
    for k in range(0, temps_iter-1, 1):   
        for i in range(1, (2*longueur_r)-1, delta_r): 
            for h in range(1, hauteur-1, delta_r): 
                if h in range(largeur_mur, hauteur-largeur_mur) and i in range(largeur_mur, hauteur-largeur_mur):
                    pass
                else:
                    T_cyl[k+1, i, h] = (alpha*delta_t/delta_r**2)*((1+delta_r/longueur_r) *T_cyl[k][i+1][h]+ T_cyl[k][i-1][h]
                                                                +T_cyl[k][i][h+1] + T_cyl[k][i][h-1]
                                                                -(4+delta_r/longueur_r)*T_cyl[k][i][h]) + T_cyl[k][i][h]
                T_cyl[:, largeur_mur:-largeur_mur,largeur_mur:-largeur_mur] = 273+20
        print(f"Itérations cylindrique temporelle {k}/{temps_iter-1}")
    end = time.perf_counter()
    return T_cyl, end-start

