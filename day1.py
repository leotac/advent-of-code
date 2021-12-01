import sys
import numpy as np

def main(filename, win):
    a = np.array([int(x) for x in open(filename)])
    return (np.diff(np.convolve(a, np.ones(win), mode="valid")) > 0).sum()

if __name__ == "__main__":
    filename, win = sys.argv[1], int(sys.argv[2])
    ret = main(filename, win)
    print(f"{ret} increasing elements with {win=}") 
