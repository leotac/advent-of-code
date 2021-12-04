import numpy as np
def read(filename):
    boards = []
    for l in open(filename):
        if "," in l:
            numbers = [int(x) for x in l.strip().split(',')]
        elif len(l.strip()) == 0:
            boards.append([])
        else:
            boards[-1].append([int(x) for x in l.strip().split()])
    boards = np.array(boards)
    return numbers, boards

def main(filename):
    numbers, boards = read(filename)
    print(numbers, boards.shape)
    
    mask = np.zeros(boards.shape, dtype=bool)
    for n in numbers:
        mask = (boards == n) | mask
        # bingo by dim 1 (a col)
        b, _ = np.where(mask.sum(axis = 1) == 5)
        if len(b) > 0:
            winning_board_idx = b[0]
            break
        # bingo by dim 2 (a row)
        b, _ = np.where(mask.sum(axis = 2) == 5)
        if len(b) > 0:
            winning_board_idx = b[0]
            break
    
    winning_board = boards[winning_board_idx]
    winning_mask = mask[winning_board_idx]
    print(winning_board, winning_mask, n)
    score = n*sum(winning_board[~winning_mask])
    return score


def main(filename):
    numbers, boards = read(filename)
    
    mask = np.zeros(boards.shape, dtype=bool)
    num_boards = boards.shape[0]
    won = set()
    for n in numbers:
        mask = (boards == n) | mask
        # bingo by dim 1 (a col)
        a, _ = np.where(mask.sum(axis = 1) == 5)
        # bingo by dim 2 (a row)
        b, _ = np.where(mask.sum(axis = 2) == 5)
        new = (set(a) | set(b)) - won
        won |= new
        
        if len(won) == num_boards:
            last = list(new)[0]
            break
            
    winning_board = boards[last]
    winning_mask = mask[last]
    print(winning_board, winning_mask, n)
    score = n*sum(winning_board[~winning_mask])
    return score


if __name__ == "__main__":
    filename = __file__.replace(".py", ".inp")
    ret = main(filename)
    print(f"{ret=}") 
