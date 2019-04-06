# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        node = self.head
        count_even = 0
        count_odd = 0
        while node:
            if node.value % 2 == 0:
                count_even += 1
                if count_even == 1:
                    node_first_even = node
                    node_even = node_first_even
                    node = node.next_node
                    continue
                node_even.next_node = node
                node_even = node_even.next_node
                node = node.next_node
                continue
            if node.value % 2 != 0:
                count_odd += 1
                if count_odd == 1:
                    self.head = node
                    node_odd = self.head
                    node = node.next_node
                    continue
                node_odd.next_node = node
                node_odd = node_odd.next_node
                node = node.next_node
        if count_odd ==0 or count_even == 0:
            pass
        else:
            node_odd.next_node = node_first_even
            node_even.next_node = None

        # Replace pass above with your code
    
    
    
