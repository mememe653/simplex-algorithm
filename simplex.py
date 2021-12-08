import numpy as np

def phase_one(A, b, c, z0):
    d = np.array([sum(A)])
    u0 = -np.array([sum(b.T)])
    tableau = np.concatenate((A, b.T), axis=1)
    temp = np.concatenate((-c, z0.T), axis=1)
    tableau = np.concatenate((tableau, temp), axis=0)
    temp = np.concatenate((-d, u0.T), axis=1)
    tableau = np.concatenate((tableau, temp), axis=0)

    eps = 1e-6
    print(d[0])
    while u0 < -eps:
        for j, el in enumerate(d[0]):
            if el > 0:
                break
        temp = b / A[:, j]
        min_el = 1e6
        min_idx = -1
        for i, el in enumerate(temp):
            if A[i, j] > 0 and temp[0, i] < min_el:
                min_el = temp[i]
                min_idx = i
        i = min_idx
        pivot(tableau, i, j)
        A = tableau[:-2, :-1]
        b = np.array([tableau[:-2, -1]])
        c = -np.array([tableau[-2, :-1]])
        z0 = np.array([[tableau[-2, -1]]])
        d = -np.array([tableau[-1, :-1]])
        u0 = np.array([[tableau[-1, -1]]])
    
    return A, b, c, z0

def phase_two(A, b, c, z0):
    tableau = np.concatenate((A, b.T), axis=1)
    temp = np.concatenate((-c, z0.T), axis=1)
    tableau = np.concatenate((tableau, temp), axis=0)

    while np.any(c > 0):
        for j, el in enumerate(c[0]):
            if el > 0:
                break
        temp = b / A[:, j]
        min_el = 1e6
        min_idx = -1
        for i, el in enumerate(temp):
            if A[i, j] > 0 and temp[i] < min_el:
                min_el = temp[i]
                min_idx = i
        i = min_idx
        pivot(tableau, i, j)
        A = tableau[:-1, :-1]
        b = tableau[:-1, -1]
        c = -tableau[-1, :-1]
        z0 = tableau[-1, -1]
    
    return A, b, c, z0

def pivot(tableau, i, j):
    tableau[i, :] = tableau[i, :] / tableau[i, j]
    for row_idx, _ in enumerate(tableau):
        if row_idx != i:
            tableau[row_idx, :] -= tableau[row_idx, j] * tableau[i, :]

if __name__ == '__main__':
    A = np.array([[1, -1, 0, -2, 0],
                  [1, 1, 2, 0, 0],
                  [0, -1, 0, 1, 1]])
    b = np.array([[0, 4, 2]])
    c = np.array([[0, 2, 1, 6, 0]])
    z0 = np.array([[2]])

    A, b, c, z0 = phase_one(A, b, c, z0)
    A, B, c, z0 = phase_two(A, b, c, z0)

    print(z0)