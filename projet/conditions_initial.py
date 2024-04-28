import  numpy as np
import time




def températures_ext(largeur, facteur_dimension, saison):
    '''
    saison: str, 'été' ou 'hiver'
    '''
    #Commence à 1m sous terre
    gradient = []
    if saison == 'hiver':
        grad = [-3, 0, 4, 6, 7, 7.5, 8]
    elif saison == 'été':
        grad = [22, 16, 13, 11, 10, 9, 8]
    
    gradient = []
    for i in range(len(grad)-1):
        gradient += list(np.linspace(grad[i], grad[i+1], facteur_dimension))
  
    for i in range(largeur-len(gradient)):
        gradient.append(8)
    gradient = [g+273 for g in gradient]
    return gradient[:largeur]



def T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, saison):

    gradient = températures_ext(largeur, facteur_dimension, saison)
    T_haut = gradient[0]
    T_bas = gradient[-1] 
    T_gauche = list(reversed(gradient))
    T_droite = list(reversed(gradient))
    T_avant = list(reversed(gradient))
    T_arrière = list(reversed(gradient))

    #Initialisation de la matrice T(k, d, l, h)
    T = np.zeros((temps_iter, largeur, longueur, hauteur))

    #Initialisation des conditions internes
    T_initial = (min(gradient)+max(gradient))/2
    T.fill(T_initial)

    #Commence à 1m sous terre
    #Températures de la couche de terre autour
    T[:, :1, :, :] = T_gauche
    T[:, (largeur-1):, :, :] = T_droite

    T[:, :, :1, :] = T_avant
    T[:, :, (longueur-1):, :] = T_arrière

    T[:, : , :, (hauteur-1):] = T_haut
    T[:, :, :, :1] = T_bas

    #Limites intérieures des murs
    T[:, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 293

    T_3D = np.zeros((largeur, longueur, hauteur))
    T_3D.fill(T_initial)

    T_3D[ :1, :, :] = T_gauche
    T_3D[(largeur-1):, :, :] = T_droite

    T_3D[ :, :1, :] = T_avant
    T_3D[ :, (longueur-1):, :] = T_arrière

    T_3D[ : , :, (hauteur-1):] = T_haut
    T_3D[ :, :, :1] = T_bas
    
    T_3D[largeur_mur:-largeur_mur, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 293
    return T, T_3D

def T_init_cyl(temps_iter, longueur_r, hauteur, largeur_mur, facteur_dimension, saison):
    gradient = températures_ext(hauteur, facteur_dimension, saison)
    T_cyl_haut = gradient[0] 
    T_cyl_bas = gradient[-1] 
    T_cyl_ext = list(reversed(gradient))

    #Initialisation de la matrice T_cyl(k, i, h, j): temps, rayon, hauteur, orientation
    T_cyl = np.zeros((temps_iter, 2*longueur_r, hauteur))

    #Initialisation des conditions internes
    T_initial = gradient[0]
    T_cyl.fill(T_initial)

    #Limites extérieures
    T_cyl[:, (2*longueur_r-1):, :] = T_cyl_ext
    T_cyl[:, :1, :] = T_cyl_ext
    T_cyl[:, :, :1] = T_cyl_bas
    T_cyl[:, :, (hauteur-1):] = T_cyl_haut
    #Limite intérieure
    T_cyl[:, largeur_mur:-largeur_mur,largeur_mur:-largeur_mur] = 273+20
    return T_cyl

