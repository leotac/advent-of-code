from collections import Counter

def main(filename):
    lines = open(filename).readlines()
    s = lines[0].strip()
    rules = {tuple(l.split()[0]): l.split()[2].strip() for l in lines[2:]}
    for i in range(10):
        s = [c for p in zip(s[:-1],s[1:]) for c in (p[0],rules.get(p,''))] + list(s[-1])
    c = Counter(s).most_common()
    return c[0][1] - c[-1][1] 

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
