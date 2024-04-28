import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
from FTCS import FTCS_temporel, FTCS_temporel_cyl
from conditions_initial import T_init_cubiques_tridimension, T_init_cyl

import time

def plotheatmap(T_k, k):
    plt.clf()   #clear figure pour en refaire 
    
    plt.title(f"Température à t = {k*delta_t:.0f} s, en coordonnées cartésiennes", fontsize=20)

    gs = gridspec.GridSpec(1, 2, width_ratios=[1,2]) 
    plt.axis('off')
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1], projection='3d')

    ax0.set_xlabel('x', fontsize=12)
    ax0.set_ylabel('z', fontsize=12)
    ax0.set_xlim(0, largeur)
    ax0.set_ylim(0, hauteur)
    ax0.set_xticks(np.linspace(0, largeur, 11))
    ax0.set_yticks(np.linspace(0, hauteur, 11))
    ax0.tick_params(axis='both', labelsize=12)
    ax0.set_aspect('equal', adjustable='box')
    ax0.set_title(f'Profil de température pour y = {y_plan} dm', y=-0.3, fontsize=16)

    ax1.set_xlabel('x [dm]', fontsize=12)
    ax1.set_ylabel('y [dm]', fontsize=12)
    ax1.set_zlabel('z [dm]', fontsize=12)
    ax1.tick_params(axis='both', labelsize=12)
    ax1.set_xlim(0, largeur)
    ax1.set_ylim(0, longueur)
    ax1.set_zlim(0, hauteur)
    ax1.set_title('Volume de température', y=-0.2, fontsize=16)

    ax0.pcolormesh(T_celsius[k, :, y_plan, :].transpose(), cmap=plt.cm.turbo)   #transpose si on veut x_z
    
    #Plot contour surfaces pour un cube à 1m de distance vers l'intérieur des murs
    _ = ax1.contourf(
        x[:, :, 0], y[:, :, 0], T_celsius[k, 1:-1, 1:-1, -2],
        zdir='z', offset=z.max(), **kw,  cmap=plt.cm.turbo
    )
    _ = ax1.contourf(
        x[0, :, :], T_celsius[k, 1:-1, 1, 1:-1], z[0, :, :],
        zdir='y', offset=1, **kw,  cmap=plt.cm.turbo
    )
    C = ax1.contourf(
        T_celsius[k,-2,1:-1, 1:-1], y[:, -1, :], z[:, -1, :],
        zdir='x', offset=x.max(), **kw, cmap=plt.cm.turbo
    )
    cbar = fig.colorbar(C, label='Température [C]', fraction=0.046, pad = 0.04, location = 'right')
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(12)
    return plt

def animate_cart(k):
    plotheatmap(T_celsius[k], k)

        
#CARTÉSIEN
#Dimensions de la maison, [dm]
largeur = 50
longueur = 50
hauteur = 50
largeur_mur = 5
#Variables
temps_iter = 5
facteur_dimension = 10 #si on a des dm, il y a 10 dm dans 1 m
alpha = 0.54*1e-6*facteur_dimension**2 #du cahier de transfert thermique, à 300 K = 27 C, [m²/s] p.61
delta_x = 1
delta_t = (delta_x**2)/(6*alpha)    #Pour la stabilité, delta_t <= delta**2/2*alpha
y_plan = int(longueur/2)

#Créer l'espace 3D
X, Y, Z = np.meshgrid(np.arange(largeur), np.arange(longueur), np.arange(hauteur))
x, y, z = np.meshgrid(np.arange(1, largeur-1), np.arange(1, longueur-1), np.arange(1, hauteur-1))



if input("Voulez-vous une simulation cartésienne? [ Oui/ Non] ") == "oui" or input("Voulez-vous une simulation cartésienne? [ Oui/ Non] ") == "oui":
    if input("Quelle saison? [H/E] ") == "H" or "h":
        T_elements, T_3D = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, 'hiver')
        var_saison = "hiver"
    else:
        var_saison = "été"
        T_elements, T_3D = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, 'été')

    ######FTCS ESPACE 3D CUBIQUE
     # Provenant du module conditions_initiales
    T, temps_cart = FTCS_temporel(T_elements, largeur, longueur, hauteur, temps_iter, alpha, delta_x, delta_t, largeur_mur)
    T_celsius = T - 273
    print('CARTÉSIEN, temps =', temps_cart, 's')

    kw = {
        'vmin': T_celsius.min(),
        'vmax': T_celsius.max(),
        'levels': np.linspace(T_celsius.min(), T_celsius.max(), 100),  #100 pour la graduation de la colorbar
    }

    fig = plt.figure(figsize=(10,15))

    anim = animation.FuncAnimation(fig, animate_cart, interval=1, frames=temps_iter, repeat=False) #J'ai mis false ici sinon même en fermant la fenetre le reste du code ne roule pas
    # Show Figure
    anim.save(f'projet/Conduction_3D_et_2D_dm_50x50x50_{var_saison}.gif')

    plt.show()


#CYLINDRIQUE
def plotheatmap_cyl(T_k, k):
    plt.clf()   #clear figure pour en refaire 
    
    plt.title(f"Température à t = {k*delta_t:.0f} s, en coordonnées cylindriques", fontsize=20)

    plt.axis('off')
    ax0 = fig_cyl.add_subplot()

    ax0.set_xlabel('base (2r) [dm]', fontsize=12)
    ax0.set_ylabel('z [dm]', fontsize=12)
    ax0.set_xlim(0, 2*longueur_r)
    ax0.set_ylim(0, hauteur)
    ax0.set_xticks(np.linspace(0, 2*longueur_r, 11))
    ax0.set_yticks(np.linspace(0, hauteur, 11))
    ax0.tick_params(axis='both', labelsize=12)
    ax0.set_aspect('equal', adjustable='box')
    ax0.set_title(f'Profil de température', y=-0.2, fontsize=16)

    im = ax0.pcolormesh(T_cyl_celsius[k, :, :].transpose(), vmin = T_cyl_celsius.min(), vmax = T_cyl_celsius.max() ,cmap=plt.cm.turbo) 
    cbar = fig_cyl.colorbar(im, label='Température [C]', fraction=0.046, pad = 0.04, location = 'right')
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(12)
    return plt

def animate_cyl(k):
    plotheatmap_cyl(T_cyl_celsius[k], k)

#Paramètres
longueur_r = 50
hauteur = 50
largeur_mur = 5
delta_r = 1

if input("Voulez-vous une simulation cylindrique? [ Oui/ Non] ") == "oui" or input("Voulez-vous une simulation cylindrique? [ Oui/ Non] ") == "oui":
    if input("Quelle saison? [H/E] ") == "H" or "h":
        T_cyl_elements = T_init_cyl(temps_iter, longueur_r, hauteur, largeur_mur, facteur_dimension, 'hiver')
        var_saison = "hiver"
    else:
        T_cyl_elements = T_init_cyl(temps_iter, longueur_r, hauteur, largeur_mur, facteur_dimension, 'été')
        var_saison ="été"

    T_cyl, temps = FTCS_temporel_cyl(T_cyl_elements, longueur_r, hauteur, temps_iter, alpha, delta_r, delta_t, largeur_mur)
    T_cyl_celsius = T_cyl - 273
    # print('CYLINDRIQUE, temps : ', round(temps, 2), ' s')

    fig_cyl = plt.figure(figsize=(10,10))

    anim = animation.FuncAnimation(fig_cyl, animate_cyl, interval=1, frames=temps_iter, repeat=False) #J'ai mis false ici sinon même en fermant la fenetre le reste du code ne roule pas
    # # Show Figure
    anim.save(f'projet/Conduction_cylindrique_{var_saison}.gif')

    plt.show()

# T_fin = T[-1, :, :, :].copy()
q_fin = np.subtract(T[-1, :, :, :], T[-2, :, :, :])
q_fin[largeur_mur:-largeur_mur,largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 0
Q_fin = q_fin[1:largeur-1, 1:longueur-1, 1: hauteur-1]

#capacité thermique volumique [kJ/m³K]
cap_beton = 2500/facteur_dimension**3
cap_laine_verre = 17/facteur_dimension**3
q_beton = cap_beton*Q_fin.sum()
# q_verre = cap_laine_verre*Q_fin.sum()
print('transfert thermique BETON', q_beton, 'kW')
# print('transfert thermique LAINE VERRE', q_verre, 'kW')


T_3D_v2 = T_3D.copy()

