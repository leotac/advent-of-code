from tqdm import tqdm
import numpy as np

class Op:
    def __init__(self, line):
        self.op, *self.args = line.split()
        
    def __call__(self, state):
        """ Apply Op to given input state [and simplify, if possible!]
        """
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
                ret = f"np.int32({first} == {second})"
        try:
            state[self.args[0]] = eval(ret)
        except:
            state[self.args[0]] = ret

def parse_blocks(filename):
    program = [Op(l.strip()) for l in open(filename)]
    
    definitions = []
    functions = []
    state = None
    for o in program:
        if o.op == "inp":
            if state: definitions.append(state["z"])
            state = dict(w="a", x=0, y=0, z="b")
        else:
            o(state)
    definitions.append(state["z"])
    print("Parsed functions:")
    for i,d in enumerate(definitions):
        exec(f"functions.append(lambda a,b: {d})")
        print(f"> {d}")
    return functions

def cartesian_product(x, y):
    return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

def compute_domains(fs):
    """ Given N sequential functions, compute the z domain for i+1-th function as the image of i-th function. 
        We start with [0] given that the initial value of z is given, z=0.
        The last one is not needed.
    """
    domain = [[0]]
    for i,f in enumerate(tqdm(fs[:-1])):
        X = cartesian_product(list(range(1,10)), list(domain[i]))
        domain.append(list(set((f(X[:,0],X[:,1])))))
    return domain

def backward(filename, criterion=min, domain=None):
    """
    Backward search
    Starting rom the last step, what are the valid inputs (pre-image) for which we can obtain the desired output(s)?
    Then, use those inputs as the desired output of the previous step.
    """
    fs = parse_blocks(filename)
   
    if domain is None:
        print("Computing z domains..")
        domain = compute_domains(fs)

    good_z = {0}
    good_states = [] 
    for i in tqdm(reversed(range(14)), total=14):
        candidate_initial_states = cartesian_product(list(range(1,10)), list(domain[i]))
        print(f"Candidate input states for step {i}:", len(candidate_initial_states))
        S = np.array(candidate_initial_states)
        Z = fs[i](S[:,0],S[:,1])
        
        # What are the input states that lead to a desired output? (good_z)
        good_idx = np.in1d(Z, list(good_z))
        good_states.append(S[good_idx])
        print("Input states that lead to good end states:", len(good_states[-1]))
        good_w = set([w[0] for w in good_states[-1]])
        good_z = set([w[1] for w in good_states[-1]])
        print(f"w ({len(good_w)}):", sorted(good_w)[:10])
        print(f"z ({len(good_z)}):", sorted(good_z)[:10])
        print("#"*20)

    good_states = reversed(good_states)
    z = 0
    W = []
    for f,S in zip(fs, good_states):
        w = criterion(w for (w,zi) in S if zi == z)
        W.append(str(w))
        print(f"Computed: {f(w,z)=} from {w=} and {z=}")
        z = f(w,z)
    assert z == 0
    return "".join(W)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = backward(filename, criterion=max)
    print(f"{ret=}") 
    ret = backward(filename, criterion=min)
    print(f"{ret=}") 
