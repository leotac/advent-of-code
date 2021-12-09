import numpy as np

def main(filename):
    H = []
    for l in open(filename):
        H.append([int(x) for x in l.strip()])
    H = np.array(H)
    
    # Find minima
    D = np.sign(np.diff(H, axis=0, append=10)) - np.sign(np.diff(H, axis=0, prepend=10)) + np.sign(np.diff(H, axis=1, append=10)) - np.sign(np.diff(H, axis=1, prepend=10))
    minima = (D==4)
    risk = np.sum(H[minima] + 1)


    peaks = (H==9)
    num_basins = np.sum(minima)
    H[peaks] = 99999
    H[~peaks] = -1
    H[minima] = range(num_basins) #initialize label in each minimum 
    closed = np.zeros(H.shape, dtype=bool)
    closed[peaks] = True
    
    # Stupid label propagation to find connected components
    while ~closed.all():
        for i,j in zip(*np.where( (H!=-1) & ~closed)):
            label = H[i,j]
            if i > 0 and H[i-1,j] == -1:
                H[i-1,j] = label
            if i < H.shape[0]-1 and H[i+1,j] == -1:
                H[i+1,j] = label
            if j > 0 and H[i,j-1] == -1:
                H[i,j-1] = label
            if j < H.shape[1]-1 and H[i,j+1] == -1:
                H[i,j+1] = label
            closed[i,j] = True

    basin_size = [np.sum(H == b) for b in range(num_basins)]
    return risk, np.product(sorted(basin_size)[-3:])

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
