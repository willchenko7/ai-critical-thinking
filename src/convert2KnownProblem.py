import re
from terms_dict import terms_dict

def convert2KnownProblem(eq,var,knownFormula):
    coeff_dict = {}
    vs = re.split(';',eq)
    for i in vs:
        k,v = re.split('=',i)
        key = k.strip()
        if key in terms_dict:
            key = terms_dict[key]
        coeff_dict[key] = v.strip()
    if var in terms_dict:
        new_var = terms_dict[var]
    else:
        new_var = var
    words = 'Solve for ' + new_var + ': '
    knownProblem = words + knownFormula
    return knownProblem, coeff_dict

if __name__ == '__main__':
    eq = 'w=10;l=20'
    var = 'perimeter'
    knownFormula = 'p = 2w + 2l'
    knownProblem,coeff_dict = convert2KnownProblem(eq,var,knownFormula)
    #expected output: knownProblem = 'Solve for p: p = 2w + 2l' ; coeff_dict = {'w':10,'l':20}
    print('----')
    print(knownProblem)
    print(coeff_dict)


    eq = 'perimeter=20;l=5'
    var = 'w'
    knownFormula  = 'p = 2w + 2l'
    knownProblem,coeff_dict = convert2KnownProblem(eq,var,knownFormula)
    #expected output: knownProblem = 'Solve for w: p = 2w + 2l' ; 
    #coeff_dict = {'p':20,'l':5}
    print('----')
    print(knownProblem)
    print(coeff_dict)
