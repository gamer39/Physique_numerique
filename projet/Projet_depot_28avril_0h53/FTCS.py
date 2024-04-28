import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def FTCS_temporel(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur):
    start = time.perf_counter()
    a = 0
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    if d in range(largeur_mur+1, hauteur-largeur_mur-1) and l in range(largeur_mur+1, hauteur-largeur_mur-1) and h in range(largeur_mur+1, hauteur-largeur_mur-1):
                        a+=1
                        pass
                    else:
                        T[k+1, d, l, h] = (alpha*delta_t/delta_x**2)*(T[k][d+1][l][h] + T[k][d-1][l][h] 
                                                                  + T[k][d][l+1][h] + T[k][d][l-1][h] 
                                                                  + T[k][d][l][h+1] + T[k][d][l][h-1] 
                                                                  - 6*T[k][d][l][h]) + T[k][d][l][h]
                    T[k+1, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur]=273+20
    end = time.perf_counter()
    print('CARTÉSIEN, on pass', a, 'fois')
    return T, round(end-start,2)


def FTCS_temporel_cyl(T_cyl, longueur_r, hauteur, temps_iter, alpha, delta_r, delta_t, largeur_mur):
    start = time.perf_counter()
    a = 0
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for i in range(1, 2*longueur_r-1, delta_r):
            for h in range(1, hauteur-1, delta_r):
                if h in range(largeur_mur, hauteur-largeur_mur) and i in range(largeur_mur, hauteur-largeur_mur):
                    a+=1
                    pass
                else:
                    T_cyl[k+1, i, h] = (alpha*delta_t/delta_r**2)*((1+delta_r/longueur_r) *T_cyl[k][i+1][h]+ T_cyl[k][i-1][h]
                                                                +T_cyl[k][i][h+1] + T_cyl[k][i][h-1]
                                                                -(4+delta_r/longueur_r)*T_cyl[k][i][h]) + T_cyl[k][i][h]
                T_cyl[:, largeur_mur:-largeur_mur,largeur_mur:-largeur_mur] = 273+20
    end = time.perf_counter()
    print('CYLINDRIQUE, on pass', a, 'fois')
    return T_cyl, end-start


def FTCS_cart_convergence(A, B, précision,largeur, longueur, hauteur, alpha, delta_t, delta_x, largeur_mur):
    delta_matrix = 1
    k = 0
    sum_temp = 0
    start = time.perf_counter()
    while delta_matrix >= précision:
        k += 1
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    B[d, l, h] = (alpha*delta_t/delta_x**2)*(A[d+1][l][h] + A[d-1][l][h] 
                                                                + A[d][l+1][h] + A[d][l-1][h] 
                                                                + A[d][l][h+1] + A[d][l][h-1] 
                                                                - 6*A[d][l][h]) + A[d][l][h]
        delta_matrix = np.max(abs(A - B))
        b = B.copy()
        b[largeur_mur:-largeur_mur,largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 0
        C = b[1:largeur-1, 1:longueur-1, 1: hauteur-1]
    
        sum_temp+=C.sum()
        A = B.copy()
        

    end = time.perf_counter()
    return A, round(end-start, 2), k, sum_temp

