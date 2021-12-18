from dataclasses import dataclass
from typing import Union, Optional
from pprint import pprint, pformat

@dataclass
class Number:
    left: Union['Number', int]
    right: Union['Number', int]
    parent: Optional['Number'] = None
    depth: int = 0
    
    def isleave(self):
        return isinstance(left,int) and isinstance(self.right,int)

    @property
    def __int__(self):
        return 3*int(self.left) + 2*int(self.left)

    def __add__(self, b):
        #do addition
        c = Number(left=self, right=b)
        c.update()
        #c.reduce()
        return c

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    def update(self, depth=0, parent=None):
        self.depth = depth
        self.parent = parent
        if isinstance(self.left, Number):
            self.left.update(depth + 1, self)
        if isinstance(self.right, Number):
            self.right.update(depth + 1, self)
 
    def reduce(self):
        while self.explode() or self.split():
            pass

    def explode(self):
        stack = [self]
        pre = None
        while stack:
            cur = stack.pop()
            if cur.depth == 4:
                break
            if isinstance(cur.right, Number): stack.append(cur.right)
            if isinstance(cur.left, Number): stack.append(cur.left)
            pre = cur

        if cur.depth < 4:
            return False
        
        print("Exploding:", cur)
        l,r = cur.left, cur.right
        assert isinstance(l, int)
        assert isinstance(r, int)

        # Finding rightmost value on the *left*
        if pre:
            if isinstance(pre.right, int):
                pre.right += l
            else:
                pre.left += l

        # Finding leftmost value on the *right*
        if stack and (post := stack.pop()):
            if isinstance(post.left, int):
                post.left += r
            else:
                post.right += r

        if cur is cur.parent.left:
            cur.parent.left = 0
        else:
            cur.parent.right = 0

        self.update()
        return True

    def __iter__(self):
        stack = [self]
        while stack:
            cur = stack.pop()
            yield cur
            if isinstance(cur.right, Number): stack.append(cur.right)
            if isinstance(cur.left, Number): stack.append(cur.left)


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
        return int(line[0]), line[1:]


def main(filename):
    numbers = [parse(l.strip()) for l in open(filename)]
    pprint(numbers)
    for n in numbers:
        n.update()
        pprint(n)
    #sum(numbers)
            

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
