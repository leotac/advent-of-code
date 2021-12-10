import numpy as np

def plot(a):
    from matplotlib import pyplot as plt
    plt.imshow(a)
    plt.axis('off')
    plt.savefig("day5.png", bbox_inches='tight', pad_inches=0)

def main(filename):
    a = np.zeros((1000, 1000), dtype=int)
    for l in open(filename):
        p1, _, p2 = l.strip().split()
        x1, y1 = tuple(map(int, p1.split(",")))
        x2, y2 = tuple(map(int, p2.split(",")))
        if x1 == x2:
            a[x1, min(y1,y2):max(y1,y2)+1] += 1
        elif y1 == y2:
            a[min(x1,x2):max(x1,x2)+1, y1] += 1
        else:
            x_step = 1 if x1 <= x2 else -1
            y_step = 1 if y1 <= y2 else -1
            a[range(x1, x2 + x_step, x_step), range(y1, y2 + y_step, y_step)] += 1

    plot(a)    
    return np.sum(a > 1)


if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
