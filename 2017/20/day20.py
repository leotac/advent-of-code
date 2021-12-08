p,v,a = [],[],[]
d = []

def dist(p1, p2=None):
    if p2 is not None:
        return sum(abs(p1[i] - p2[i]) for i in range(len(p1)))
    return sum(abs(x) for x in p1)

with open("day20.txt") as f:
    for l in f:
        pos,vel,acc = [map(int,x[3:-1].split(",")) for x in l.strip().split(", ")]
        p.append(pos)
        v.append(vel)
        a.append(acc)
        d.append(dist(pos))

N = len(p)

def tick():
    for coord in range(3):
        for i in range(N):
            if not destroyed[i]:
                v[i][coord] = v[i][coord] + a[i][coord]
                p[i][coord] = p[i][coord] + v[i][coord]
    
    for i in range(N):
        if not destroyed[i]:
            d[i] = dist(p[i])

min_a = min([dist(y) for y in a])
print([(i,p[i],d[i],v[i],a[i]) for i in range(N) if dist(a[i]) == min_a]) 

destroyed = [False]*N

def collisions():
    to_destroy = [False]*N
    for i in range(N):
        if not destroyed[i]:
            for j in range(N):
                if not destroyed[j]:
                    if dist(p[i],p[j]) == 0:
                        to_destroy[i] = True
                        to_destroy[j] = True
    return to_destroy

T = 100
for t in range(T):
    tick()
    for i in collisions():
        destroyed[i] = True
    print sum(1 for x in destroyed if not x)
