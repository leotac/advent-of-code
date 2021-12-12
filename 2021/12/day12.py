from collections import deque

PATHS = set()
def big(x):
    return x.isupper()

def explore(cur, G, visited, again=False, path=""):
    
    if again and (big(cur) or visited[cur] == 0):
        return 0 #no need to use exception

    if visited[cur] == 2 or (visited[cur] == 1 and not again) or (visited[cur] == 1 and cur == "start"):
        return 0
    if cur == "end":
 #       print(visited, path)
        PATHS.add(path)
        return 1
 
    visited = visited.copy()
    if not big(cur):
        visited[cur] += 1
    
    if max(visited.values()) < 2:
        return sum(explore(n, G, visited, path=f"{path}-{n}") for n in G[cur]) \
                + sum(explore(n, G, visited, again=True, path=f"{path}-{n}") for n in G[cur])
    else:
        return sum(explore(n, G, visited, path=f"{path}-{n}") for n in G[cur])


def main(filename):
    G = {}
    for l in open(filename):
        i,j = l.strip().split("-")
        G.setdefault(i, []).append(j)
        G.setdefault(j, []).append(i)
    visited = {n:0 for n in G}
    return explore("start", G, visited, path="start")

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
#    filename = "data2"
    ret = main(filename)
    print(len(PATHS))
    print(f"{ret=}") 
