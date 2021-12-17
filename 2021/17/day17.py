import numpy as np

def within(p, target):
    return all(target[:,0] <= p) and all(p <= target[:,1])

def infeasible(p,v,target):
    return (v[1] <= 0 and p[1] < target[1,0]) or \
            (v[0] <= 0 and p[0] < target[0,0]) or \
            (v[0] >= 0 and p[0] > target[0,1])

def simulate(v_init, target, maxit=1000):
    p, v = np.array([0,0]), np.array(v_init)
    highest = 0
    for i in range(1,maxit):
        p += v
        v -= [np.sign(v[0]), 1]
        if p[1] > highest:
            highest = p[1]
        if within(p,target):
            return True, highest
        if infeasible(p,v,target):
            return False, None 
    print(f"WARNING: Not completed from {v_init=} within {maxit=} iterations!")
    return False, None

def main(target):
    res = []
    for xv in range(1,300):
        for yv in range(-150,300):
            found, highest = simulate([xv,yv], target)
            if found:
                res.append((highest, xv, yv))
    
    res = np.array(res)
    num_solutions = len(res)
    max_height = res.max(axis=0)[0]
    print(res.max(axis=0), res.min(axis=0))
    return num_solutions, max_height

if __name__ == "__main__":
    target = np.array([[150,193],[-136.,-86]])
    ret = main(target)
    print(f"{ret=}") 
