from lol2csv import lol2csv
from csv2lol import csv2lol
import re

def removeWords(in_file,out_file):
    data = csv2lol(f'data/{in_file}.csv')
    new_data = []
    for i in data:
        if ':' in i[0]:
            nr = re.split(':',i[0])[1]
        else:
            nr = i[0]
        new_data.append([nr.strip()])
    lol2csv(f'data/{out_file}.csv',new_data)
    return

if __name__ == '__main__':
    in_file = 'train-very-basic-combine'
    out_file = 'just-math'
    removeWords(in_file,out_file)