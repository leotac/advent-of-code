HEX = "D2FE28"
VERBOSE = True

def parse_hex(h):
    return parse(hex2bin(h), 0)

def hex2bin(h):
    return bin(int(h, base=16))[2:]

def parse(raw, parsed=0):
    if VERBOSE: print("PARSING:", "".join(list(raw)))
    match list(raw):
        case [v0,v1,v2,"1","0","0",*rest]:
            if VERBOSE: print("literal header:", "".join([v0,v1,v2]), "100")
            return "L" + literal(rest)
        case []:
            return ""

def literal(raw, parsed=0):
    """Parse literal *payload* (not header)"""
    if VERBOSE: print("matching", "".join(list(raw)))
    match list(raw):
        case ["1",*rest]:
            lit = "".join(rest[:4])
            if VERBOSE: print("literal:", lit, "remaining:", "".join(rest[4:]))
            return "".join(rest[:4]) + literal(rest[4:], parsed=parsed+5)
        case ["0", *rest]:
            tail = 4 - (parsed % 4)
            lit = "".join(rest[:4])
            remaining = rest[4+tail+1:]
            if VERBOSE: print("literal:", lit, "tail:", rest[4:4+tail+1], "remaining:", "".join(remaining))
            if remaining:
                return lit + "_" + parse(remaining, parsed=parsed+4+tail)
            return lit
        case o:
            print("Literal parsing failed, couldn't match:", o)
            raise ValueError

assert int(parse_hex(HEX)[1:], base=2) == 2021

def main(filename):
    pass

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
