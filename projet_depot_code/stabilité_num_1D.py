import numpy as np
from scipy.sparse import diags
import matplotlib.pyplot as plt
from conditions_initial import T_init_cubiques_tridimension
largeur = 50
longueur = 50
hauteur = 50
largeur_mur = 5
#Variables
temps_iter = 300
facteur_dimension = 10 #si on a des dm, il y a 10 dm dans 1 m
alpha = 0.54*1e-6*facteur_dimension**2 #du cahier de transfert thermique, à 300 K = 27 C, [m²/s] p.61
dx = 1
dt = (dx**2)/(6*alpha)    #Pour la stabilité, delta_t <= delta**2/2*alpha



T = T_init_cubiques_tridimension(temps_iter, largeur, longueur, hauteur, largeur_mur, facteur_dimension, 'été')
Tcrank= T[0,0,0,:]
TFTCS = T[0,0,0,:]
Tcrank = Tcrank[:, np.newaxis]


########Méthode de Crank-Nicholson 1D
#####Création matrice diagonale: 

def Crank_Nicholson(T, k, dt):
     A = alpha*dt/dx**2
     N = len(T) 
     matrice_D = np.zeros((N,N))
     matrice_G = np.copy(matrice_D)

     for i in range(1, N-1):
        for j in range(1,N-1):
            if j == i:
                matrice_D[i,j] = 2*(1-A)
                matrice_G[i,j] = 2*(1+A)

                matrice_D[i+1, j] = A
                matrice_D[i, j-1] = A
                matrice_D[i, j+1] = A
                matrice_D[N-1,:] = 0
                
                matrice_G[i+1, j] = -A
                matrice_G[i, j-1] = -A
                matrice_G[i, j+1] = -A
                matrice_G[N-1,:] = 0 

   
     matrice_D[0,0] = 1
     matrice_G[0,0] = 1
     matrice_D[N-1, N-1] = 1
     matrice_G[N-1, N-1] = 1

     for i in range(k):

        produit = np.matmul(matrice_D, T)

        Temp = np.linalg.solve(matrice_G, produit)
        T = Temp

     return(T)

#####Méthode de FTCS 1D
def FTCS_temporel(T, hauteur, alpha, delta_x, delta_t):
    N = hauteur-1
    T[1:N] = (alpha*delta_t/delta_x**2)*( T[0: N-1] + T[2: N +1] - 2*T[1:N])+T[1:N]
    return T




moy_crank=[]
moy_FTCS = []
liste_t = []

for i in range(1,21):
    print(f"itération:{i}")
    dt = (dx**2)/(alpha)*0.15*i
    liste_t.append(i*0.1) 
    T_C = Crank_Nicholson(Tcrank, 10000, dt)
    T_F = FTCS_temporel(TFTCS, hauteur, alpha, dx, dt)
    moy_crank.append(np.average(T_C))
    moy_FTCS.append(np.average(T_F))



plt.figure
plt.minorticks_on()
plt.tick_params(axis="both",direction="in",labelsize='large',which='both',color='black')
plt.plot(liste_t, moy_crank, label="Méthode Crank-Nicolson", linestyle="-")
plt.plot(liste_t, moy_FTCS, label="méthode FTCS ", linestyle="-.")
plt.ylim((200,400))
plt.axvline(x = 1/6, label = "Valeur utilisée en 3D", color="red", linestyle ="dotted")
plt.ylabel("Température moyenne [k]")
plt.xlabel("Incrément dt [dx²/\u03B1]")
plt.legend()
plt.show()



