from solving_system import solving_system
from csv2lol import csv2lol
from append2csv import append2csv
from lol2csv import lol2csv
from single_solving_step import single_solving_step

def take_test(test_name,solving_method='gumbel'):
    questions = csv2lol(f'tests/{test_name}.csv')
    answers = [['answers']]
    for i in range(1,len(questions)):
        q = questions[i][0]
        #a = solving_system(q)
        b_train_tmp = False
        b_encapsulate = True
        b_try_first = True
        a = single_solving_step(q,solving_method,b_train_tmp,b_encapsulate,b_try_first)
        answers.append([a])
        append2csv(f'tests/{test_name}-answers.csv',[a])
    #append2csv(f'tests/{test_name}-answers-full.csv',[answers])
    return

if __name__ == '__main__':
    test_name = 'basic-geometry'
    solving_method = 'gumbel'
    take_test(test_name,solving_method)