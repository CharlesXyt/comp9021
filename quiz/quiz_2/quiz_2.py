# Written by *** and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers, the largest possible value
and the length of L being input by the user, and generates:
- a list "fractions" of strings of the form 'a/b' such that:
    . a <= b;
    . a*n and b*n both occur in L for some n
    . a/b is in reduced form
  enumerated from smallest fraction to largest fraction
  (0 and 1 are exceptions, being represented as such rather than as 0/1 and 1/1);
- if "fractions" contains then 1/2, then the fact that 1/2 belongs to "fractions";
- otherwise, the member "closest_1" of "fractions" that is closest to 1/2,
  if that member is unique;
- otherwise, the two members "closest_1" and "closest_2" of "fractions" that are closest to 1/2,
  in their natural order.
'''


import sys
from random import seed, randint
from math import gcd


try:
    arg_for_seed, length, max_value = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length, max_value = int(arg_for_seed), int(length), int(max_value)
    if arg_for_seed < 0 or length < 0 or max_value < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(0, max_value) for _ in range(length)]
if not any(e for e in L):
    print('\nI failed to generate one strictly positive number, giving up.')
    sys.exit()
print('\nThe generated list is:')
print('  ', L)

fractions = []
spot_on, closest_1, closest_2 = [None] * 3
# Replace this comment with your codel
fractions_process = []
list.sort(L)
for i in range(1,len(L)):
    if L[i] == 0:
        L.pop(i)
    if L[i] > 0:
        break
L_comp = []
for i in range(0, len(L)):
    if L[i] == 0:
        L_comp.append('0')
        fractions_process.append('0')
        continue
    for j in range(i, len(L)):
        m, n = int(L[i]), int(L[j])
        g = gcd(L[i], L[j])
        m /= g
        n /= g
        m, n = int(m), int(n)
        if f'{m}/{n}' in fractions_process:
            continue
        L_comp.append(f'{m/n:0.5f}')
        fractions_process.append(f'{m}/{n}')

L_comp1 = []
for i in L_comp:
	L_comp1.append(float(i))
medium = 2
count = 0
while True:
    count += 1
    for i in range(0,len(L_comp)):
        if medium > float(L_comp[i]):
            medium = float(L_comp[i])
            index = i
        else:
            continue
    L_comp[index] = 2
    medium = 2
    if fractions_process[index] == '1/1':
        fractions.append('1')
    else:
        fractions.append(fractions_process[index])
    if count == len(L_comp):
        break
list.sort(L_comp1)
for i in range(len(L_comp1)):
    if L_comp1[i] == 0.5:
        spot_on = True
        if (0.5 - L_comp1[i - 1]) - (L_comp1[i + 1] - 0.5) > 0:
            closest_1 = fractions[i + 1]
            break
        elif (0.5 - L_comp1[i - 1]) - (L_comp1[i + 1] - 0.5) < 0:
            closest_1 = fractions[i - 1]
            break
        else:
            closest_1 = fractions[i - 1]
            closest_2 = fractions[i + 1]
            break






print('\nThe fractions no greater than 1 that can be built from L, from smallest to largest, are:')
print('  ', '  '.join(e for e in fractions))
if spot_on:
    print('One of these fractions is 1/2')
elif closest_2 is None:
    print('The fraction closest to 1/2 is', closest_1)
else:
    print(closest_1, 'and', closest_2, 'are both closest to 1/2')
