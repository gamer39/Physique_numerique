import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec


#Dimensions de la maison, [m]
largeur = 10
longueur = 10
hauteur = 10

#Créer l'espace 3D
X, Y, Z = np.meshgrid(np.arange(largeur), np.arange(longueur), np.arange(hauteur))
x, y, z = np.meshgrid(np.arange(1, largeur-1), np.arange(1, longueur-1), np.arange(1, hauteur-1))

#Variables
temps_iter = 50
alpha = 15.89*1e-6 #du cahier de transfert thermique, à 300 K = 27 C, [m²/s] p.61
delta_x = 1
delta_t = (delta_x**2)/(6*alpha)    #Pour la stabilité, delta_t <= delta**2/6*alpha

#Initialisation de la matrice T(k, d, l, h)
T = np.empty((temps_iter, largeur, longueur, hauteur))

#Initialisation des conditions internes
T_initial = 0
T.fill(T_initial)

T_haut = 100
T_bas = 0
T_gauche = 0
T_droite = 50
T_avant = 0
T_arrière = 50


T[:, :1, :, :] = T_gauche
T[:, (largeur-1):, :, :] = T_droite

T[:, :, :1, :] = T_avant
T[:, :, (longueur-1):, :] = T_avant

T[:, : , :, (hauteur-1):] = T_haut
T[:, :, :, :1] = T_bas

def calcul_profil(T):
    for k in range(0, temps_iter-1, 1):   #range(start, stop, step)
        for d in range(1, largeur-1, delta_x):
            for l in range(1, longueur-1, delta_x):
                for h in range(1, hauteur-1, delta_x):
                    T[k+1, d, l, h] = (alpha*delta_t/delta_x**2)*(T[k][d+1][l][h] + T[k][d-1][l][h] 
                                                                  + T[k][d][l+1][h] + T[k][d][l-1][h] 
                                                                  + T[k][d][l][h+1] + T[k][d][l][h-1] 
                                                                  - 6*T[k][d][l][h]) + T[k][d][l][h]

    return T

def plotheatmap(T_k, k):
    plt.clf()   #clear figure pour en refaire 
    
    plt.title(f"Température à t = {k*delta_t:.2f} s")

    gs = gridspec.GridSpec(1, 2, width_ratios=[1,2]) 
    plt.axis('off')
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], projection='3d')

    ax0.set_xlabel('x')
    ax0.set_ylabel('z')
    ax0.set_xlim(0, largeur)
    ax0.set_ylim(0, hauteur)
    ax0.set_xticks(np.arange(largeur))
    ax0.set_yticks(np.arange(hauteur))
    ax0.set_aspect('equal', adjustable='box')
    ax0.set_title(f'Profil de température pour y = {y_plan} m', y=-0.2)

    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    ax1.set_xlim(0, largeur)
    ax1.set_ylim(0, longueur)
    ax1.set_zlim(0, hauteur)
    ax1.set_title('Volume de température à 1 m à l\'intérieur', y=-0.1)

    ax0.pcolormesh(T[k, :, y_plan, :].transpose(), cmap=plt.cm.jet)   #transpose si on veut x_z
    
    #Plot contour surfaces pour un cube à 1m de distance vers l'intérieur des murs
    _ = ax1.contourf(
        x[:, :, 0], y[:, :, 0], T[k, 1:-1, 1:-1, -2],
        zdir='z', offset=z.max(), **kw,  cmap=plt.cm.jet
    )
    _ = ax1.contourf(
        x[0, :, :], T[k, 1:-1, 1, 1:-1], z[0, :, :],
        zdir='y', offset=1, **kw,  cmap=plt.cm.jet
    )
    C = ax1.contourf(
        T[k,-2,1:-1, 1:-1], y[:, -1, :], z[:, -1, :],
        zdir='x', offset=x.max(), **kw, cmap=plt.cm.jet
    )
    fig.colorbar(C, label='Température [K]')

    return plt

def animate(k):
    plotheatmap(T[k], k)

T = calcul_profil(T)
y_plan = int(longueur/2)

kw = {
    'vmin': T.min(),
    'vmax': T.max(),
    'levels': np.linspace(T.min(), T.max(), 100),  #100 pour la graduation de la colorbar
}

fig = plt.figure(figsize=(15,15))

anim = animation.FuncAnimation(fig, animate, interval=1, frames=temps_iter, repeat=False)
# Show Figure
anim.save('/home/alicecalice/Documents/Physique numérique/Conduction_3D_et_2D.gif')
plt.show()