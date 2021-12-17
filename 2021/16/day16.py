VERBOSE = False

def hex2bin(h):
    return "".join([f"{int(c,base=16):04b}" for c in h])
    
def bin2dec(*x):
    return int("".join(list(x)),base=2)

from functools import reduce
from dataclasses import dataclass, field
from typing import List
from pprint import pprint 

OPS = { 0: lambda *z : reduce(lambda x,y: x+y, z, 0),
        1: lambda *z : reduce(lambda x,y: x*y, z, 1),
        2: min, 
        3: max, 
        5: lambda x,y: int(x > y),
        6: lambda x,y: int(x < y),
        7: lambda x,y: int(x == y)
        }

@dataclass
class Packet:
    version: int
    
    def sum_versions(self):
        raise NotImplementedError

@dataclass
class Literal(Packet):
    value: int

    def sum_versions(self):
        return self.version

@dataclass
class Operator(Packet):
    optype: int
    children: List[Packet] = field(default_factory=list)

    def sum_versions(self):
        return self.version + sum(c.sum_versions() for c in self.children)

    @property
    def value(self):
        if len(self.children) == 0:
            return 0
        elif len(self.children) == 1:
            return self.children[0].value
        return OPS[self.optype](*[c.value for c in self.children])

def parse_hex(h):
    if VERBOSE: print("######################", h)
    packets = parse_all(hex2bin(h))
    if VERBOSE: pprint(packets)
    return sum(p.sum_versions() for p in packets), sum([p.value for p in packets])

def parse_all(raw):
    """ Returns list of packets parsed in input string 'raw'"""
    packets = []
    remaining = raw
    while remaining != "":
        packet, remaining = parse_one(remaining)
        if packet:
            packets.append(packet)
    return packets

def parse_one(raw):
    """Parse ONE packet (or sub-packet), and return what is left."""
    if VERBOSE: print("PARSING:", "".join(list(raw)), f"({len(raw)})")
    match list(raw):
        case [v0,v1,v2,"1","0","0",*rest]:
            if VERBOSE: print("literal header:", "".join([v0,v1,v2]), "100")
            version = int("".join([v0,v1,v2]),base=2)
            lit, remaining = parse_literal(rest)
            return Literal(version=version, value=bin2dec(lit)), remaining
        case [v0,v1,v2,t0,t1,t2,*rest]:
            version = bin2dec(v0,v1,v2)
            optype = bin2dec(t0,t1,t2)
            if VERBOSE: print("operator header:", "".join([v0,v1,v2]), "".join([t0,t1,t2]))
            subpackets, remaining = parse_perator(rest)
            return Operator(optype=optype, version=version, children=subpackets), remaining
        case _:
            if VERBOSE: print("All this can't be parsed:", raw)
            return None, ""

def parse_literal(raw):
    """Parse literal *payload* (not header) and return literal value in binary (plus remaining string)"""
    if VERBOSE: print("matching", "".join(list(raw)))
    match list(raw):
        case ["1",*rest]:
            lit = "".join(rest[:4])
            if VERBOSE: print("Intermediate chunk of literal:", lit, ", remaining:", "".join(rest[4:]))
            lit, remaining = parse_literal(rest[4:])
            return "".join(rest[:4]) + lit, remaining
        case ["0", *rest]:
            lit = "".join(rest[:4])
            remaining = rest[4:]
            if VERBOSE: print("Last chunk of literal:", lit, ", remaining:", "".join(remaining))
            return lit, remaining
        case o:
            print("Literal parsing failed, couldn't match:", o)
            raise ValueError

def parse_perator(raw):
    """Parse operator *payload* (not header) and return subpackets (+ remaining, unparsed string)"""
    if VERBOSE: print("matching", "".join(list(raw)))
    match list(raw):
        case ["0", *rest]:
            if len(rest) < 15: return [], raw
            length = int("".join(rest[:15]), base=2)
            if VERBOSE: print("length [0] (num bits):", length)
            subpackets = parse_all(rest[15:15+length]) 
            return subpackets, rest[15+length:]
        case ["1", *rest]:
            if len(rest) < 11: return [], raw
            num_subpackets = int("".join(rest[:11]), base=2)
            if VERBOSE: print("length [1] (num subpackets):", num_subpackets)
            remaining = rest[11:]
            subpackets = []
            for _ in range(num_subpackets):
                packet, remaining = parse_one(remaining)
                subpackets.append(packet)
            return subpackets, remaining
        case _:
            if VERBOSE: print("Operator parsing failed, couldn't match:", o)
            return [], raw


print(parse_hex("D2FE28"), "011111100101")
print(parse_hex("38006F45291200"), (10,20))
print(parse_hex("EE00D40C823060"), (1,2,3))
print(parse_hex("8A004A801A8002F478"), "exp.version=16")
print(parse_hex("620080001611562C8802118E34"), "exp.version=12")
print(parse_hex("C0015000016115A2E0802F182340"), "exp.version=23")
print(parse_hex("A0016C880162017C3686B18A3D4780"), "exp.version=31")

def main(filename):
    line = open(filename).read().strip()
    return parse_hex(line)

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
