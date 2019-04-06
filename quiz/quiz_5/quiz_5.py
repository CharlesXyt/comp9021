# Randomly fills a grid of size height and width whose values are input by the user,
# with nonnegative integers randomly generated up to an upper bound N also input the user,
# and computes, for each n <= N, the number of paths consisting of all integers from 1 up to n
# that cannot be extended to n+1.
# Outputs the number of such paths, when at least one exists.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

save = defaultdict(list)
def get_paths():
    save = defaultdict(list)
    for i in range(height):
        for j in range(width):
            find(1,grid,i,j)
    # Replace pass above with your code


# Insert your code for other functions

def find(number,grid,i,j):
    if grid[i][j] == number:
        m = 0
        for count in range(4):
            if count == 0:
                if j + 1 > width - 1:
                    m += 1
                    if m == 4:
                        save[number].append(1)
                    continue
                if grid[i][j + 1] == number + 1:
                    find(number + 1, grid,i,j + 1)
                else:
                    m += 1
            if count == 1:
                if j - 1 < 0:
                    m += 1
                    if m == 4:
                        save[number].append(1)
                    continue
                if grid[i][j - 1] == number + 1:
                    find(number + 1,grid,i,j - 1)
                else:
                    m += 1
            if count == 2:
                if i - 1 < 0:
                    m += 1
                    if m == 4:
                        save[number].append(1)
                    continue
                if grid[i - 1][j] == number + 1:
                    find(number + 1,grid,i - 1,j)
                else:
                    m += 1
            if count == 3:
                if i + 1 > height - 1:
                    m += 1
                    if m == 4:
                        save[number].append(1)
                    continue
                if grid[i + 1][j] == number + 1:
                    find(number + 1,grid,i + 1,j)
                else:
                    m += 1
            if m == 4:
                save[number].append(1)




try:
    for_seed, max_length, height, width = [int(i) for i in
                                           input('Enter four nonnegative integers: ').split()
                                           ]
    if for_seed < 0 or max_length < 0 or height < 0 or width < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[randint(0, max_length) for _ in range(width)] for _ in range(height)]
print('Here is the grid that has been generated:')
display_grid()
get_paths()
paths = defaultdict(int)
for i in save:
    paths[i] = len(save[i])



if paths:
    for length in sorted(paths):
        print(f'The number of paths from 1 to {length} is: {paths[length]}')

