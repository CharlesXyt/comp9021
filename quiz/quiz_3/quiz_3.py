# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for given step_number >= 1
# and step_size >= 2, the number of stairs of step_number many steps,
# with all steps of size step_size.
#
# A stair of 1 step of size 2 is of the form
# 1 1
#   1 1
#
# A stair of 2 steps of size 2 is of the form
# 1 1
#   1 1
#     1 1
#
# A stair of 1 step of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#
# A stair of 2 steps of size 3 is of the form
# 1 1 1
#     1
#     1 1 1
#         1
#         1 1 1
#
# The output lists the number of stairs from smallest step sizes to largest step sizes,
# and for a given step size, from stairs with the smallest number of steps to stairs
# with the largest number of stairs.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def stairs_in_grid():
    L = []
    stair_out = defaultdict(list)
    nb_of_stairs = 1
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0:
                if j == 0:
                    size = 0
                else:
                    for y in range(1,j + 1):
                        if grid[i][j - y] == 0:
                            size = y - 1
                            break
                        if y == j:
                            size = y
                if size == 0:
                    continue
                for t in range(1,size + 1):
                    nb_of_steps = 0
                    L_middle = stair_one_step(i,j,grid,t)
                    if L_middle != False:
                        nb_of_steps = 1
                    else:
                        continue
                    while True:
                        if L_middle not in L:
                            L.append(L_middle)
                            L_middle = stair_one_step(L_middle[2],L_middle[3],grid,t)
                            step_size = t
                            nb_of_steps += 1
                        else:
                            step_size = 0
                            break
                        if L_middle == False:
                            break
                    if step_size == 0:
                        continue
                    if step_size in stair_out:
                        for h in range(len(stair_out[step_size])):
                            if stair_out[step_size][h][0] == nb_of_steps:
                                stair_out[step_size][h][1] = nb_of_stairs + stair_out[step_size][h][1]
                                break
                            if h == len(stair_out[step_size]) - 1:
                                stair_out[step_size].append([nb_of_steps, nb_of_stairs])
                    else:
                        stair_out[step_size].append([nb_of_steps, nb_of_stairs])
            else:
                continue
    return stair_out
    # Replace return {} above with your code

# Possibly define other functions
def stair_one_step(i,j,grid,size):
    i_start = i
    j_start = j
    if i_start >= len(grid) - size or j_start >= len(grid) - size:
        return False
    if grid[i][j] == 0:
        return False
    else:
        for _ in range(size):
            i += 1
            if grid[i][j] == 0:
                return False
        for _ in range(size):
            j += 1
            if grid[i][j] == 0:
                return False
        l =[i_start,j_start,i,j,size]
        return l



try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are step sizes, and whose values are pairs of the form
# (number_of_steps, number_of_stairs_with_that_number_of_steps_of_that_step_size),
# ordered from smallest to largest number_of_steps.
stairs = stairs_in_grid()
stairs1 = defaultdict(list)
for step_size in stairs:
    for i in stairs[step_size]:
        stairs1[step_size + 1].append([i[0] - 1,i[1]])

for step_size in sorted(stairs1):
    print(f'\nFor steps of size {step_size}, we have:')
    stairs1[step_size].sort(key = lambda x: (x[0],x[1]))
    for nb_of_steps, nb_of_stairs in stairs1[step_size]:
        stair_or_stairs = 'stair' if nb_of_stairs == 1 else 'stairs'
        step_or_steps = 'step' if nb_of_steps == 1 else 'steps'
        print(f'     {nb_of_stairs} {stair_or_stairs} with {nb_of_steps} {step_or_steps}')

