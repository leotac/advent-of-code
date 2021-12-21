from itertools import cycle
from functools import lru_cache 

def move(p, v):
    return (p + v - 1) % 10 + 1

def deterministic(p0, p1, sides):
    positions = [p0, p1]
    scores = [0, 0]
    die = enumerate(cycle(range(1, sides+1)), start=1)
    while True:
        for p in (0,1):
            for i in range(3):
                num_rolls, value = next(die)
                positions[p] = move(positions[p], value)
            scores[p] += positions[p]
            if scores[p] >= 1000:
                return min(scores)*num_rolls

@lru_cache(maxsize=21*21*10*10*6)
def quantum(score1, score2, pos1, pos2, num_roll):
    if score1 >= 21:
        return 1
    
    if score2 >= 21:
        return 0

    wins = 0
    if num_roll < 3:# player 1's turn
        for d in (1,2,3):
            new_pos = move(pos1, d)
            new_score = score1 + (num_roll==2 and new_pos)
            wins += quantum(new_score, score2, new_pos, pos2, (num_roll + 1) % 6)
    elif num_roll >= 3:# player 2's turn
        for d in (1,2,3):
            new_pos = move(pos2, d)
            new_score = score2 + (num_roll==5 and new_pos)
            wins += quantum(score1, new_score, pos1, new_pos, (num_roll + 1) % 6) 
    return wins

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = deterministic(10, 7, 100)
    print(f"{ret}") 
    ret = quantum(0, 0, 10, 7, 0)
    print(f"{ret}") 
