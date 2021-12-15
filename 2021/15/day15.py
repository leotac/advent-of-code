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
    
    # Simplified Dijkstra, given that all incoming arcs in a node cost the same
    start = (0,0)
    end = (M*I - 1, M*J - 1)
    visited = {start}
    heap = []
    push(heap, (0, start))
    while len(heap) > 0:
        score, u = pop(heap)
        for v in adj(*u, (M*I, M*J)):
            if v not in visited:
                if v == end:
                    return score + risk(*v)
                push(heap, (score + risk(*v), v))
                visited |= {v}

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename, M=1)
    print(f"{ret}") 
    ret = main(filename, M=5)
    print(f"{ret}") 
