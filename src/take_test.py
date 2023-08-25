from solving_system import solving_system
from csv2lol import csv2lol
from append2csv import append2csv
from lol2csv import lol2csv

def take_test(test_name):
    questions = csv2lol(f'tests/{test_name}.csv')
    answers = [['answers']]
    for i in range(1,len(questions)):
        q = questions[i][0]
        a = solving_system(q)
        answers.append([a])
        append2csv(f'tests/{test_name}-answers.csv',[a])
    append2csv(f'tests/{test_name}-answers-full.csv',[answers])
    return

if __name__ == '__main__':
    test_name = 'basic_algebra'
    take_test(test_name)