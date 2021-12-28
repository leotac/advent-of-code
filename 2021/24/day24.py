from tqdm import trange, tqdm
from itertools import product
import numpy as np
from concurrent.futures import ProcessPoolExecutor

class OpTree:
    def __init__(self, line):
        self.op, *self.args = line.split()
        
    def __call__(self, state):
        # Ops are always x = x <OP> y
        try: #try to simplify x
            first = eval(state[self.args[0]])
        except:
            first = state[self.args[0]]

        try: #check if second argument is a constant
            second = int(self.args[1])
        except:
            second = state[self.args[1]]

        if self.op == "add":
            if first == 0 and second == 0:
                ret = 0
            elif first == 0:
                ret = f"{second}"
            elif second == 0:
                ret = f"{first}"
            else:
                ret = f"({first} + {second})"
        elif self.op == "mul":
            ret = f"({first} * {second})"
            if first == 0 or second == 0:
                ret = 0
            if second == 1:
                ret = f"{first}"
        elif self.op == "div":
            if second == 0: raise ValueError
            ret = f"({first} // {second})"
            if second == 1:
                ret = f"{first}"
        elif self.op == "mod":
            if second == 0: raise ValueError
            if second == 1:
                ret = 0
            else:
                ret = f"({first} % {second})"
        elif self.op == "eql":
            if isinstance(first, int) and first > 9 and second in "abcdefghijklmnop":
                ret = 0
            if isinstance(first,str) and "% 26) + 1" in first and second == "a":
                ret = 0
            elif isinstance(first, int) and isinstance(second, int):
                ret = int(first == second)
            else:
                #ret = f"np.int32({first} == {second})"
                ret = f"int({first} == {second})"
        try:
            state[self.args[0]] = eval(ret)
        except:
            state[self.args[0]] = ret

def parse_blocks(filename):

    program = [OpTree(l.strip()) for l in open(filename)]
    
    definitions = []
    state = None
    for o in program:
        if o.op == "inp":
            if state: definitions.append(state["z"])
            state = dict(w="a", x=0, y=0, z="b")
        else:
            o(state)
    definitions.append(state["z"])
    blocks = []
    for d in definitions:
        exec(f"blocks.append(lambda a,b: {d})")
    return definitions, blocks

def backward_fast(filename, domain=None):
    defs, fs = parse_blocks(filename)
   
    if domain is None:
        domain = [[0]]
        for i,(f,d) in tqdm(enumerate(zip(fs,defs)), total=14):
            print(f"{i}: with def: {d}")
            #X = np.array([(w,z) for w in range(1,10) for z in domain[i]])
            domain.append(set([f(w,z) for w in range(1,10) for z in tqdm(domain[i])]))
            #domain.append(set(f(X[:,0],X[:,1])))
            print(f"Obtained: {len(domain[-1])} distinct output values")
        
    assert 0 in domain[14] #domain[14] is the image of block 13

    good_z = [{0}]
    good_states = [set((i,0) for i in range(1,10))]
    for i in tqdm(reversed(range(14)), total=14):
        print(f"From input {i} to the next one, using domain {i} ({len(domain[i])})")
        d = domain[i]
        if i == 13:
            d = range(25)
        candidate_initial_states = list(product(range(1,10), d))
        print(len(candidate_initial_states))
        good_initial_states = []
        for s in tqdm(candidate_initial_states): 
            z = fs[i](s[0],s[1]) #w,z
            if z in good_z[i]:
                good_initial_states.append(s)
        good_states.append(set(good_initial_states))
        print("Initial states that lead to good end states:", len(good_initial_states))
        good_w = set([w[0] for w in good_initial_states])
        good_z = set([w[1] for w in good_initial_states])
        print(f"w ({len(good_w)}):", sorted(good_w)[:5] + sorted(good_w)[-5:])
        print(f"z ({len(good_z)}):", sorted(good_z)[:5] + sorted(good_z)[-5:])
        print("#"*20)

    good_states = reversed(good_states)
    z = 0
    ws = []
    for i,f,S in enumerate(zip(fs, reversed(good_states))):
        w = min(w for (w,zi) in S if zi == z)
        ws.append(w)
        print(f"Computed: {f(w,z)=} from {w=} and {z=}")
        z = f(w,z)
    return


if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = backward_fast(filename)
    print(f"{ret=}") 
