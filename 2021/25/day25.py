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

def draw(x, i):
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots(1, figsize=(4,4))
    a = x.copy()
    a[a=="."] = 0
    a[a==">"] = 1
    a[a=="v"] = 2
    ax.imshow(a.astype(int), vmin=0, vmax=2)
    ax.axis('off')
    plt.margins(x=0)
    plt.savefig(f"img/{i:03d}.png", bbox_inches='tight', pad_inches=0) 
    plt.close()
    plt.cla()

def main(filename):
    cucumbers = np.array([list(l.strip()) for l in open(filename)])
    for i in trange(1000):
        draw(cucumbers, i)
        new = step(cucumbers)
        if (new == cucumbers).all(): break
        cucumbers = new
    return i+1

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
