import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from main import *

room_length = 10
room_width = 10
room_height = 10

def conditions_init3D(u_top, u_bottom, u_left, u_right, u_front, u_back):
    u = np.zeros((room_length + delta_x, room_width + delta_x, room_height + delta_x), float)

    u[room_length, :, :] = u_top  
    u[0, :, :] = u_bottom  
    u[:, 0, :] = u_left  
    u[:, room_width, :] = u_right  
    u[:, :, 0] = u_front  
    u[:, :, room_height] = u_back  

    u_prime = np.zeros((room_length + delta_x, room_width + delta_x, room_height + delta_x), float)
    return u, u_prime

def jacobi3D(u, u_prime, n):
    x = 0
    k = 0
    while x < n:
        for i in range(1, room_length+delta_x):
            for j in range(1, room_width+delta_x):
                for k in range(1, room_height+delta_x):
                    if i == 1 or i == room_length or j == 1 or j == room_width or k == 1 or k == room_height:
                        u_prime[i,j]=u[i,j]
                    else:
                        u_prime[i, j, k] =(u[i+delta_x, j, k] + u[i-delta_x, j, k] + u[i, j+delta_x, k] + u[i, j-delta_x, k] + u[i, j, k+delta_x] + u[i, j, k-delta_x])/6

        u, u_prime = u_prime.copy(), u.copy()
        x += 1
        k += 1
    return u

def plot3D(u):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y, Z = np.meshgrid(range(room_length + delta_x), range(room_width + delta_x), range(room_height + delta_x))
    ax.scatter(X, Y, Z, c=u, cmap=plt.cm.jet)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Température')
    plt.show()

u_ini, u_prime = conditions_init3D(100, 0, 0, 0, 0, 0)
u = jacobi3D(u_ini, u_prime, 500)
plot3D(u)
