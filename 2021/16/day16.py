VERBOSE = False

class Parser:
    def __init__(self):
        self.version = 0

    def parse_hex(self, h):
        print("#######", h)
        self.version = 0
        ret = self.parse_all(self.hex2bin(h))
        return ret, self.version
    
    def hex2bin(self, h):
        return "".join([f"{int(c,base=16):04b}" for c in h])

    def parse_all(self, raw):
        tot = ""
        remaining = raw
        while remaining != "":
            parsed, remaining = self.parse(remaining)
            tot += parsed
        return tot

    def parse(self, raw, max_depth=None):
        """Parse ONE packet (or sub-packet), and what is left.."""
        if VERBOSE: print("PARSING:", "".join(list(raw)), f"({len(raw)})")
        match list(raw):
            case [v0,v1,v2,"1","0","0",*rest]:
                if VERBOSE: print("literal header:", "".join([v0,v1,v2]), "100")
                version = int("".join([v0,v1,v2]),base=2)
                self.version += version
                if VERBOSE: print(f"L, {version=}", self.version)
                lit, remaining = self.literal(rest, prefix="(")
                return lit, remaining
            case [v0,v1,v2,t0,t1,t2,*rest]:
                version = int("".join([v0,v1,v2]),base=2)
                self.version += version
                if VERBOSE: print(f"O, {version=}", self.version)
                if VERBOSE: print("operator header:", "".join([v0,v1,v2]), "".join([t0,t1,t2]))
                op, remaining = self.operator(rest)
                return op, remaining
            case _:
                if VERBOSE: print("All this can't be parsed:", raw)
                return "", ""
 
   
    def literal(self, raw, prefix=""):
        """Parse literal *payload* (not header)"""
        if VERBOSE: print("matching", "".join(list(raw)))
        match list(raw):
            case ["1",*rest]:
                lit = "".join(rest[:4])
                if VERBOSE: print("Intermediate chunk of literal:", lit, ", remaining:", "".join(rest[4:]))
                lit, remaining = self.literal(rest[4:])
                return prefix + "".join(rest[:4]) + lit, remaining
            case ["0", *rest]:
                lit = "".join(rest[:4])
                remaining = rest[4:]
                if VERBOSE: print("Last chunk of literal:", lit, ", remaining:", "".join(remaining))
                return prefix + lit + ")", remaining
            case o:
                print("Literal parsing failed, couldn't match:", o)
                raise ValueError
    
    def operator(self, raw):
        """Parse operator *payload* (not header)"""
        if VERBOSE: print("matching", "".join(list(raw)))
        match list(raw):
            case ["0", *rest]:
                if len(rest) < 15:
                    return "", raw
                length = int("".join(rest[:15]), base=2)
                if VERBOSE: print("length [0] (num bits):", length)
                return "[" + self.parse_all(rest[15:15+length]) + "]", rest[15+length:]
            case ["1", *rest]:
                subpackets = int("".join(rest[:11]), base=2)
                if VERBOSE: print("length [1] (num subpackets):", subpackets)
                remaining = rest[11:]
                pp = ""
                for _ in range(subpackets):
                    parsed, remaining = self.parse(remaining)
                    pp += parsed
                return "[" + pp + "]", remaining
            case o:
                print("Operator parsing failed, couldn't match:", o)
                return "", o

p = Parser()
print(p.parse_hex("D2FE28"), "011111100101")
print(p.parse_hex("38006F45291200"), (10,20))
print(p.parse_hex("EE00D40C823060"), (1,2,3))
print(p.parse_hex("8A004A801A8002F478"), "exp.version=16")
print(p.parse_hex("620080001611562C8802118E34"), "exp.version=12")
print(p.parse_hex("C0015000016115A2E0802F182340"), "exp.version=23")
print(p.parse_hex("A0016C880162017C3686B18A3D4780"), "exp.version=31")

def main(filename):
    line = open(filename).read()[0]
    p = Parser()
    p.parse_hex(line)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
