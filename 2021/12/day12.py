VERBOSE = False
G = dict()

def big(x):
    return x.isupper()

def explore(cur, visited, exceptions, path=""):
    if cur == "end":
        if VERBOSE: print(visited, path)
        return 1
 
    if exceptions > 0:
        return sum(
                explore(n, visited | {n}, exceptions, path=f"{path}-{n}") 
                for n in G[cur] 
                if (big(n) or (n not in visited)) and n != "start" ) \
                + sum(
                    explore(n, visited | {n}, exceptions-1, path=f"{path}-{n}")
                    for n in G[cur]
                    if not big(n) and (n in visited) and n != "start")
    else: # no exceptions remaining
        return sum(explore(n, visited | {n}, exceptions, path=f"{path}-{n}") 
                for n in G[cur] 
                if (big(n) or (n not in visited)) and n != "start" )

def main(filename, exceptions):
    visited = set()
    return explore("start", visited, exceptions, path="start")

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    for l in open(filename):
        i,j = l.strip().split("-")
        G.setdefault(i, []).append(j)
        G.setdefault(j, []).append(i)

    ret1 = main(filename, 0)
    ret2 = main(filename, 1)
    print(ret1, ret2) 
