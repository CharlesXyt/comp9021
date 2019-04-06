# Uses data available at http://data.worldbank.org/indicator
# on Forest area (sq. km) and Agricultural land area (sq. km).
# Prompts the user for two distinct years between 1990 and 2004
# as well as for a strictly positive integer N,
# and outputs the top N countries where:
# - agricultural land area has increased from oldest input year to most recent input year;
# - forest area has increased from oldest input year to most recent input year;
# - the ratio of increase in agricultural land area to increase in forest area determines
#   output order.
# Countries are output from those whose ratio is largest to those whose ratio is smallest.
# In the unlikely case where many countries share the same ratio, countries are output in
# lexicographic order.
# In case fewer than N countries are found, only that number of countries is output.


# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv
from collections import defaultdict

agricultural_land_filename = 'API_AG.LND.AGRI.K2_DS2_en_csv_v2.csv'
forest_filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2.csv'

if not os.path.exists(agricultural_land_filename):
    print(f'No file named {agricultural_land_filename} in working directory, giving up...')
    sys.exit()
forest_filename = 'API_AG.LND.FRST.K2_DS2_en_csv_v2.csv'
if not os.path.exists(forest_filename):
    print(f'No file named {forest_filename} in working directory, giving up...')
    sys.exit()
try:
    years = {int(year) for year in
             input('Input two distinct years in the range 1990 -- 2014: ').split('--')
             }
    if len(years) != 2 or any(year < 1990 or year > 2014 for year in years):
        raise ValueError
except ValueError:
    print('Not a valid range of years, giving up...')
    sys.exit()
try:
    top_n = int(input('Input a strictly positive integer: '))
    if top_n < 0:
        raise ValueError
except ValueError:
    print('Not a valid number, giving up...')
    sys.exit()

countries = []
year_1, year_2 =years

line_num1 = 0
agri_file = defaultdict(list)

y1 = year_1 - 1990
y2 = year_2 - 1990
fore = []
agri = []
final = []
if y1 > y2:
    t = y2
    y2 = y1
    y1 = t

with open(agricultural_land_filename,'r',encoding = 'utf-8') as f1:
    while True:
        if line_num1 < 4:
            f1.readline()
            line_num1 += 1
        else:
            lines =csv.DictReader(f1)
            for line in lines:
                t = line['Country Name']
                for i in range(1990 + y1, 1990 + y2 + 1):
                    if line[f'{i}'] == '':
                        break
                    if i == 1990 + y2:
                        for j in range(1990 + y1, 1990 + y2 +1):
                            agri_file[t].append(line[f'{j}'])
            break
line_num1 = 0
fore_file = defaultdict(list)
with open(forest_filename, 'r', encoding='utf-8') as f2:
    while True:
        if line_num1 < 4:
            f2.readline()
            line_num1 += 1
        else:
            lines = csv.DictReader(f2)
            for line in lines:
                t = line['Country Name']
                for i in range(1990 + y1,1990 + y2 + 1):
                    if line[f'{i}'] == '':
                        break
                    if i == 1990 + y2:
                        for j in range(1990 + y1,1990 + y2 + 1):
                            fore_file[t].append(line[f'{j}'])
            break


for fore_item in fore_file:
    if fore_item not in agri_file:
        continue
    fore.append([fore_item,float(fore_file[fore_item][-1]) - float(fore_file[fore_item][0])])
for agri_item in agri_file:
    if agri_item not in fore_file:
        continue
    agri.append([agri_item,float(agri_file[agri_item][-1]) - float(agri_file[agri_item][0])])
print(fore)
print(agri)

for i in range(len(fore)):
    if fore[i][1] == 0:
        continue
    if agri[i][1] == 0:
        continue
    if agri[i][1] < 0  or fore[i][1] < 0:
        continue
    final.append([agri[i][0],agri[i][1] / fore[i][1]])
final.sort(key = lambda x:( - x[1] , x[0]))

print(final)
if top_n > len(final):
    top_n = len(final)

print(f'Here are the top {top_n} countries or categories where, between {y1 + 1990} and {y2 + 1990},\n'
      '  agricultural land and forest land areas have both strictly increased,\n'
      '  listed from the countries where the ratio of agricultural land area increase\n'
      '  to forest area increase is largest, to those where that ratio is smallest:')

for i in range(top_n):
    print(f'{final[i][0]} ({final[i][1]:0.2f})')
