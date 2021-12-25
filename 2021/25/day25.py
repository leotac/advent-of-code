import numpy as np
from tqdm import trange

def right(x):
    newx = x.copy()
    I,J = np.where(x == ">")
    for i,j in zip(I,J):
        r = (j+1) % x.shape[1]
        if x[i,r] == ".":
            newx[i,r] = ">"
            newx[i,j] = "."
    return newx

def down(x):
    newx = x.copy()
    I,J = np.where(x == "v")
    for i,j in zip(I,J):
        d = (i+1) % x.shape[0]
        if x[d,j] == ".":
            newx[d,j] = "v"
            newx[i,j] = "."
    return newx

def step(x):
    x = right(x)
    x = down(x)
    return x

def main(filename):
    cucumbers = np.array([list(l.strip()) for l in open(filename)])
    for i in trange(4000):
        new = step(cucumbers)
        if (new == cucumbers).all(): break
        cucumbers = new
    return i+1

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
