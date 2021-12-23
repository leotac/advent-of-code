import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Block:
    x: Tuple
    y: Tuple
    z: Tuple
    sign: int

    @property
    def volume(self):
        return self.sign*(self.x[1] - self.x[0] + 1)*(self.y[1] - self.y[0] + 1)*(self.z[1] - self.z[0] + 1)

def apply(action, blocks):
    newblocks = []
    if action[0] == "on":
        newblocks.append(Block(x=(action[1],action[2]), y=(action[3],action[4]), z=(action[5],action[6]), sign=1))

    for b in blocks:
        if (o := overlap(action, b)) is not None:
            newblocks.append(o)

    return newblocks

def overlap(action, b:Block):
    x = max(action[1], b.x[0]), min(action[2], b.x[1])
    y = max(action[3], b.y[0]), min(action[4], b.y[1])
    z = max(action[5], b.z[0]), min(action[6], b.z[1])

    if x[0] > x[1] or y[0] > y[1] or z[0] > z[1]:
        return None

    return Block(x=x, y=y, z=z, sign=-b.sign)#

def reboot(actions):
    blocks = []
    for i, action in enumerate(actions):
        blocks += apply(action, blocks)

    return sum(b.volume for b in blocks)

def parse(l):
    state, coords = l.strip().split()
    ranges = [int(v) for c in coords.split(",") for v in c[2:].split("..")]
    return [state, *ranges]

def main(filename):
    steps = [parse(l) for l in open(filename)]
    first = reboot(steps[:20])
    second = reboot(steps)
    return first, second

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}")
