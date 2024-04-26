import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def FTCS_temporel(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur):
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    T[k+1, d, l, h] = (alpha*delta_t/delta_x**2)*(T[k][d+1][l][h] + T[k][d-1][l][h] 
                                                                  + T[k][d][l+1][h] + T[k][d][l-1][h] 
                                                                  + T[k][d][l][h+1] + T[k][d][l][h-1] 
                                                                  - 6*T[k][d][l][h]) + T[k][d][l][h]
                    T[k+1, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur]=273+20

    return T



#def Éléments_fini3D_convergence(T, B, précision,largeur, longueur, hauteur, alpha, delta_t, delta_x):
 #   delta_matrix = 1
  #  A = T[0, :, :, :]
   # k = 0
    #start = time.perf_counter()
    #while delta_matrix >= précision:
    #    k += 1
    #    for d in range(1, largeur-1, delta_x):
    ##        for l in range(1, longueur-1, delta_x):
     #           for h in range(1, hauteur-1, delta_x):
     #               B[d, l, h] = (alpha*delta_t/delta_x**2)*(A[d+1][l][h] + A[d-1][l][h] 
                                                                #+ A[d][l+1][h] + A[d][l-1][h] 
                                                                #+ A[d][l][h+1] + A[d][l][h-1] 
                                                                #- 6*A[d][l][h]) + A[d][l][h]
     #   delta_matrix = np.max(abs(A - B))
     #   A = B.copy()

  #  end = time.perf_counter()
   # return A, round(end-start, 2), k

