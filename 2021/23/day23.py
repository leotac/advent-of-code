from copy import deepcopy
from collections import defaultdict
from tqdm import trange
from itertools import permutations
from heapdict import heapdict

DEPTH = 4
BURROW = [list(l) for l in ['...........'] + ['##.#.#.#.##']*DEPTH]
ROOMS = set([(i,room) for i in range(1,DEPTH+1) for room in (2,4,6,8)])
HALLWAY = set([(0,t) for t in range(11)])
VALIDHALLWAY = HALLWAY - {(0,2),(0,4),(0,6),(0,8)} 
PODS = {"A","B","C","D"}
PODROOM = {"A":2, "B":4, "C":6, "D":8}
PODCOST = {"A": 1,"B":10,"C":100,"D":1000}

def compute_path(u,v):
    if u == v:
        return None
    if u[0] == v[0] == 0: #both hallways not a valid move
        return None

    if u[0] == 0: #from hallway to room
        sign = int(v[1] > u[1]) or -1
        path = [(0,t) for t in range(u[1], v[1] + sign, sign)]
        path += [(t,v[1]) for t in range(1, v[0]+1)]
        return path

    if v[0] == 0: #from room to hallway
        path = [(t,u[1]) for t in range(u[0], 0, -1)]
        sign = int(v[1] > u[1]) or -1
        path += [(0,t) for t in range(u[1], v[1] + sign, sign)]
        return path       

    if u[0] > 0 and v[0] > 0 and u[1] != v[1]: #from room to other room
        path = [(t,u[1]) for t in range(u[0], 0, -1)]
        sign = int(v[1] > u[1]) or -1
        path += [(0,t) for t in range(u[1], v[1] + sign, sign)]
        path += [(t,v[1]) for t in range(1, v[0]+1)]
        return path

    return None #doesn't make sense to move within the same room

PATHS = {u: {v: path for v in (ROOMS|VALIDHALLWAY) if (path := compute_path(u,v))} for u in (ROOMS|VALIDHALLWAY)}

def getcost(u,v,pod):
    if u == v:
        return 0
    if u[1] == v[1]:
        return PODCOST[pod]*abs(u[1]-v[1])
    return PODCOST[pod]*(len(PATHS[u][v]) - 1) 

class State:

    def __init__(self, positions, cost, parent):
        assert len(positions) == DEPTH*4
        self.positions = positions
        self.cost = cost
        self.parent = parent
        # estimate cost to finish
        self.estimated = cost
        pods = defaultdict(list)
        for u, pod in positions.items(): 
            pods[pod].append(u)
        for c, items in pods.items():
            room = PODROOM[c]
            # try all possible combinations to estimate cost..
            self.estimated += min([sum(getcost(items[i],(p[i],room),c) for i in range(DEPTH)) for p in permutations(range(1,DEPTH+1))])

    def isvalid(self, path):
        for u in path[1:]: #check path is empty
            if u in self.positions:
                return False
        end = path[-1]
        pod = self.positions[path[0]]
        if end in ROOMS:
            if end[1] != PODROOM[pod]:
                return False
            if end[0] < DEPTH: #then all those below must be pods of the same race
                if not all((self.positions.get((i,end[1]), None) == pod) for i in range(end[0]+1,DEPTH+1)):
                    return False
        return True

    def iswin(self):
        if set(self.positions) != ROOMS:
            return False

        for u, pod in self.positions.items():
            if u[1] != PODROOM[pod]:
                return False
        return True

    def __repr__(self):
        b = deepcopy(BURROW)
        for p,c in self.positions.items():
            b[p[0]][p[1]] = c
        return "\n".join("".join(l) for l in b)

def search(amphipods, maxit=100000):
    
    init = State(amphipods, 0, None)
    stack = heapdict()
    stack[init] = init.estimated
    visited = dict()
    best = (50000, None) #initialized with good upper bound 
    for it in trange(maxit):
        s, _ = stack.popitem()
        if it % 10000 == 0: print(len(stack), best[0], s.cost, s.estimated, len(visited))
        if s.estimated > best[0]:
            print(f"Best: {best[0]}, most promising: {s.estimated}")
            return best
        for u,pod in s.positions.items():
            for end, path in PATHS[u].items():
                if s.isvalid(path):
                    newpositions = s.positions.copy()
                    del newpositions[u]
                    newpositions[end] = pod
                    newcost = s.cost + (len(path) - 1)*PODCOST[pod]
                    newstate = State(newpositions, cost=newcost, parent=s)
                    if newstate.iswin() and newstate.cost < best[0]:
                        print(f"Found solution with cost {newstate.cost} after {it} iterations")
                        best = (newstate.cost, newstate)
                    if newstate.estimated < best[0] and newstate.cost < visited.get(str(newstate), 9999999): 
                        # estimate must be better than current best and state must be new or reached in fewer steps
                        stack[newstate] = newstate.estimated
                        visited[str(newstate)] = newstate.cost

def parse(filename):
    s = {}
    c = [list(l.strip()) for l in open(filename)]
    for i in range(len(c)):
        for j in range(11):
            if c[i][j] in "ABCD":
                s[i,j] = c[i][j]
    return s

def main(filename):
    amphipods = parse(filename)
    return search(amphipods)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp2")
    ret = main(filename)
    print(f"{ret=}") 
