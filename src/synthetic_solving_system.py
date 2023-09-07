from single_solving_step import single_solving_step
from traverseFormulaHypergraph import traverseFormulaHypergraph
from formulaConversions import convertFormulaWithNumbers2Coefficients,fillFormulaWithCoefficients,simplify_formula
import re


def synthetic_solving_system(problem):
    solving_method = 'gumbel'
    b_train_tmp = False
    b_encapsulate = True
    b_try_first = True

    words,formula_strings = re.split(':',problem)
    var = re.split(' ',words)[-1]

    solve_statements = traverseFormulaHypergraph(formula_strings,var)
    if solve_statements == []:
        solve_statements = [problem]
    print(solve_statements)
    coeff_dict = {}
    for q in solve_statements:
        voi = re.split(' ',re.split(':',q)[0])[-1]
        a = single_solving_step(q,solving_method,b_train_tmp,b_encapsulate,b_try_first)
        if '=' in a and voi != var:
            v1,v2 = re.split('=',a)
            if v1.strip() == voi:
                coeff_dict[voi] = v2.strip()
            elif v2.strip() == voi:
                coeff_dict[voi] = v1.strip()
    
    print(coeff_dict)
    i = 0
    while i < 100:
        i+=1
        old_a = a
        a = fillFormulaWithCoefficients(a, coeff_dict)
        if a == old_a:
            break
    a = simplify_formula(a)
    return a

if __name__ == '__main__':
    #problem = 'Solve for x: A + x = B -->'
    #problem = 'Solve for perimeter_of_square: s=10 -->'
    #problem = 'Solve for x: x = y + z + A + q;A=1;B=2;C=3;y=B + C;z=w;g=h;w=C+A;z=h;x=r;q=1 -->' #answer: x = 11
    problem = 'Solve for x: x + y = 5;y+x=6'
    a = synthetic_solving_system(problem)
    print('----')
    print(f'Final answer: {a}')