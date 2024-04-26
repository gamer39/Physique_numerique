import numpy as np
from scipy.sparse import diags

# Parameters
alpha = 22.5*1e-6 
L = 10     
Nx = Ny = Nz = L + 1  
dx = dy = dz = 1.0    
dt = 0.01              
num_steps = 100      
T_initial = 0         
T_boundary = 100      

# Set boundary conditions


A = alpha*dt/(2*dx**2)
B = alpha*dt/(2*dy**2)
C = alpha*dt/(2*dz**2)
#####Création matrice diagonale: 
def Matrice_diago(facteur, N):
   
     matrice = np.zeros((N,N))
     for i in range(N-1):
        for j in range(N-1):
            if j == i:
                matrice[i,j] = 1+2*facteur

                matrice[i+1, j] = facteur
                matrice[i, j+1] = facteur
     matrice[N-1, N-1] = 1+2*facteur

     return(matrice)

print(Matrice_diago(A, 4))
