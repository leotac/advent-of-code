from functools import reduce

OPEN = {"(":1, "[":2, "{":3, "<":4}
CLOSE = {")":3, "]":57, "}":1197, ">":25137}
MATCH = dict(zip(OPEN, CLOSE))

def check(s):
    stack = []
    for c in s:
        if c in OPEN:
            stack.append(c)
        elif c in CLOSE:
            if c != MATCH[stack.pop()]:
                return CLOSE[c], 0
    return 0, reduce(lambda t, c: t*5 + OPEN[c], reversed(stack), 0)

def main(filename):
    scores = [check(l.strip()) for l in open(filename)]
    first = sum(a for a,b in scores if a)
    second = sorted(b for a,b in scores if b)
    second = second[int(len(second)/2)]
    return first, second

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
