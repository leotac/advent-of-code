import numpy as np
from collections import Counter

def main(filename, gen):
    c = Counter([int(x) for x in open(filename).read().strip().split(",")])
    fish = np.array([c[i] for i in range(9)])

    for i in range(gen):
        pop = np.roll(pop, -1)
        pop[6] += pop[8]
    return pop.sum()

# alternative: use transition matrix
A = np.block([
    [np.eye(1,8,6).T, np.eye(8)], 
    [1, np.zeros((1,8))]
    ]).astype(int)

def main2(filename, gen):
    c = Counter([int(x) for x in open(filename).read().strip().split(",")])
    fish = np.array([c[i] for i in range(9)])
    return np.sum(np.linalg.matrix_power(A,gen) @ fish)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret1 = main(filename, gen=80)
    ret2 = main(filename, gen=256)
    print(ret1, ret2) 
    
    ret1 = main2(filename, gen=80)
    ret2 = main2(filename, gen=256)
    print(ret1, ret2) 
