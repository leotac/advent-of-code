import numpy as np
from itertools import permutations, product
def parse(filename):
    scanners = []
    for l in open(filename):
        if "---" in l:
            scanners.append([])
        elif l.strip() == "":
            continue
        else:
            scanners[-1].append([int(x) for x in l.strip().split(",")])
    return [np.array(s) for s in scanners]


def do(scanners):

    scan_0 = {0: scanners[0]} # readings in canonical coordinates (i.e., scanner 0)
    scan_positions = {0: np.array([0,0,0])}
    transformed = [0]
    scan_orig = set(range(1,len(scanners))) # in original coordinates (scanner 1, ...n)
    while len(scan_0) < len(scanners):
        s0 = transformed.pop()
        for i,s in enumerate(scanners):
            if i not in scan_0: #not yet transformed 
                ret, scanner_position = find_match(scan_0[s0], s) #try to find correspondence between s0 and s
                if ret is not None: #managed to bring to canonical coordinates..
                    scan_0[i] = ret
                    scan_positions[i] = scanner_position
                    transformed.append(i)
                    print(f"Found corr between {s0} and {i}")
                    print(transformed, scan_0.keys())

    #when everything translated to canonical coordinates..

    stacked = np.vstack(list(scan_0.values()))
    beacons = np.array(sorted(set(tuple(r) for r in stacked)))

    return beacons, scan_positions 

def manhattan(scanners):
    return max([np.abs(u-v).sum() for i,u in scanners.items() for j,v in scanners.items()])


def find_match(scan0, scan1): #transform scan1 in coordinates of scan0, if possible
    d0, d1 = [{np.linalg.norm(s[i]-s[j]):(i,j) for i in range(len(s)) for j in range(i+1,len(s))} for s in (scan0,scan1)]
    common_dist = set(d0) & set(d1)

    indices0 = set([i for c in common_dist for i in d0[c]])
    indices1 = set([i for c in common_dist for i in d1[c]])
#    print(indices0, indices1, len(indices0), len(indices1))
    common_beacons0 = scan0[sorted(indices0)]
    common_beacons1 = scan1[sorted(indices1)]
    
    corr = []
    for idx in indices0:
        D = set(np.linalg.norm(scan0[idx]-scan0[j]) for j in indices0)
        for i in indices1:
            D1 = set(np.linalg.norm(scan1[i]-scan1[j]) for j in indices1)
            if D1 == D:
                print(f"Found correspondence: {idx} (scan in 0-coord) => {i} (other scan)")
                corr.append((idx,i))
                break

    if len(corr) < 12:
        print("Not enough correspondences, no good")
        return None, None

    print(corr)
    a,b = corr[0]
    c,d = corr[1]
    for p in permutations(range(3),3):
        for s in product((-1,1),repeat=3):
            diff0 = scan0[a]-scan0[c]
            diff1 = scan1[b]-scan1[d]
            if all(diff1[p,]*s == diff0):
                print(diff1[p,]*s, diff0, "with transform:", p, s)
                reorient = p, s
                break

    p, s = reorient
    translation = scan0[a] - scan1[b,p]*s
    print(translation,p,s)

    scan1_reoriented = np.array([r[p,]*s for r in scan1])
    scan1_transformed = scan1_reoriented + translation
    return scan1_transformed, translation

def main(filename):
    reports = parse(filename)
    beacons, scanners = do(reports)
    return len(beacons), manhattan(scanners)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
