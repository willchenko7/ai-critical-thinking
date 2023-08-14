from sympy import *
import re
from string_to_sympy_eq import string_to_sympy_eq,are_equations_equivalent
'''
x, y, z = symbols('x y z')
eq1 = Eq(x + y, z)
eq2 = Eq(y, z - x)
eq3 = Eq(x, z - y)
print(simplify(eq1) == simplify(eq2))
'''

def equation_checker(sentence):
    '''
    example sentce: "Add A to both sides: x + A = B --> x = B - A"
    equations: "x + A = B" and "x = B - A"
    eq1 = Eq(x + A, B)
    eq2 = Eq(x, B - A)
    '''
    #conver ^ to **
    sentence = sentence.replace('^','**')
    #print(sentence)
    #parse sentence into separate equations
    l_sympy_eq = []
    l_all_symbols = []
    parts = re.split(r' --> ',sentence)
    for part in parts:
        if ':' in part:
            i_eq = re.split(r': ',part)[1]
        else:
            i_eq = part
        #print(i_eq)
        #convert equation to sympy equation
        i_sympy_eq,i_all_symbols = string_to_sympy_eq(i_eq)
        s = ''.join(list(i_all_symbols.keys()))
        distinct_symbols = ''.join(sorted(set(s), key=s.index))
        #print(distinct_symbols)
        l_sympy_eq.append(i_sympy_eq)
        l_all_symbols.append(distinct_symbols)
    if 'w' in str(l_sympy_eq[1]):
        temp = 10
    else:
        temp = 1
    #check if all equations are equivalent
    #gets a score, 0 if equivalent, 1 if not (lower is better), 1 if symbols do not match
    score = 0
    for i in range(len(l_sympy_eq)-1):
        check_eq, diff,diff_terms = are_equations_equivalent(l_sympy_eq[i],l_sympy_eq[i+1])
        if diff_terms >= 1:
          diff_terms = diff_terms * 20
        else:
          diff_terms = 0.5
        #print(f'Diff terms: {diff_terms}')
        multiplier = len(str(diff))
        if check_eq == False:
            score += 1
        set1 = set(l_all_symbols[i])
        set2 = set(l_all_symbols[i+1])
        #if len(set1.symmetric_difference(set2)) > 0:
            #score += len(set1.symmetric_difference(set2))
    return ((score * multiplier)*diff_terms)/10/temp, l_sympy_eq

if __name__ == '__main__':
    #test with example sentence
    sentence = "Expand A: A(x + w) = E --> Ax + Az = E"
    score,l_sympy_eq = equation_checker(sentence)
    print(l_sympy_eq)
    print(score)