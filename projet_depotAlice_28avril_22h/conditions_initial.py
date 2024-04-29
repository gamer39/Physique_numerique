import  numpy as np
from matplotlib import pyplot as plt
import time




def températures_ext(hauteur, facteur_dimension, saison):
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
  
    for i in range(hauteur-len(gradient)):
        gradient.append(8)
    gradient = [g+273 for g in gradient]
    return gradient[:hauteur]



def T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, saison):

    gradient = températures_ext(hauteur, facteur_dimension, saison)
    T_haut = gradient[0]
    T_bas = gradient[-1] 
    T_gauche = list(reversed(gradient))
    T_droite = list(reversed(gradient))
    T_avant = list(reversed(gradient))
    T_arrière = list(reversed(gradient))

    #Initialisation de la matrice T(k, d, l, h)
    T = np.zeros((temps_iter, largeur, longueur, hauteur))

    #Initialisation des conditions internes
    T_initial = 293  #20C
    T.fill(T_initial)

    #Commence à 1m sous terre
    #Températures de la couche de terre autour
    T[:, :largeur_mur, :, :] = T_gauche
    T[:, (largeur-largeur_mur):, :, :] = T_droite

    T[:, :, :largeur_mur, :] = T_avant
    T[:, :, (longueur-largeur_mur):, :] = T_arrière

    T[:, : , :, (hauteur-largeur_mur):] = T_haut
    T[:, :, :, :largeur_mur] = T_bas

    return T

def T_init_cyl(temps_iter, longueur_r, hauteur, largeur_mur, facteur_dimension, saison):
    gradient = températures_ext(hauteur, facteur_dimension, saison)
    T_cyl_haut = gradient[0] 
    T_cyl_bas = gradient[-1] 
    T_cyl_ext = list(reversed(gradient))

    #Initialisation de la matrice T_cyl(k, i, h, j): temps, rayon, hauteur, orientation
    T_cyl = np.zeros((temps_iter, 2*longueur_r, hauteur))

    #Initialisation des conditions internes
    T_initial = 293
    T_cyl.fill(T_initial)

    #Limites extérieures
    T_cyl[:, ((2*longueur_r)-largeur_mur):, :] = T_cyl_ext
    T_cyl[:, :largeur_mur, :] = T_cyl_ext
    T_cyl[:, :, :largeur_mur] = T_cyl_bas
    T_cyl[:, :, (hauteur-largeur_mur):] = T_cyl_haut

    return T_cyl

