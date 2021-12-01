import numpy as np

def main(filename, win):
    a = np.array([int(x) for x in open(filename)])
    return (np.diff(np.convolve(a, np.ones(win), mode="valid")) > 0).sum()

if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    for win in (1,3):
        ret = main(filename, win)
        print(f"{ret} increasing elements with {win=}") 
