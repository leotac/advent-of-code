def adj(i,j):
    for ii in (i-1,i,i+1):
        for jj in (j-1,j,j+1):
            yield (ii,jj)

def compute_ranges(pixels, margin=0):
    range_i = range(min(i for (i,_) in pixels) - margin, max(i for (i,_) in pixels) + 1 + margin)
    range_j = range(min(j for (_,j) in pixels) - margin, max(j for (_,j) in pixels) + 1 + margin)
    return range_i, range_j

def light(i,j,pixels,range_i,range_j,background):
    if (i,j) in pixels:
        return "1"
    elif i in range_i and j in range_j:
        return "0"
    else:
        return background

def enhance(pixels, algorithm,background):
    extended_i, extended_j = compute_ranges(pixels, margin=1)
    range_i, range_j = compute_ranges(pixels, margin=0)
    newpixels = set()
    for i in extended_i:
        for j in extended_j:
            index = int("".join([light(k,l,pixels,range_i,range_j,background) for (k,l) in adj(i,j)]), 2)
            if algorithm[index] == "#":
                newpixels |= {(i,j)}
    return newpixels

def draw(pixels):
    from drawille import Canvas
    c = Canvas()
    range_i, range_j = compute_ranges(pixels)
    for i in range_i:
        for j in range_j:
            if (i,j) in pixels:
                c.set(i,j)
    print(c.frame())

def main(filename, n=2):
    lines = open(filename).readlines()
    algorithm = lines[0]
    pixels = set((i,j) for i,l in enumerate(lines[2:]) for j,c in enumerate(l) if c=="#")
    draw(pixels)
    for i in range(50):
        pixels = enhance(pixels, algorithm, background="0" if i%2==0 else "1")
        draw(pixels)
    return len(pixels)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
