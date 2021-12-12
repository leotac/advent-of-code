VERBOSE = False
G = dict()

def big(x):
    return x.isupper()

def explore(cur, visited, again=False, path=""):
    
    if again and (big(cur) or visited[cur] == 0):
        return 0 #no need to use exception

    if visited[cur] == 2 or (visited[cur] == 1 and not again) or (visited[cur] == 1 and cur == "start"):
        return 0

    if cur == "end":
        if VERBOSE: print(visited, path)
        return 1
 
    visited = visited.copy()
    if not big(cur):
        visited[cur] += 1
    
    if max(visited.values()) < 2:
        return sum(explore(n, visited, path=f"{path}-{n}") for n in G[cur]) \
                + sum(explore(n, visited, again=True, path=f"{path}-{n}") for n in G[cur])
    else: # already used exception
        return sum(explore(n, visited, path=f"{path}-{n}") for n in G[cur])


def main(filename):
    for l in open(filename):
        i,j = l.strip().split("-")
        G.setdefault(i, []).append(j)
        G.setdefault(j, []).append(i)
    visited = {n:0 for n in G}
    return explore("start", visited, path="start")

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
#    filename = "data2"
    ret = main(filename)
    print(f"{ret=}") 
