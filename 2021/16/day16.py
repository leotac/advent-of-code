HEX = "D2FE28"
VERBOSE = False

VERSION = 0
def parse_hex(h):
    global VERSION
    VERSION = 0
    ret = parse(hex2bin(h))
    print(VERSION)
    return ret

def hex2bin(h):
    return "".join([f"{int(c,base=16):04b}" for c in h])

def parse(raw, max_depth=None):
    global VERSION
    if VERBOSE: print("PARSING:", "".join(list(raw)))
    if max_depth == 0:
        return ""
    match list(raw):
        case [v0,v1,v2,"1","0","0",*rest]:
            if VERBOSE: print("literal header:", "".join([v0,v1,v2]), "100")
            version = int("".join([v0,v1,v2]),base=2)
            VERSION += version
            print(f"L, {version=}", VERSION)
            if max_depth is None:
                return "(" + literal(rest)
            return "(" + literal(rest, max_depth=max_depth-1)
        case [v0,v1,v2,t0,t1,t2,*rest]:
            version = int("".join([v0,v1,v2]),base=2)
            VERSION += version
            print(f"O, {version=}")
            if VERBOSE: print("operator header:", "".join([v0,v1,v2]), "".join([t0,t1,t2]))
            return "[" + operator(rest)
        case _:
            return ""

def literal(raw, max_depth=None):
    """Parse literal *payload* (not header)"""
    if VERBOSE: print("matching", "".join(list(raw)))
    match list(raw):
        case ["1",*rest]:
            lit = "".join(rest[:4])
            if VERBOSE: print("literal:", lit, "remaining:", "".join(rest[4:]))
            return "".join(rest[:4]) + literal(rest[4:], max_depth=max_depth)
        case ["0", *rest]:
            lit = "".join(rest[:4])
            remaining = rest[4:]
            if VERBOSE: print("literal:", lit, "remaining:", "".join(remaining))
            if remaining:
                return lit + ")" + parse(remaining, max_depth=max_depth)
            return lit
        case o:
            print("Literal parsing failed, couldn't match:", o)
            raise ValueError

def operator(raw):
    """Parse operator *payload* (not header)"""
    pass
    if VERBOSE: print("matching", "".join(list(raw)))
    match list(raw):
        case ["0", *rest]:
            length = int("".join(rest[:15]), base=2)
            if VERBOSE: print("length [0] (num bits):", length)
            return parse(rest[15:15+length+1], max_depth=None) + "]"
        case ["1", *rest]:
            subpackets = int("".join(rest[:11]), base=2)
            if VERBOSE: print("length [1] (num subpackets):", subpackets)
            return parse(rest[11:], max_depth=subpackets) + "]"
        case o:
            print("Literal parsing failed, couldn't match:", o)
            raise ValueError


#print(parse_hex(HEX))
#[1:].strip("()[]"), base=2) == 2021
#assert int(parse_hex(HEX)[1:].strip("()[]"), base=2) == 2021

def main(filename):
    pass

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
