import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
from Elements_finis3D import Éléments_fini3D
from conditions_initial import T_init_cubiques_tridimension, hiver
from Gauss_Siedel import Gauss_Siedel_surrelax

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

#Créer l'espace 3D
X, Y, Z = np.meshgrid(np.arange(largeur), np.arange(longueur), np.arange(hauteur))
x, y, z = np.meshgrid(np.arange(1, largeur-1), np.arange(1, longueur-1), np.arange(1, hauteur-1))



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
    ax0.set_xticks(np.linspace(0, largeur, 10))
    ax0.set_yticks(np.linspace(0, hauteur, 10))
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




######Éléments fini cubiques
T = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur) # Provenant du module conditions_initiales
T = Éléments_fini3D(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur)

y_plan = int(longueur/2)

kw = {
    'vmin': T.min(),
    'vmax': T.max(),
    'levels': np.linspace(T.min(), T.max(), 100),  #100 pour la graduation de la colorbar
}

fig = plt.figure(figsize=(15,15))

anim = animation.FuncAnimation(fig, animate, interval=1, frames=temps_iter, repeat=False)
# Show Figure
#anim.save('/home/alicecalice/Documents/Physique numérique/Conduction_3D_et_2D_dm.gif')

plt.show()



#######Gauss Siegel Cubique
T = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur) # Provenant du module conditions_initiales
T = Gauss_Siedel_surrelax(T, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur)
kw = {
    'vmin': T.min(),
    'vmax': T.max(),
    'levels': np.linspace(T.min(), T.max(), 100),  #100 pour la graduation de la colorbar
}
fig = plt.figure(figsize=(15,15))

anim = animation.FuncAnimation(fig, animate, interval=1, frames=temps_iter, repeat=False)
# Show Figure
#anim.save('projet/3D_finate_difference_method_formeL.py')
plt.show()