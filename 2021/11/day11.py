import numpy as np

def main(filename):
    A = np.array([[int(x) for x in l.strip()] for l in open(filename)])
    part_one = sum(tick(A,t) for t in range(100))
    for t in range(100, 10000):
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
    assert ((A>9) == flashed).all()
    A[flashed] = 0
    return flashed.sum()

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
