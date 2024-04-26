import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import time

largeur = 50
hauteur = 50

temps_iter = 750

alpha = 15.89*1e-6 #du cahier de transfert thermique, à 300 K = 27 C, p.61
delta_x = 1
delta_t = (delta_x**2)/(4*alpha)    #9.5

#Initialisation de la matrice T(k, i, j)
T = np.empty((temps_iter, largeur, hauteur))

#Initialisation des conditions internes
T_initial = 0
T.fill(T_initial)

#Conditions limites
T_haut = 30.0 + 273.15
T_bas = 0
T_gauche = 273.15
T_droite = 273.15

T[:, (largeur-1), :] = T_haut
T[:, :1, :] = T_bas
T[:, :, :1] = T_gauche
T[:, :, (hauteur-1):] = T_droite


def calcul_profil(T):
    for k in range(0, temps_iter-1, 1):
        for i in range(1, largeur-1, delta_x):
            for j in range(1, hauteur-1, delta_x):
                T[k+1, i, j] = (alpha*delta_t/delta_x**2)*(T[k][i+1][j] + T[k][i-1][j] + T[k][i][j+1] + T[k][i][j-1] - 4*T[k][i][j]) + T[k][i][j]

    return T

def graph(T_k, k):
    plt.clf()

    plt.title(f'Profil de température à t = {k*delta_t:.2f} s')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')

    plt.pcolormesh(T_k, cmap=plt.cm.jet, vmin=0, vmax=315)
    plt.colorbar()

    return plt

def film(k):
    return graph(T[k], k)

T = calcul_profil(T)

anim = FuncAnimation(fig = plt.figure(), func = film, interval=1, frames = temps_iter, repeat=False)
# anim.save('/home/alicecalice/Documents/Physique numérique/Conduction_2D.gif')
plt.show()

print('FINI')