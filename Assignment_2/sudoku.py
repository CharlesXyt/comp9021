import os
from itertools import count
from re import sub
from collections import defaultdict

class SudokuError(Exception):
    def __init__(self, message):
        self.message = message

class Sudoku(str):
    def __init__(self,filename = None):
        self._filename = filename
        self.l = self._judge()
        self.L= [[self.l[i][j] for i in range(9)] for j in range(9)]

    def _cut(self,l1,l2):
        l = [self.l[i][j] for i in l1 for j in l2]
        return l

    def preassess(self):
        for i in range(9):
            t =list(self.l[i])
            l_process = []
            for e in t:
                if e !=0:
                    l_process.append(e)
            if len(l_process) !=len(set(l_process)):
                return print('There is clearly no solution.')
        L = [[self.l[i][j] for i in range(9)] for j in range(9)]
        for i in range(9):
            t = list(L[i])
            l_process = []
            for e in t:
                if e != 0:
                    l_process.append(e)
            if len(l_process) != len(set(l_process)):
                return print('There is clearly no solution.')
        l1 = [0,1,2]
        l2 = [3,4,5]
        l3 = [6,7,8]
        l_row = [l1,l2,l3]
        l_col = [l1,l2,l3]
        for i in l_row:
            for j in l_col:
                for _ in range(9):
                    t = self._cut(i,j)
                    l_process = []
                    for e in t:
                        if e != 0:
                            l_process.append(e)
                    if len(l_process) != len(set(l_process)):
                        return print('There is clearly no solution.')
        return print('There might be a solution.')

    def _judge(self):
        with open(self._filename) as file:
            L=[]
            for line in file:
                l = line.split()
                h=[]
                for i in l:
                    if len(i) == 1:
                        h.append(i)
                    else:
                        for e in i:
                            h.append(e)
                if h:
                    L.append(h)
        if len(L) != 9:
            raise SudokuError('Incorrect input')
        for i in range(len(L)):
            for j in range(len(L[i])):
                if len(L[i]) !=9:
                    raise SudokuError('Incorrect input')
                try:
                    L[i][j] = int(L[i][j])
                except:
                    raise SudokuError('Incorrect input')
                L[i][j] = int(L[i][j])
                if L[i][j] not in range(10):
                    raise SudokuError('Incorrect input')
        return L

    def bare_tex_output(self):
        l_mark = [[[] for _ in range(9)] for _ in range(9)]
        for i in range(len(self.l)):
            for j in range(len(self.l[i])):
                if self.l[i][j] == 0:
                    continue
                l_mark[i][j].append(self.l[i][j])
        self._print_tex('bare',l_mark)

    def _force(self):
        l1 = [0, 1, 2]
        l2 = [3, 4, 5]
        l3 = [6, 7, 8]
        l_row = [l1, l2, l3]
        l_col = [l1, l2, l3]
        l_force = self._mark()
        l_forced = self._mark()
        while True:
            for i in range(0,9,3):
                for j in range(0,9,3):
                    for r in l_row:
                        for l in l_col:
                            if i in r and j in l:
                                l_matrix = [l_force[i2][j2] for i2 in r for j2 in l]
                                R = list(r)
                                L = list(l)
                    for nb in range(len(l_matrix)):
                        if len(l_matrix[nb]) ==1:
                            continue
                        for e in l_matrix[nb]:
                            count = 0
                            for other in range(len(l_matrix)):
                                if other == nb or len(l_matrix[other]) ==1:
                                    continue
                                if e in l_matrix[other]:
                                    count +=1
                            if count == 0:
                                col =nb%3 +L[0]
                                row = nb//3 + R[0]
                                l_force[row][col] = [e]
            if l_force == l_forced:
                break
            else:
                l_forced = [[list(l_force[i][j]) for j in range(9)] for i in range(9)]
                l_force = self._mark(l_force)
        return l_force

    def forced_tex_output(self):
        l = self._force()
        for i in range(9):
            for j in range(9):
                if len(l[i][j]) > 1:
                    l[i][j] = []
        self._print_tex('forced',l)

    def _mark(self,l_marked = None):
        if not l_marked:
            l_marked = [list(self.l[_]) for _ in range(len(self.l))]
            L_marked = [list(self.L[_]) for _ in range(len(self.L))]
        else:
            l_change = [list(self.l[_]) for _ in range(len(self.l))]
            for i in range(9):
                for j in range(9):
                    if len(l_marked[i][j]) ==1:
                        l_change[i][j] = l_marked[i][j][0]
            l_marked = l_change
            L_marked = [[l_change[i][j] for i in range(9)] for j in range(9)]
        l_mark = [[[] for _ in range(9)] for _ in range(9)]
        l1 = [0, 1, 2]
        l2 = [3, 4, 5]
        l3 = [6, 7, 8]
        l_row = [l1, l2, l3]
        l_col = [l1, l2, l3]
        l_1 = [1, 2]
        l_2 = [3, 4]
        l_3 = [5, 6]
        l_4 = [7, 8, 9]
        l_rl = [l_1, l_2, l_3, l_4]
        for i in range(len(l_marked)):
            for j in range(len(l_marked[i])):
                for r in l_row:
                    for l in l_col:
                        if i in r and j in l:
                            l_matrix = [l_marked[i2][j2] for i2 in r for j2 in l]
                if l_marked[i][j] == 0:
                    l_remove = []
                    l_process = list(range(1, 10))
                    for item in l_process:
                        if item in l_marked[i] or item in L_marked[j] or item in l_matrix:
                            l_remove.append(item)
                    for trash in l_remove:
                        l_process.remove(trash)
                    l_mark[i][j] = list(l_process)
                else:
                    l_mark[i][j].append(l_marked[i][j])
        return l_mark

    def marked_tex_output(self):
        l_mark =self._force()
        self._print_tex('marked', l_mark)

    def _print_tex(self,function,l_mark):
        l_1 = [1, 2]
        l_2 = [3, 4]
        l_3 = [5, 6]
        l_4 = [7, 8, 9]
        l_rl = [l_1, l_2, l_3, l_4]
        tex_name_first = sub('\..*', '', self._filename)
        tex_name_first += '_' +function
        if os.path.isfile(tex_name_first + '.tex'):
            for i in count():
                tex_name = tex_name_first + str(i)
                if not os.path.isfile(tex_name + '.tex'):
                    break
        else:
            tex_name = tex_name_first
        with open(tex_name + '.tex', 'w') as tex_file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{positioning}\n'
                  '\\usepackage{cancel}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n'
                  '                               label=above right:{\\tiny #2},\n'
                  '                               label=below left:{\\tiny #3},\n'
                  '                               label=below right:{\\tiny #4}]{#5};}}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\tikzset{every node/.style={minimum size=.5cm}}\n'
                  '\n'
                  '\\begin{center}\n'
                  '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline',
                  file=tex_file
                  )
            for i in range(0,9):
                print(f'% Line {i+1}',file= tex_file)
                for j in range(0,9):
                    l_save = defaultdict(str)
                    if self.l[i][j]:
                        print('\\N{}{}{}{}''{'f'{self.l[i][j]}''}',end='', file=tex_file)
                    elif len(l_mark[i][j]) ==1:
                        print('\\N{}{}{}{}''{'f'{l_mark[i][j][0]}''}', end='', file=tex_file)
                    else:
                        for item in l_mark[i][j]:
                            for r in range(4):
                                    if item in l_rl[r]:
                                        l_save[r] = l_save[r] + str(item)+' '
                        for r in l_save:
                            if l_save[r].endswith(' '):
                                l_save[r] = l_save[r][:-1]
                        print('\\N{' f'{l_save[0]}' '}{' f'{l_save[1]}' '}{' f'{l_save[2]}''}{' f'{l_save[3]}' '}{}', end='', file=tex_file)
                    if j == 8:
                        if i % 3 == 2:
                            print(' \\\\ \hline\\hline', end='', file=tex_file)
                        else:
                            print(' \\\\ \hline', end='', file=tex_file)
                    else:
                        if j%3 == 2:
                            print(' &', end='', file=tex_file)
                        else:
                            print(' & ', end='', file=tex_file)
                    if j % 3 == 2:
                        print('', file=tex_file)
                if i == 8:
                    print('\\end{tabular}\n'
                            '\\end{center}\n'
                            '\n'
                            '\\end{document}', file=tex_file)
                else:
                    print('', file=tex_file)

    def _worked(self):
        l_mark = self._force()
        l_marked =self._force()
        l1 = [0, 1, 2]
        l2 = [3, 4, 5]
        l3 = [6, 7, 8]
        l_row = [l1, l2, l3]
        l_col = [l1, l2, l3]
        while True:
            for i in range(9):
                for j in range(9):
                    if len(l_mark[i][j]) ==1:
                        continue
                    for item in l_mark[i][j]:
                        count =0
                        for other in range(len(l_mark[i])):
                            if other == j:
                                continue
                            if item in l_mark[i][other]:
                                count+=1
                        if count == 0:
                            l_mark[i][j] = [item]
            l_mark=self._mark(l_mark)
            L_mark = [[l_mark[i][j] for i in range(9)] for j in range(9)]
            for i in range(9):
                for j in range(9):
                    if len(L_mark[i][j]) == 1:
                        continue
                    for item in L_mark[i][j]:
                        count = 0
                        for other in range(len(L_mark[i])):
                            if other == j:
                                continue
                            if item in L_mark[i][other]:
                                count += 1
                        if count == 0:
                            t = [item]
                            L_mark[i][j] = t
                            l_mark[j][i] = t
            l_mark = self._mark(l_mark)
            for i in range(0,9,3):
                for j in range(0,9,3):
                    for r in l_row:
                        for l in l_col:
                            if i in r and j in l:
                                l_matrix = [l_mark[i2][j2] for i2 in r for j2 in l]
                                R = list(r)
                                L = list(l)
                    for nb in range(len(l_matrix)):
                        if len(l_matrix[nb]) ==1:
                            continue
                        for e in l_matrix[nb]:
                            count = 0
                            for other in range(len(l_matrix)):
                                if other == nb or len(l_matrix[other]) ==1:
                                    continue
                                if e in l_matrix[other]:
                                    count +=1
                            if count == 0:
                                col =nb%3 +L[0]
                                row = nb//3 + R[0]
                                l_mark[row][col] = [e]
            l_mark = self._mark(l_mark)
            for i in range(9):
                for j in range(len(l_mark[i])):
                    for other in l_mark[i]:
                        count = 0
                        l_save =[]
                        for t in range(9):
                            if set(l_mark[i][t]).issubset(other):
                                l_save.append(l_mark[i][t])
                                count+=1
                        if count == len(other):
                            for trash in other:
                                for item in l_mark[i]:
                                    if item in l_save:
                                        continue
                                    if trash in item:
                                        item.remove(trash)
            L_mark = [[l_mark[i][j] for i in range(9)] for j in range(9)]
            for i in range(9):
                for j in range(len(L_mark[i])):
                    for other in L_mark[i]:
                        count = 0
                        l_save = []
                        for t in range(9):
                            if set(L_mark[i][t]).issubset(other):
                                l_save.append(L_mark[i][t])
                                count += 1
                        if count == len(other):
                            for trash in other:
                                for item in L_mark[i]:
                                    if item in l_save:
                                        continue
                                    if trash in item:
                                        item.remove(trash)
            for i in range(9):
                for j in range(len(l_mark[i])):
                    if len(l_mark[i][j]) == 1:
                        continue
                    for R in l_row:
                        for L in l_col:
                            if i in R and j in L:
                                l_matrix = [l_mark[i2][j2] for i2 in R for j2 in L]
                                R_process = list(R)
                                L_process = list(L)
                    for other in l_matrix:
                        count = 0
                        l_save = []
                        for r in R_process:
                            for l in L_process:
                                if set(l_mark[r][l]).issubset(other):
                                    l_save.append(l_mark[r][l])
                                    count += 1
                        if count == len(other):
                            for trash in other:
                                for item in l_matrix:
                                    if item in l_save:
                                        continue
                                    if trash in item:
                                        item.remove(trash)

            if l_mark == l_marked:
                break
            else:
                l_marked =[[list(l_mark[i][j]) for j in range(9)]for i in range(9)]
        return l_mark

    def worked_tex_output(self):
        l_mark = self._force()
        l_work = self._worked()
        function = 'worked'
        l_1 = [1, 2]
        l_2 = [3, 4]
        l_3 = [5, 6]
        l_4 = [7, 8, 9]
        l_rl = [l_1, l_2, l_3, l_4]
        tex_name_first = sub('\..*', '', self._filename)
        tex_name_first += '_' + function
        if os.path.isfile(tex_name_first + '.tex'):
            for i in count():
                tex_name = tex_name_first + str(i)
                if not os.path.isfile(tex_name + '.tex'):
                    break
        else:
            tex_name = tex_name_first
        with open(tex_name + '.tex', 'w') as tex_file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage[left=0pt,right=0pt]{geometry}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{positioning}\n'
                  '\\usepackage{cancel}\n'
                  '\\pagestyle{empty}\n'
                  '\n'
                  '\\newcommand{\\N}[5]{\\tikz{\\node[label=above left:{\\tiny #1},\n'
                  '                               label=above right:{\\tiny #2},\n'
                  '                               label=below left:{\\tiny #3},\n'
                  '                               label=below right:{\\tiny #4}]{#5};}}\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\tikzset{every node/.style={minimum size=.5cm}}\n'
                  '\n'
                  '\\begin{center}\n'
                  '\\begin{tabular}{||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||@{}c@{}|@{}c@{}|@{}c@{}||}\hline\hline',
                  file=tex_file
                  )
            for i in range(0, 9):
                print(f'% Line {i+1}', file=tex_file)
                for j in range(0, 9):
                    l_save = defaultdict(str)
                    l_saved =defaultdict(list)
                    if self.l[i][j]:
                        print('\\N{}{}{}{}''{'f'{self.l[i][j]}''}', end='', file=tex_file)
                    elif len(l_mark[i][j]) == 1:
                        print('\\N{}{}{}{}''{'f'{l_mark[i][j][0]}''}', end='', file=tex_file)
                    else:
                        for item in l_work[i][j]:
                            for r in range(4):
                                if item in l_rl[r]:
                                    l_saved[r].append(item)
                        for item in l_mark[i][j]:
                            for r in range(4):
                                if item in l_rl[r]:
                                    if item in l_saved[r] and len(l_work[i][j]) >1:
                                        l_save[r] = l_save[r] + str(item) + ' '
                                    else:
                                        l_save[r] = l_save[r] + '\cancel{'+str(item) +'}'+' '
                        for r in l_save:
                            if l_save[r].endswith(' '):
                                l_save[r] = l_save[r][:-1]
                        if len(l_work[i][j]) ==1:
                            print(
                                '\\N{' f'{l_save[0]}' '}{' f'{l_save[1]}' '}{' f'{l_save[2]}''}{' f'{l_save[3]}' '}{'f'{l_work[i][j][0]}''}',
                                end='', file=tex_file)
                        else:
                            print('\\N{' f'{l_save[0]}' '}{' f'{l_save[1]}' '}{' f'{l_save[2]}''}{' f'{l_save[3]}' '}{}',
                              end='', file=tex_file)
                    if j == 8:
                        if i % 3 == 2:
                            print(' \\\\ \hline\\hline', end='', file=tex_file)
                        else:
                            print(' \\\\ \hline', end='', file=tex_file)
                    else:
                        if j % 3 == 2:
                            print(' &', end='', file=tex_file)
                        else:
                            print(' & ', end='', file=tex_file)
                    if j % 3 == 2:
                        print('', file=tex_file)
                if i == 8:
                    print('\\end{tabular}\n'
                          '\\end{center}\n'
                          '\n'
                          '\\end{document}', file=tex_file)
                else:
                    print('', file=tex_file)



