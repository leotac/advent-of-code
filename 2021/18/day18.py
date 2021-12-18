from dataclasses import dataclass
from typing import Union
from pprint import pprint, pformat

@dataclass
class Int:
    magnitude: int

@dataclass
class Number:
    left: Union['Number', 'Int']
    right: Union['Number', 'Int']
    depth: int = 0

    @property
    def magnitude(self):
        return 3*left.magnitude + 2*left.magnitude

    def __add__(self, b):
        #do addition
        c = Number(left=self, right=b)
        c.update()
        #c.reduce()
        return c

    def reduce(self):
        pass

    def update(self, depth=0):
        self.depth = depth
        if isinstance(self.left, Number):
            self.left.update(depth + 1)
        if isinstance(self.right, Number):
            self.right.update(depth + 1)
    
def parse(line):
    p, rest =  _parse(line)
    assert not rest
    return p

def _parse(line):
    if line[0] == "[":
        left, rest = _parse(line[1:])
        assert rest[0] == ","
        right, rest = _parse(rest[1:])
        assert rest[0] == "]"
        return Number(left=left, right=right), rest[1:]
    else: 
        assert line[1] in (",","]")
        return Int(int(line[0])), line[1:]


def main(filename):
    numbers = [parse(l.strip())[0] for l in open(filename)]
    pprint(numbers)
    for n in numbers:
        n.update()
        pprint(n)
    #sum(numbers)
            

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
