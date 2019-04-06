# Creates a class to represent a permutation of 1, 2, ..., n for some n >= 0.
#
# An object is created by passing as argument to the class name:
# - either no argument, in which case the empty permutation is created, or
# - "length = n" for some n >= 0, in which case the identity over 1, ..., n is created, or
# - the numbers 1, 2, ..., n for some n >= 0, in some order, possibly together with "lengh = n".
#
# __len__(), __repr__() and __str__() are implemented, the latter providing the standard form
# decomposition of the permutation into cycles (see wikepedia page on permutations for details).
#
# Objects have:
# - nb_of_cycles as an attribute
# - inverse() as a method
#
# The * operator is implemented for permutation composition, for both infix and in-place uses.
#
# Written by *** and Eric Martin for COMP9021


class PermutationError(Exception):
    def __init__(self, message):
        self.message = message


class Permutation:
    def __init__(self, *args, length=None):
        self.args = [i for i in args]
        self.length = len(args)
        self._length = length
        if length == None:
            if 0 in args:
                raise PermutationError('Cannot generate permutation from these arguments')
            elif not all(isinstance(i, int) for i in args):
                raise PermutationError('Cannot generate permutation from these arguments')
            elif self.length != len(set(self.args)):
                raise PermutationError('Cannot generate permutation from these arguments')
            elif self.length == 0:
                self.nb_of_cycles = 0
                pass
            else:
                L = self.cycle()
                self.nb_of_cycles = len(L)
        elif length < 0:
            raise PermutationError('Cannot generate permutation from these arguments')
        elif self.length == 0:
            self.args =list(range(1,length+1))
            L = self.cycle()
            self.nb_of_cycles = len(L)
        elif length != self.length:
            raise PermutationError('Cannot generate permutation from these arguments')
        elif 0 in args:
            raise PermutationError('Cannot generate permutation from these arguments')
        elif not all(isinstance(i,int) for i in args):
            raise PermutationError('Cannot generate permutation from these arguments')
        elif self.length != len(set(self.args)):
            raise PermutationError('Cannot generate permutation from these arguments')
        else:
            L = self.cycle()
            self.nb_of_cycles = len(L)

        # Replace pass above with your code

    def __len__(self):
        return len(self.args)
        # Replace pass above with your code

    def __repr__(self):
        output='Permutation('
        for i in range(len(self.args)):
            if i == len(self.args) -1:
                output += f'{self.args[i]}'
            else:
                output += f'{self.args[i]}, '
        output+=')'
        return output

        # Replace pass above with your code

    def cycle(self):
        l = self.args
        M = {i: l[i - 1] for i in range(1, len(l) + 1)}
        L = []
        h = []
        m = 1
        while True:
            h = []
            while True:
                if M[m] not in h:
                    m = M[m]
                    h.append(m)
                else:
                    break
            L.append(h)
            for i in l:
                t = 0
                for j in range(len(L)):
                    if i in L[j]:
                        t = 1
                        break
                if t == 0:
                    m = i
                    break

            if sum(1 for i in range(len(L)) for _ in range(len(L[i]))) == len(l):
                break
        for i in range(len(L)):
            t = L[i].index(max(L[i]))
            L[i] = L[i][t:]+L[i][:t]
        return L

    def __str__(self):
        if len(self.args) == 0 and not self._length:
            output = '()'
        else:
            output = '('
            t = self.cycle()
            t.sort(key = lambda x : x[0])
            for i in range(len(t)):
                for j in  range(len(t[i])):
                    if j ==len(t[i]) -1:
                        output+= f'{t[i][j]}'
                    else:
                        output += f'{t[i][j]} '
                if i == len(t) - 1:
                    output +=')'
                else: output +=')('
        return output
        # Replace pass above with your code

    def __mul__(self, permutation):
        if self.length != permutation.length:
            raise PermutationError('Cannot compose permutations of different lengths')
        M={permutation.args[i]: self.args[i] for i in range(len(self.args))}
        l1 = []
        for i in sorted(M):
            l1.append(M[i])
        return Permutation(*l1)

        # Replace pass above with your code

    def __imul__(self, permutation):
        self.args = self.inverse().args
        M = {permutation.args[i]: self.args[i] for i in range(len(self.args))}
        l1 = []
        for i in sorted(M):
            l1.append(M[i])
        self.args = l1
        return Permutation(*self.args)
        # Replace pass above with your code

    def inverse(self):
        l = self.args
        M = {l[i - 1]:i for i in range(1, len(l) + 1)}
        l1=[]
        for i in sorted(M):
            l1.append(M[i])
        return Permutation(*l1)
        # Replace pass above with your code

        # Insert your code for helper functions, if needed
p1 = Permutation(5, 4, 3,2,2, 1)


print(p1)
