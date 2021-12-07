from collections import Counter
import math

def main(filename, cost):
    c = Counter(int(x) for x in open(filename).read().strip().split(","))
    hi = max(c.keys())
    best = (math.inf, -1)
    for i in range(hi+1):
        v = sum(count*cost(i,k) for k,count in c.items())
        if v < best[0]:
            best = (v, i)
        # by convexity (both cases, sum of convex func)
        # as soon as the function starts increasing, we can exit the loop.
        # (for the same reason one could easily do a faster binary line search)
        else: 
            break
    return best

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename, cost=lambda i,j : abs(i-j))
    print(f"{ret=}") 

    def gauss(i,j):
        n = abs(i-j)
        return int(n*(n+1)/2)

    ret = main(filename, cost=gauss)
    print(f"{ret=}") 
