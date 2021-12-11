import numpy as np
from tqdm import trange

# Plotting

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

hist = []
hist2 = []
DIR = "img2"
PLOT = False

def plot(A, t):
    hist.append(A.clip(0,10).mean())
    try:
        hist2.append(hist[-1] - hist[-2])
    except:
        hist2.append(hist[-1])
    _heatmap(A,t)
    _phasespace(A,t)
    
def _heatmap(A, t):
    fig, axes = plt.subplots(1,2,figsize=(8,4))
    axes[0].imshow(A, vmin=0, vmax=10)
    axes[0].axis('off')
    lo = max(0,t-50)
    axes[1].plot(range(lo,t+1), hist[lo:])
    axes[1].set_xlim(lo, t+10)
    axes[1].plot(t, hist[-1], "ro")
    axes[1].set_ylim(0, 10)
    axes[1].text(lo,0.1,f"{t}",color="black")
    axes[1].axis('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.margins(x=0)
    plt.savefig(f"{DIR}/{t:03d}.png", bbox_inches='tight', pad_inches=0) 
    plt.close()
    plt.cla()

def _phasespace(A, t):
    fig, ax = plt.subplots(1,1,figsize=(8,4))
    x, y = hist, hist2 
    if len(x) > 2:
        z = np.linspace(0.0, 1.0, len(x) - 1)
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, array=z, cmap="gray",
                              linewidth=2)
        ax.add_collection(lc)
    else:
        ax.plot(x, y, color="white")
    
    fig.patch.set_facecolor('black')
    ax.set_xlim(0.5, 10.5)
    ax.plot(hist[-1], hist2[-1], "ro")
    ax.set_ylim(-11, 7)
    ax.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.margins(x=0)
    plt.savefig(f"{DIR}/state_{t:03d}.png", bbox_inches='tight', pad_inches=0) 
    plt.close()
    plt.cla()

# Solution

def main(filename):
    A = np.array([[int(x) for x in l.strip()] for l in open(filename)])
    part_one = sum(tick(A,t) for t in trange(100))
    for t in trange(100, 10000):
        if tick(A,t) == np.product(A.shape):
            print(f"First synch @ step {t+1}")
            part_two = t+1
            break
    return part_one, part_two

def adj(i,j,A):
    for x in (-1,0,+1):
        for y in (-1,0,1):
            k,l = i+x, j+y
            if (x or y) and 0 <= k < A.shape[0] and 0 <= l < A.shape[1]:
                yield k,l

def tick(A, t):
    flashed = np.zeros(A.shape, dtype=bool)
    A += 1
    while not (flashed | (A <= 9)).all():
        flashing = ~flashed & (A > 9)
        flashed |= flashing
        for (i,j) in zip(*np.where(flashing)):
            for (k,l) in adj(i,j, A):
                if ~flashed[k,l]:
                    A[k,l] += 1
    if PLOT: plot(A,t)
    assert ((A>9) == flashed).all()
    A[flashed] = 0
    return flashed.sum()

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
