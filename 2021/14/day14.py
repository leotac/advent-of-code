from collections import Counter, defaultdict

def parse(filename):
    lines = open(filename).readlines()
    s = lines[0].strip()
    rules = {l.split()[0]: l.split()[2].strip() for l in lines[2:]}
    return s, rules

def part1(filename, N): # naive
    s, rules = parse(filename)
    for i in range(N):
        s = [c for p in zip(s[:-1],s[1:]) for c in (p[0],rules.get(''.join(p),''))] + list(s[-1])
    c = Counter(s).most_common()
    return c[0][1] - c[-1][1] 

def part2(filename, N): # smarter
    s, rules = parse(filename)
    
    counts = defaultdict(int)
    for p in zip(s[:-1],s[1:]):
        counts["".join(p)] += 1

    for i in range(N):
        oldcounts = counts.copy()
        counts = defaultdict(int)
        for r,c in oldcounts.items():
            if r in rules:
                counts[r[0]+rules[r]] += c
                counts[rules[r] + r[1]] += c
            else:
                counts[r] += c

    letter_counts = defaultdict(int)
    for p,v in counts.items():
        letter_counts[p[0]] += v
        letter_counts[p[1]] += v
    letter_counts[s[0]] += 1
    letter_counts[s[-1]] += 1

    assert all(v%2 == 0 for v in letter_counts.values())
    return (max(letter_counts.values()) - min(letter_counts.values())) // 2

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = part1(filename, 10)
    print(f"{ret=}") 
    ret = part2(filename, 40)
    print(f"{ret=}") 
