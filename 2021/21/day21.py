from itertools import cycle
from functools import lru_cache 
import numpy as np

def move(p, v):
    return (p + v - 1) % 10 + 1

def die(sides=100, deterministic=True):
    if deterministic:
        for i,n in enumerate(cycle(range(1, sides+1))):
            yield n, i+1

def deterministic(p0, p1, die_sides):
    positions = [p0, p1]
    scores = [0, 0]
    roll = die(sides=die_sides, deterministic=True)
    while True:
        for p in (0,1):
            for i in range(3):
                v, num_rolls = next(roll)
                positions[p] = move(positions[p], v)
            scores[p] += positions[p]
            if scores[p] >= 1000:
                return min(scores)*num_rolls

@lru_cache(maxsize=21*21*10*10*6)
def quantum(score1, score2, pos1, pos2, num_roll):
    if score1 >= 21:
        return np.array([1, 0])
    
    if score2 >= 21:
        return np.array([0, 1])

    if num_roll < 3:# player 1's turn
        wins = np.array([0,0])
        for d in (1,2,3):
            p, s = move(pos1, d), score1
            if num_roll == 2:
                s += p
            wins += quantum(s, score2, p, pos2, (num_roll + 1) % 6)
        return wins
    elif num_roll >= 3:# player 2's turn
        wins = np.array([0,0])
        for d in (1,2,3):
            p, s = move(pos2, d), score2
            if num_roll == 5:
                s += p
            wins += quantum(score1, s, pos1, p, (num_roll + 1) % 6) 
        return wins

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = deterministic(10, 7, 100)
    print(f"{ret}") 
    ret = quantum(0, 0, 10, 7, 0)[0]
    print(f"{ret}") 

