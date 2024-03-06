import numpy as np

def householder_qr(A):
    m, n = A.shape
    R = np.copy(A)
    Q_matrice = []
    for i in range(n):
        x = R[i:, i]
        norm_x = np.linalg.norm(x)
        signe = 1 if x[0] >= 0 else -1
        e_1 = np.array([1 if j == 0 else 0 for j in range(len(x))])
        v = (signe * norm_x * e_1) + x
        denominator = np.dot(v, v)
        if denominator == 0:
            H = np.eye(len(x))
        else:
            H = np.eye(len(x)) - 2 * np.outer(v, v) / denominator
        Q_i = np.eye(m)
        Q_i[i:, i:] = H
        
        # Update the relevant submatrix of R
        R[i:, :] = np.dot(Q_i, R[i:, :]) 
        
        Q_matrice.append(Q_i)
    Q = np.transpose(Q_matrice[0])
    for i in Q_matrice[1:]:
        Q = np.matmul(Q, np.transpose(i))
    return Q, R

A = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])

print(householder_qr(A))
