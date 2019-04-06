# Randomly generates N distinct integers with N provided by the user,
# inserts all these elements into a priority queue, and outputs a list
# L consisting of all those N integers, determined in such a way that:
# - inserting the members of L from those of smallest index of those of
#   largest index results in the same priority queue;
# - L is preferred in the sense that the last element inserted is as large as
#   possible, and then the penultimate element inserted is as large as possible, etc.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, sample

from priority_queue_adt import *


# Possibly define some functions
def pre(element,tree):
    h = tree._data.index(element)
    tree._data[h], tree._data[len(tree)] = tree._data[len(tree)], tree._data[h]
    tree._length -= 1
    if tree.min_capacity // 2 <= tree._length <= len(tree._data) // 4:
        tree._resize(len(tree._data) // 2)
    tree._bubble_down(h)
def preferred_sequence():
    prefer_order = []
    tree =PriorityQueue()
    compare = PriorityQueue()
    l_process = list(L)
    l_process.sort(reverse= True)
    for i in L:
        tree.insert(i)
        compare.insert(i)
    while True:
        for i in range(len(l_process)):
            pre(l_process[i],tree)
            tree.insert(l_process[i])
            if tree._data[1:len(tree)+1] == compare._data[1:len(compare)+1]:
                pre(l_process[i], tree)
                pre(l_process[i],compare)
                prefer_order.append(l_process[i])
                l_process.pop(i)
                break
            else:
                tree = PriorityQueue()
                for item in compare._data[1:len(compare)+1]:
                    tree.insert(item)
        if len(l_process) == 0:
            break
    prefer_order.reverse()
    return prefer_order
    # Replace pass above with your code (altogether, aim for around 24 lines of code)


try:
    for_seed, length = [int(x) for x in input('Enter 2 nonnegative integers, the second one '
                                                                             'no greater than 100: '
                                             ).split()
                       ]
    if for_seed < 0 or length > 100:
        raise ValueError
except ValueError:
    print('Incorrect input (not all integers), giving up.')
    sys.exit()    
seed(for_seed)
L = sample(list(range(length * 10)), length)
pq = PriorityQueue()
for e in L:
    pq.insert(e)
print('The heap that has been generated is: ')
print(pq._data[ : len(pq) + 1])
print('The preferred ordering of data to generate this heap by successsive insertion is:')

print(preferred_sequence())
print(pq._data[ : len(pq) + 1])

