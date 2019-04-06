# Generates a binary tree T whose shape is random and whose nodes store
# random even positive integers, both random processes being directed by user input.
# With M being the maximum sum of the nodes along one of T's branches, minimally expands T
# to a tree T* such that:
# - every inner node in T* has two children,
# - the sum of the nodes along all of T*'s branches is equal to M.
#
# Written by *** and Eric Martin for COMP9021


import sys
from random import seed, randrange

from binary_tree_adt import *


def create_tree(tree, for_growth, bound):
    if randrange(max(for_growth, 1)):
        tree.value = 2 * randrange(bound + 1)
        tree.left_node = BinaryTree()
        tree.right_node = BinaryTree()
        create_tree(tree.left_node, for_growth - 1, bound)
        create_tree(tree.right_node, for_growth - 1, bound)


def expand_tree(tree):
    l = []
    find(tree,tree.value,l)
    sum = max(l)
    sum -= tree.value
    expand(tree,sum)


    # Replace pass above with your code


# Possibly define other functions
def find(tree,sum,l = list):
    if tree.left_node.value == None and tree.right_node.value == None:
        l.append(sum)
        return
    if tree.left_node.value and tree.right_node.value ==None:
        sum +=tree.left_node.value
        find(tree.left_node,sum,l)
        return
    elif tree.right_node.value and tree.left_node.value ==None:
        sum+=tree.right_node.value
        find(tree.right_node,sum,l)
        return
    else:
        sum1 = sum + tree.left_node.value
        sum2 =sum + tree.right_node.value
        find(tree.left_node, sum1, l)
        find(tree.right_node, sum2, l)
        return
def expand(tree,sum):
    if tree.left_node.value ==None and tree.right_node.value == None:
        if sum!=0:
            tree.left_node = BinaryTree(sum)
            tree.right_node = BinaryTree(sum)
    elif tree.left_node.value ==None and tree.right_node.value:
        tree.left_node = BinaryTree(sum)
        sum -= tree.right_node.value
        expand(tree.right_node,sum)
        return
    elif tree.left_node.value and tree.right_node.value ==None:
        tree.right_node = BinaryTree(sum)
        sum -= tree.left_node.value
        expand(tree.left_node,sum)
        return
    else:
        sum1 =sum - tree.right_node.value
        sum2 =sum - tree.left_node.value
        expand(tree.right_node, sum1)
        expand(tree.left_node, sum2)
        return




try:
    for_seed, for_growth, bound = [int(x) for x in input('Enter three positive integers: ').split()
                                   ]
    if for_seed < 0 or for_growth < 0 or bound < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
tree = BinaryTree()
create_tree(tree, for_growth, bound)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
expand_tree(tree)
print('Here is the expanded tree:')
tree.print_binary_tree()







