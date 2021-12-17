from functools import reduce
from dataclasses import dataclass, field
from typing import List
from pprint import pprint 

VERBOSE = False

def hex2bin(h):
    return "".join([f"{int(c,base=16):04b}" for c in h])
    
def bin2dec(*x):
    return int("".join(list(x)),base=2)

def tostr(x):
    return "".join(x)

OPS = { 0: sum,
        1: lambda z : reduce(lambda x,y: x*y, z, 1),
        2: min, 
        3: max, 
        5: lambda z: int(z[0] > z[1]),
        6: lambda z: int(z[0] < z[1]),
        7: lambda z: int(z[0] == z[1])
        }

@dataclass
class Packet:
    version: int

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
        if self.children:
            return OPS[self.optype]([c.value for c in self.children])
        return 0

def parse_hex(h):
    if VERBOSE: print("##########", h)
    packets = parse_all(hex2bin(h))
    if VERBOSE: pprint(packets)
    return packets, sum(p.sum_versions() for p in packets), sum([p.value for p in packets])

def parse_all(raw):
    """ Returns list of packets parsed in input string 'raw'"""
    packets = []
    remaining = raw
    while remaining:
        packet, remaining = parse_one(remaining)
        if packet: packets.append(packet)
    return packets

def parse_one(raw):
    """Parse ONE packet (or sub-packet), and return what is left."""
    match list(raw):
        case [v0,v1,v2,"1","0","0",*rest]:
            version = bin2dec(v0,v1,v2)
            lit, remaining = parse_literal(rest)
            return Literal(version=version, value=bin2dec(lit)), remaining
        case [v0,v1,v2,t0,t1,t2,*rest]:
            version = bin2dec(v0,v1,v2)
            optype = bin2dec(t0,t1,t2)
            subpackets, remaining = parse_operator(rest)
            return Operator(optype=optype, version=version, children=subpackets), remaining
        case _:
            return None, ""

def parse_literal(raw):
    """Parse literal *payload* (not header) and return literal value in binary (plus remaining string)"""
    match list(raw):
        case ["1",*rest]:
            lit, remaining = parse_literal(rest[4:])
            return tostr(rest[:4]) + lit, remaining
        case ["0", *rest]:
            lit, remaining = tostr(rest[:4]), rest[4:]
            return lit, remaining
        case _:
            raise ValueError("Literal parsing failed, couldn't match:", raw)

def parse_operator(raw):
    """Parse operator *payload* (not header) and return subpackets (+ remaining, unparsed string)"""
    match list(raw):
        case ["0", *rest]:
            if len(rest) < 15: return [], raw
            length = int("".join(rest[:15]), base=2)
            subpackets = parse_all(rest[15:15+length]) 
            return subpackets, rest[15+length:]
        case ["1", *rest]:
            if len(rest) < 11: return [], raw
            num_subpackets = int("".join(rest[:11]), base=2)
            remaining = rest[11:]
            subpackets = []
            for _ in range(num_subpackets):
                packet, remaining = parse_one(remaining)
                subpackets.append(packet)
            return subpackets, remaining
        case _:
            return [], raw

assert parse_hex("D2FE28")[0][0].value == 2021
assert parse_hex("8A004A801A8002F478")[1] == 16
assert parse_hex("620080001611562C8802118E34")[1] == 12
assert parse_hex("C0015000016115A2E0802F182340")[1] == 23
assert parse_hex("A0016C880162017C3686B18A3D4780")[1] == 31
assert parse_hex("9C0141080250320F1802104A08")[2] == 1

def main(filename):
    line = open(filename).read().strip()
    packets, versions, values = parse_hex(line)
    return versions, values

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
