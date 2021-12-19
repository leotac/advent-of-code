from dataclasses import dataclass
from typing import Union, Optional
from colorama import Fore, Style
from copy import deepcopy

VERBOSE=False

@dataclass
class Int:
    magnitude: int
    parent: Optional['Number'] = None

    def __int__(self):
        return self.magnitude
    def __repr__(self):
        if self.magnitude >= 10:
            return Fore.RED + f"{self.magnitude}" + Fore.RESET
        return f"{self.magnitude}"
    def update(self, depth=0, parent=None):
        self.parent = parent

@dataclass
class Number:
    left: Union['Number', int]
    right: Union['Number', int]
    parent: Optional['Number'] = None
    depth: int = 0
    
    def __int__(self):
        return 3*int(self.left) + 2*int(self.right)

    def __add__(self, b):
        c = deepcopy(Number(left=self, right=b))
        c.update()
        c.reduce()
        return c

    def __repr__(self):
        if self.depth >= 4:
            return Style.BRIGHT + f"[{self.left},{self.right}]" + Style.RESET_ALL
        return f"[{self.left},{self.right}]"

    def update(self, depth=0, parent=None):
        self.depth = depth
        self.parent = parent
        self.left.update(depth + 1, self)
        self.right.update(depth + 1, self)
 
    def reduce(self):
        if VERBOSE: print(">", self)
        while self.explode() or self.split():
            self.update()
            if VERBOSE: print(">", self)

    def explode(self):
        pre = None
        it = iter(self)
        for cur in it:
            if isinstance(cur, Number) and cur.depth == 4:
                break
            if isinstance(cur, Int):
                # save previous leaf encountered
                pre = cur

        if isinstance(cur,Int) or cur.depth < 4:
            return False
        
        l,r = next(it), next(it)
        assert isinstance(l, Int)
        assert isinstance(r, Int)

        if VERBOSE: print("Exploding", cur)
        # Finding rightmost leaf value on the *left*, if any
        if pre:
            assert isinstance(pre, Int)
            pre.magnitude += int(l)

        # Finding leftmost leaf value on the *right*, if any
        try:
            while not isinstance(post := next(it), Int):
                pass
            assert isinstance(post, Int)
            post.magnitude += int(r)
        except StopIteration:
            pass

        if cur is cur.parent.left:
            cur.parent.left = Int(0)
        else:
            cur.parent.right = Int(0)
        return True

    def split(self):
        for cur in self:
            if isinstance(cur, Int) and (v := int(cur)) >= 10:
                if VERBOSE: print("Splitting on", cur, "with parent:", cur.parent)
                if cur is cur.parent.left:
                    cur.parent.left = Number(left=Int(v//2), right=Int(v//2 + v%2))
                elif cur is cur.parent.right:
                    cur.parent.right = Number(left=Int(v//2), right=Int(v//2 + v%2))
                else:
                    raise ValueError
                return True
        return False

    def __iter__(self):
        stack = [self]
        while stack:
            cur = stack.pop()
            yield cur
            if isinstance(cur, Number):
                stack.append(cur.right)
                stack.append(cur.left)


def parse(line):
    p, rest =  _parse(line)
    assert not rest
    p.update()
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
    numbers = [parse(l.strip()) for l in open(filename)]
    a = numbers[0]
    for b in numbers[1:]:
        a += b
    first = int(a)
    second1 = max(int(numbers[i] + numbers[j]) for i in range(len(numbers)) for j in range(i+1,len(numbers)))
    second2 = max(int(numbers[j] + numbers[i]) for i in range(len(numbers)) for j in range(i+1,len(numbers)))
    return first, second1, second2

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
