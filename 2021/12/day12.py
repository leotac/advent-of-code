VERBOSE = False
G = dict()

def big(x):
    return x.isupper()

def explore(cur, visited, exceptions, path):
    if cur == "end":
        if VERBOSE: print(visited, path)
        return 1
 
    paths = sum(explore(n, visited | {n}, exceptions, path+[n]) for n in G[cur] 
            if (big(n) or (n not in path)) and n != "start" )
    if exceptions > 0:
        paths += sum( explore(n, visited, exceptions-1, path+[n]) for n in G[cur]
                if not big(n) and (n in visited) and n != "start")
    return paths

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    for l in open(filename):
        i,j = l.strip().split("-")
        G.setdefault(i, []).append(j)
        G.setdefault(j, []).append(i)

    ret1 = explore("start", set(), exceptions=0, path=["start"])
    ret2 = explore("start", set(), exceptions=1, path=["start"])
    print(ret1, ret2) 
