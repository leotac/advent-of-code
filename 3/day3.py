import numpy as np

def main1(filename):
    tot = None
    for l in open(filename):
        if not tot:
            ncols = len(l.strip())
            tot = [0]*ncols
        for i, b in enumerate(l.strip()):
            if b == '1':
                tot[i] += 1
            else:
                tot[i] -= 1
    gamma = sum(2**(ncols - 1 - i) for i in range(ncols) if tot[i] > 0)
    epsilon = sum(2**(ncols - 1 - i) for i in range(ncols) if tot[i] < 0)
    return gamma*epsilon

def main2(filename):
    x = None
    for i,l in enumerate(open(filename)):
        if x is None:
            n = len(l.strip())
            x = np.zeros((1000, n), dtype=int)
        for j, b in enumerate(l.strip()):
            if b == '1':
                x[i,j] = 1
            else:
                x[i,j] = -1
    
    mask = [True]*x.shape[0]
    for j in range(n):
        if sum(x[mask,j]) >= 0:
            mask = (x[:,j] > 0) & mask
        else:
            mask = (x[:,j] < 0) & mask
        if sum(mask) == 1:
            oxy = x[mask].flatten()
            break
    oxy = int("".join("1" if b > 0 else "0" for b in oxy), base=2) 

    mask = [True]*x.shape[0]
    for j in range(n):
        if sum(x[mask,j]) >= 0:
            mask = (x[:,j] < 0) & mask
        else:
            mask = (x[:,j] > 0) & mask
        if sum(mask) == 1:
            co2 = x[mask].flatten()
            break
    co2 = int("".join("1" if b > 0 else "0" for b in co2), base=2) 
    return co2*oxy

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main2(filename)
    print(f"{ret=}") 
