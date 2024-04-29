import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec
from FTCS import FTCS_temporel, FTCS_temporel_cyl
from conditions_initial import T_init_cubiques_tridimension, T_init_cyl
import time
import warnings

#CARTÉSIEN
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
    ax1.set_title('Volume de température', y=-0.1, fontsize=16)

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
    cbar = fig.colorbar(C, label='Température [C]', fraction=0.046, pad = 0.04, location = 'right', 
                        ticks=np.arange(T_celsius.min(), T_celsius.max()+1, 1))
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(12)
    return plt

def animate_cart(k):
    plotheatmap(T_celsius[k], k)

def transfert_thermique_cart(matrice_temp, largeur_mur, dim_x, dim_y, dim_z, facteur_dimension, cap, delta_t, k_fin, k_init):
    '''
    Si on veut uniquement les valeurs à l'équilibre : k_fin = -1, k_init = -2
    Si on veut les valeurs en transition : k_fin = temps_iter-1, k_init = 0
    '''
    q_fin = np.subtract(matrice_temp[k_fin, :, :, :], matrice_temp[k_init, :, :, :])
    q_fin[largeur_mur:-largeur_mur,largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 0
    Q_fin = q_fin[1:dim_x-1, 1:dim_y-1, 1: dim_z-1]
    
    #capacité thermique volumique [kJ/m³K]
    cap_dm = cap/facteur_dimension**3
    q_beton = cap_dm*(Q_fin.sum())/((k_fin-k_init)*delta_t)
    print(k_fin, k_init, (k_fin-k_init)*delta_t)

    return q_beton

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
    cbar = fig_cyl.colorbar(im, label='Température [C]', fraction=0.046, pad = 0.04, location = 'right',
                             ticks=np.arange(T_cyl_celsius.min(), T_cyl_celsius.max()+1, 1))
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(12)
    return plt

def animate_cyl(k):
    plotheatmap_cyl(T_cyl_celsius[k], k)

def transfert_thermique_cyl(matrice_temp, largeur_mur, dim_base, dim_z, facteur_dimension, cap, delta_t, k_fin, k_init):
    '''
    Si on veut uniquement les valeurs à l'équilibre : k_fin = -1, k_init = -2
    Si on veut les valeurs en transition : k_fin = temps_iter-1, k_init = 0
    '''
    q_fin = np.subtract(matrice_temp[k_fin, :, :], matrice_temp[k_init, :, :])
    q_fin[largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 0
    Q_fin = q_fin[1:dim_base-1, 1: dim_z-1]

    
    q_int = Q_fin[int((2*longueur_r-2)/2):, :]
    som_q_3D = 0
    for i, row in enumerate(q_int):
        for element in row:
            som_q_3D += (i+0.5)*element*2*np.pi

    #capacité thermique volumique [kJ/m³K]
    cap_dm = cap/facteur_dimension**3
    q_beton = cap_dm*som_q_3D/((k_fin-k_init)*delta_t)
    print(k_fin, k_init, (k_fin-k_init)*delta_t)

    return q_beton


#CARTÉSIEN
#Dimensions de la maison, [dm]
largeur = 117
longueur = 117
hauteur = 50
largeur_mur = 5  #donc les murs ont 4 dm de largeur
#Variables
temps_iter = 70
facteur_dimension = 10 #si on a des dm, il y a 10 dm dans 1 m
alpha = 0.155*1e-6*facteur_dimension**2 #béton: 0.54 m²/s, laine de verre: 0.58 m²/s, liège: 0.115 m²/s
delta_x = 1
delta_t = (delta_x**2)/(6*alpha)    #Pour la stabilité, delta_t <= delta**2/2*alpha
y_plan = int(longueur/2)
cap_béton = 280 #kJ/m³K  #béton: 2 500, laine de verre: 17, liège: 280

#Créer l'espace 3D
X, Y, Z = np.meshgrid(np.arange(largeur), np.arange(longueur), np.arange(hauteur))
x, y, z = np.meshgrid(np.arange(1, largeur-1), np.arange(1, longueur-1), np.arange(1, hauteur-1))

#Paramètres cylindriques
longueur_r = 66 #doit être pair
delta_r = 1

val_cart = input("Voulez-vous une simulation cartésienne? [Oui/ Non] ")
if val_cart == "Oui" or val_cart == "OUI" or val_cart == "oui":
    val_saison_cart = input("Quelle saison? [H/E] ")
    if val_saison_cart == "H" or val_saison_cart == "h":
        T_elements = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, 'hiver')
        var_saison = "hiver"
    elif val_saison_cart == "E" or val_saison_cart == "e":
        var_saison = "été"
        T_elements = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, 'été')

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

    fig = plt.figure(figsize=(15,10))

    anim = animation.FuncAnimation(fig, animate_cart, interval=1, frames=temps_iter, repeat = False) #J'ai mis false ici sinon même en fermant la fenetre le reste du code ne roule pas
    # Show Figure
    anim.save(f'/home/alicecalice/Documents/Physique numérique/git2/Conduction_3D_et_2D_VERRE_{var_saison}.gif', fps=2)

    plt.show()

    q_beton_trans = transfert_thermique_cart(T, largeur_mur, largeur, longueur, hauteur, facteur_dimension, cap_béton, delta_t, temps_iter-1, 0)
    print('transfert thermique VERRE transition', q_beton_trans, 'kW')

    q_beton = transfert_thermique_cart(T, largeur_mur, largeur, longueur, hauteur, facteur_dimension, cap_béton, delta_t, -1, -2)
    print('transfert thermique VERRE équilibre', q_beton, 'kW')



val_cyl = input("Voulez-vous une simulation cylindrique? [Oui/ Non] ")
if val_cyl == "Oui" or val_cyl == "OUI" or val_cyl == "oui":
    val_saison_cyl = input("Quelle saison? [H/E] ")
    if val_saison_cyl == "H" or val_saison_cyl == "h":
            T_cyl_elements = T_init_cyl(temps_iter, longueur_r, hauteur, largeur_mur, facteur_dimension, 'hiver')
            var_saison = "hiver"
    elif val_saison_cyl == 'E' or val_saison_cyl == 'e':
        T_cyl_elements = T_init_cyl(temps_iter, longueur_r, hauteur, largeur_mur, facteur_dimension, 'été')
        var_saison ="été"

    T_cyl, temps = FTCS_temporel_cyl(T_cyl_elements, longueur_r, hauteur, temps_iter, alpha, delta_r, delta_t, largeur_mur)
    T_cyl_celsius = T_cyl - 273
    print('CYLINDRIQUE, temps : ', round(temps, 2), ' s')

    fig_cyl = plt.figure(figsize=(10,10))

    anim = animation.FuncAnimation(fig_cyl, animate_cyl, interval=1, frames=temps_iter, repeat=False) #J'ai mis false ici sinon même en fermant la fenetre le reste du code ne roule pas
    #     # # Show Figure
    anim.save(f'/home/alicecalice/Documents/Physique numérique/git2/Conduction_cylindrique_LIÈGE_{var_saison}.gif', fps=2)

    plt.show()

    q_beton_cyl_trans = transfert_thermique_cyl(T_cyl, largeur_mur, 2*longueur_r, hauteur, facteur_dimension, cap_béton, delta_t, temps_iter-1, 0)
    print('transfert thermique LIÈGE CYLINDRIQUE transition', q_beton_cyl_trans, 'kW')

    q_beton_cyl = transfert_thermique_cyl(T_cyl, largeur_mur, 2*longueur_r, hauteur, facteur_dimension, cap_béton, delta_t, -1, -2)
    print('transfert thermique LIÈGE CYLINDRIQUE équilibre', q_beton_cyl, 'kW')



