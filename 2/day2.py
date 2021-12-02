
def main1(filename):
    from collections import defaultdict
    d = defaultdict(int)
    for x in open(filename):
        cmd, delta = x.split()
        d[cmd] += int(delta) 
    x = d["forward"]
    y = d["down"] - d["up"]
    return x*y

def main2(filename):
    x, y, aim = 0, 0, 0
    for l in open(filename):
        cmd, delta = l.split()
        if cmd == "down":
            aim += int(delta)
        elif cmd == "up":
            aim -= int(delta)
        elif cmd == "forward":
            x += int(delta)
            y += aim*int(delta)
    return x*y



if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main1(filename)
    print(f"{ret=}") 

    ret = main2(filename)
    print(f"{ret=}") 
