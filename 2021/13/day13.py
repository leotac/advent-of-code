import numpy as np

def plot(X):
    for r in np.where(X.T,'█',' '):
        print(''.join(r))

def fold(X, idx, dim):
    assert X.shape[dim] // 2 == idx
    if dim == 0:
        return X[:idx,:] | X[:idx:-1,:]
    else:
        return X[:,:idx] | X[:,:idx:-1]

def main(filename):
    coords = np.array([[int(x) for x in l.strip().split(',')] for l in open(filename) if ',' in l])
    folds = np.array([l.strip().split()[-1] for l in open(filename) if 'fold' in l])
    
    I,J = coords.max(axis=0) + 1
    X = np.zeros((I,J+2), dtype=bool) # there's a bug in my input
    X[coords[:,0], coords[:,1]] = 1
    
    for i,f in enumerate(folds):
        dim, idx = f.split('=')
        X = fold(X, int(idx), 0 if dim=='x' else 1)
        if i == 0: print(X.sum())
    plot(X)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    main(filename)
