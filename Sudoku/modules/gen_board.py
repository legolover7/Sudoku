# Import statementes
import random
import copy

# Randomize rows, columns and numbers (of valid base pattern)
def shuffle(s): 
    return random.sample(s,len(s)) 

# Generates a random sudoku board
def generate(base, percentage=1):
    side = base*base

    # {attern for a baseline valid solution
    def pattern(r,c): 
        return (base*(r%base)+r//base+c)%side

    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # Produce board using randomized baseline pattern
    board = [ [[nums[pattern(r,c)], False, 0, []] for c in cols] for r in rows ]

    solve_board = copy.deepcopy(board)
    

    # Remove percentage amount of nums
    for i in range(base ** 4 - int(percentage * base ** 4)):
        x = random.randint(0, base ** 2-1)
        y = random.randint(0, base ** 2-1)
        while board[x][y] == "":
            x = random.randint(0, base ** 2-1)
            y = random.randint(0, base ** 2-1)
        board[x][y][0] = ""


    return board, solve_board