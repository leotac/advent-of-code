from heapq import heappush as push, heappop as pop
def adj(i,j, bounds):
    for (x,y) in (i-1,j), (i+1,j), (i,j-1), (i,j+1):
        if 0 <= x < bounds[0] and 0 <= y < bounds[1]:
            yield (x,y)
def main(filename):
    risk = [[int(x) for x in l.strip()] for l in open(filename)]
    shape = len(risk), len(risk[0])

    # Simplified Dijikstra, thanks to the fact that all incoming edges weight the same..
    start = (0,0)
    end = (shape[0] - 1, shape[1] - 1)
    visited = {start: (None,0)}
    heap = []
    push(heap, (0, start))
    while len(heap) > 0:
        score, u = pop(heap)
        for v in adj(*u, shape):
            if v not in visited:
                push(heap, (score + risk[v[0]][v[1]], v))
                visited[v] = (u, (score + risk[v[0]][v[1]]))
                if v == end:
                    return visited[v][1]


if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    #filename = "test"
    ret = main(filename)
    print(f"{ret=}") 
