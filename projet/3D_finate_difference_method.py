import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

largeur = 10
longueur = 10
hauteur = 10

# Define dimensions
Nx, Ny, Nz = 100, 300, 500
X, Y, Z = np.meshgrid(np.arange(largeur), np.arange(longueur), np.arange(hauteur))
x, y, z = np.meshgrid(np.arange(1, largeur-1), np.arange(1, longueur-1), np.arange(1, hauteur-1))

temps_iter = 50

alpha = 15.89*1e-6 #du cahier de transfert thermique, à 300 K = 27 C, [m²/s] p.61
delta_x = 1
delta_t = (delta_x**2)/(6*alpha)    #15 733

#Initialisation de la matrice T(k, i, j)
T = np.empty((temps_iter, largeur, longueur, hauteur))
#Initialisation des conditions internes
T_initial = 0
T.fill(T_initial)

T_haut = 100
T_bas = 0
T_gauche = 50
T_droite = 50
T_avant = 50
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
    plt.clf()

    plt.title(f"Température à t = {k*delta_t:.2f} s")
    ax = fig.add_subplot(111, projection='3d')

    # Plot contour surfaces
    # _ = ax.contourf(
    #     X[:, :, 0], Y[:, :, 0], T[0, :, :, 0],
    #     zdir='z', offset=0, **kw
    # )
    # _ = ax.contourf(
    #     X[0, :, :], T[0, 0, :, :], Z[0, :, :],
    #     zdir='y', offset=0, **kw
    # )
    # C = ax.contourf(
    #     T[0,:, -1, :], Y[:, -1, :], Z[:, -1, :],
    #     zdir='x', offset=X.max(), **kw
    # )
    # --
    _ = ax.contourf(
        x[:, :, 0], y[:, :, 0], T[k, 1:-1, 1:-1, -2],
        zdir='z', offset=z.max(), **kw,  cmap=plt.cm.jet
    )
    _ = ax.contourf(
        x[0, :, :], T[k, 1:-1, 1, 1:-1], z[0, :, :],
        zdir='y', offset=1, **kw,  cmap=plt.cm.jet
    )
    C = ax.contourf(
        T[k,-2,1:-1, 1:-1], y[:, -1, :], z[:, -1, :],
        zdir='x', offset=x.max(), **kw, cmap=plt.cm.jet
    )

    # Set limits of the plot from coord limits
    xmin, xmax = X.min(), X.max()
    ymin, ymax = Y.min(), Y.max()
    zmin, zmax = Z.min(), Z.max()
    ax.set(xlim=[xmin, xmax], ylim=[ymin, ymax], zlim=[zmin, zmax])

    # Plot edges
    edges_kw = dict(color='0.4', linewidth=1, zorder=1e3)
    ax.plot([xmax, xmax], [ymin, ymax], 0, **edges_kw)
    ax.plot([xmin, xmax], [ymin, ymin], 0, **edges_kw)
    ax.plot([xmax, xmax], [ymin, ymin], [zmin, zmax], **edges_kw)

    # Set labels and zticks
    ax.set(
        xlabel='X [m]',
        ylabel='Y [m]',
        zlabel='Z [m]',
        zticks=np.arange(10),
    )

    # Set zoom and angle view
    ax.view_init(40, -40, 0)
    ax.set_box_aspect(None, zoom=0.9)

    # Colorbar
    fig.colorbar(C, ax=ax, fraction=0.02, pad=0.1, label='Name [units]')
    return plt

def animate(k):
    plotheatmap(T[k], k)

T = calcul_profil(T)

kw = {
    'vmin': T.min(),
    'vmax': T.max(),
    'levels': np.linspace(T.min(), T.max(), 10),
}

# Create a figure with 3D ax
fig = plt.figure(figsize=(10, 10))

anim = animation.FuncAnimation(fig, animate, interval=1, frames=temps_iter, repeat=False)
# Show Figure
anim.save('/home/alicecalice/Documents/Physique numérique/Conduction_3D.gif')
plt.show()