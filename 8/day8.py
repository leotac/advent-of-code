from itertools import permutations
from tqdm import tqdm

DIGITS = [
        set("abcefg"),
        set("cf"),
        set("acdeg"),
        set("acdfg"),
        set("bcdf"),
        set("abdfg"),
        set("abdefg"),
        set("acf"),
        set("abcdefg"),
        set("abcdfg"),
]
S = "abcdefg"

def is_feasible(z, sol):
    for d in z:
        if set(sol[x] for x in d) not in DIGITS:
            return False
    return True

def bruteforce(z):
    for p in permutations(S):
        sol = dict(zip(p,S))
        if is_feasible(z, sol):
            return sol

def to_digit(s):
    return str(DIGITS.index(set(s)))

def decode(x,y):
    sol = bruteforce(x + y)
    return [to_digit(sol[x] for x in d) for d in y]

def main(filename):
    total = 0
    for i,l in enumerate(tqdm(open(filename), total=200)):
        s = l.strip().split()
        decoded = decode(s[:10], s[-4:])
        total += int("".join(decoded))
    return total

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
