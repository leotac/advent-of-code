def main1(filename):
    fish = [int(x) for x in open(filename).read().strip().split(",")]
    for i in range(80):
        new = 0
        for i in range(len(fish)):
            fish[i] -= 1
            if fish[i] < 0:
                fish[i] = 6
                new += 1
        fish += [8]*new
    return len(fish)

def main2(filename, gen):
    import numpy as np
    fish = [int(x) for x in open(filename).read().strip().split(",")]
    pop = np.zeros(9, dtype=int)
    for f in fish:
        pop[f] += 1
    for i in range(gen):
        pop = np.roll(pop, -1)
        pop[6] += pop[8]
    return pop.sum()

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main2(filename, gen=256)
    print(f"{ret=}") 
