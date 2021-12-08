import numpy as np
from tqdm import trange

T = 100

def tick(X):
    X[:, 1, :] += X[:, 2, :] 
    X[:, 0, :] += X[:, 1, :]

def dedup(X):
    positions, counts = np.unique(X[:,0,:], axis=0, return_counts=True)
    dups = np.zeros(X.shape[0], dtype=bool)
    for pos in positions[counts>1]:
        dups |= (X[:,0,:] == pos).all(axis=1)
    return X[~dups,:,:]

def main(filename):
    X = []
    for i,l in enumerate(open(filename)):
        p, v, a = l.strip().split()
        p = np.array([int(x) for x in p[3:-2].split(",")])
        v = np.array([int(x) for x in v[3:-2].split(",")])
        a = np.array([int(x) for x in a[3:-1].split(",")])
        X.append([p, v, a])
    X = np.array(X)
    for t in trange(T):
        tick(X)
        X = dedup(X)
        print(t, X.shape)
    return X.shape[0]

if __name__ == "__main__":
    filename = "data" 
    ret = main(filename)
    print(f"{ret=}") 
