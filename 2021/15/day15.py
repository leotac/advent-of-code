# plotting
from colorama import Style,Fore
import os, time

VERBOSE = False
def plot(risk, v, visible, highlighted):
    os.system('clear')
    I = max(u[0] for u in visible)
    J = max(u[1] for u in visible)
    for i in range(I+1):
        print("".join([fmt((i,j), risk, v, visible, highlighted) for j in range(J+1)]))

def fmt(pos, risk, v, visible, highlighted):
    if pos == v:
        return Style.BRIGHT+Fore.BLUE + str(risk(*pos)) + Style.RESET_ALL
    elif pos in set(visible) & set(highlighted):
        return Style.BRIGHT+Fore.RED + str(risk(*pos)) + Style.RESET_ALL
    elif pos in visible:
        return str(risk(*pos))
    else:
        return " "

def backwards(v, parent):
    path = [v]
    while (v := parent[v]) is not None:
        path.append(v)
    return path

# solution
from heapq import heappush as push, heappop as pop

def adj(i,j, bounds):
    for (x,y) in (i-1,j), (i+1,j), (i,j-1), (i,j+1):
        if 0 <= x < bounds[0] and 0 <= y < bounds[1]:
            yield (x,y)

def main(filename, M=1):
    tile = [[int(x) for x in l.strip()] for l in open(filename)]
    I, J = len(tile), len(tile[0])

    def risk(i,j):
        return (tile[i % I][j % J] + (i // I) + (j // J) - 1) % 9 + 1
    
    # Simplified Dijkstra (all incoming arcs in a node have the same cost)
    start, end = (0,0), (M*I - 1, M*J - 1)
    visited = {start: None}
    frontier = [(0, start)]
    while len(frontier) > 0:
        score, u = pop(frontier)
        if VERBOSE: time.sleep(0.01); plot(risk, u, visited, {i[1] for i in frontier})
        for v in adj(*u, (M*I, M*J)):
            if v not in visited:
                push(frontier, (c := score + risk(*v), v))
                visited[v] = u
                if v == end:
                    if VERBOSE: plot(risk, v, visited, set(backwards(v,visited)))
                    return c

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename, M=1)
    print(f"{ret}") 
    ret = main(filename, M=5)
    print(f"{ret}") 
