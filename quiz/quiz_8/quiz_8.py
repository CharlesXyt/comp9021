# Randomly fills a grid of size 10 x 10 with digits between 0
# and bound - 1, with bound provided by the user.
# Given a point P of coordinates (x, y) and an integer "target"
# also all provided by the user, finds a path starting from P,
# moving either horizontally or vertically, in either direction,
# so that the numbers in the visited cells add up to "target".
# The grid is explored in a depth-first manner, first trying to move north,
# always trying to keep the current direction,
# and if that does not work turning in a clockwise manner.
#
# Written by Eric Martin for COMP9021


import sys
from random import seed, randrange

from stack_adt import *


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))

def explore_depth_first(x, y, target):
    direction = {
        'W':lambda a,b:(a,b-1),
        'N':lambda a,b:(a-1,b),
        'E':lambda a,b:(a,b+1),
        'S':lambda a,b:(a+1,b)
    }
    next_step ={
        'start':('W','S','E','N'),
        'N':('W','E','N'),
        'E':('N','S','E'),
        'S':('E','W','S'),
        'W':('S','N','W')
    }
    stack =Stack()
    stack.push(([(x,y)],grid[x][y],'start'))
    while not stack.is_empty():
        path,sum,old_direction = stack.pop()
        if sum == target:
            return path
        old_x = path[-1][0]
        old_y = path[-1][1]
        for next in next_step[old_direction]:
            new_sum = 0
            new_x,new_y =direction[next](old_x,old_y)
            if (new_x,new_y) in path:
                continue
            if new_x not in range(10) or new_y not in range(10):
                continue
            path_record = []
            for i in path:
                path_record.append(i)
            path_record.append((new_x,new_y))
            new_sum = sum +grid[new_x][new_y]
            if new_sum>target:
                continue
            else:
                stack.push((path_record,new_sum,next))
    return None

try:
    for_seed, bound, x, y, target = [int(x) for x in input('Enter five integers: ').split()]
    if bound < 1 or x not in range(10) or y not in range(10) or target < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [[randrange(bound) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
path = explore_depth_first(x, y, target)
if not path:
    print(f'There is no way to get a sum of {target} starting from ({x}, {y})')
else:
    print('With North as initial direction, and exploring the space clockwise,')
    print(f'the path yielding a sum of {target} starting from ({x}, {y}) is:')
    print(path)
