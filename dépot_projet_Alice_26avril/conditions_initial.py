import  numpy as np
import time
def températures_ext(largeur, saison):
    '''
    saison: str, 'été' ou 'hiver'
    '''
    #Commence à 1m sous terre
    T_haut = 273
    T_bas = 273+8
    if saison == 'hiver':
        gradient = [-3, 0, 4, 6, 7, 7.5, 8]
    elif saison == 'été':
        gradient = [22, 16, 13, 11, 10, 9, 8]
    for i in range(largeur-len(gradient)):
        gradient.append(8)
    T_gauche = [273+g for g in list(reversed(gradient))]
    T_droite = [273+g for g in list(reversed(gradient))]
    T_avant = [273+g for g in list(reversed(gradient))]
    T_arrière = [273+g for g in list(reversed(gradient))]
    return(T_haut, T_bas, T_gauche, T_droite, T_avant, T_arrière)



def T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, saison):

    T_haut, T_bas, T_gauche, T_droite, T_avant, T_arrière = températures_ext(largeur, saison)

        #Initialisation de la matrice T(k, i, j)
    #Initialisation de la matrice T(k, d, l, h)
    T = np.empty((temps_iter, largeur, longueur, hauteur))

    #Initialisation des conditions internes
    T_initial = 273+20
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
    T[:, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur, largeur_mur:-largeur_mur] = 273+20

    #Créer une matrice 3D sans le temps, pour itérer en boucle while
    A = np.empty((largeur, longueur, hauteur))
    A.fill(273+20)
    A[ :1, :, :] = T_gauche
    A[ (largeur-1):, :, :] = T_droite

    A[ :, :1, :] = T_avant
    A[ :, (longueur-1):, :] = T_avant

    A[ : , :, (hauteur-1):] = T_haut
    A[ :, :, :1] = T_bas
    return T, A
    
