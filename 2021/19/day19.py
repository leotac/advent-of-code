import numpy as np
from itertools import permutations, product

VERBOSE=False

def parse(filename):
    reports = []
    for l in open(filename):
        if "---" in l:
            reports.append([])
        elif l.strip() == "":
            continue
        else:
            reports[-1].append([int(x) for x in l.strip().split(",")])
    return [np.array(s) for s in reports]

def align(reports):
    """ Return beacons and scanners, all transformed into the coordinates of scanner 0
    """
    scanners = {0: np.array([0,0,0])}
    
    aligned_reports = {0: reports[0]} # readings in canonical coordinates (i.e., scanner 0)
    unprocessed = [0]   # stack of reports in canonical coordinates that
                        # have been aligned but haven't been used yet to find matches
    
    while len(aligned_reports) < len(reports):
        i = unprocessed.pop()
        for j in range(len(reports)):
            if j not in aligned_reports:
                aligned_report, scanner = match_and_align(aligned_reports[i], reports[j])
                if aligned_report is not None:
                    if VERBOSE: print(f"Found alignment between reports {i} and {j}")
                    aligned_reports[j] = aligned_report
                    scanners[j] = scanner
                    unprocessed.append(j)
                    draw(aligned_report)

    stacked = np.vstack(list(aligned_reports.values()))
    beacons = np.array(sorted(set(tuple(r) for r in stacked)))
    return beacons, scanners

def manhattan(scanners):
    return max([np.abs(u-v).sum() for i,u in scanners.items() for j,v in scanners.items()])

def match_and_align(report0, report1):
    """ Attempt to find beacons in the overlap of report0 and report1, and 
    return report1 transformed according to report0 reference system.
    """
    # Find clique of beacons that have the same pairwise distances in both reports
    d0, d1 = [{np.linalg.norm(s[i]-s[j]):(i,j) for i in range(len(s)) for j in range(i+1,len(s))} for s in (report0,report1)]
    common_dist = set(d0) & set(d1)
    clique0 = set([i for c in common_dist for i in d0[c]])
    clique1 = set([i for c in common_dist for i in d1[c]])
   
    # Match beacons in report0 and report1 based on the distances to other beacons in the clique
    corr = []
    for idx in clique0:
        D = set(np.linalg.norm(report0[idx]-report0[j]) for j in clique0)
        for i in clique1:
            D1 = set(np.linalg.norm(report1[i]-report1[j]) for j in clique1)
            if D1 == D:
                if VERBOSE: print(f"Found beacon match: {idx} (report in 0-coord) => {i} (other reportn)")
                corr.append((idx,i))
                break

    # If we don't match at least 12 beacons, not enough information to confirm the match
    if len(corr) < 12:
        return None, None

    # Get first two beacons (a,b) to find coordinate transformation + translation
    # Reorient/rearrange until the diff vector between a and b must be the same in both reports.
    a0, a1 = corr[0]
    b0, b1 = corr[1]
    for p in permutations(range(3), 3):
        for s in product((-1,1), repeat=3):
            diff0 = report0[a0] - report0[b0]
            diff1 = report1[a1] - report1[b1]
            if all(diff1[p,]*s == diff0):
                reorient = p, s
                break

    # Find position of scanner1 in canonical coordinates (scanner0)
    p, s = reorient
    scanner1 = report0[a0] - report1[a1,p]*s

    report1_reoriented = np.array([r[p,]*s for r in report1])
    report1_aligned = report1_reoriented + scanner1
    return report1_aligned, scanner1

from drawille import Canvas
import os, time
def draw(report, c=Canvas()):
    os.system("clear")
    for x in report:
        c.set(int(x[0]/100),int(x[1]/100))
    print(c.frame(min_x=-50,max_x=50,min_y=-50,max_y=50))
    time.sleep(0.5)

def main(filename):
    reports = parse(filename)
    beacons, scanners = align(reports)
    return len(beacons), manhattan(scanners)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
