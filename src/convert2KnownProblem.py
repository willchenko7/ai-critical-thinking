import re
from terms_dict import terms_dict
from load_formulas import load_formulas


def convert2KnownProblem(eq,var,knownFormula):
    formulas = load_formulas()
    additionalFormulas = []
    coeff_dict = {}
    vs = re.split(';',eq)
    for i in vs:
        k,v = re.split('=',i)
        key = k.strip()

        if key in formulas:
            additionalFormulas.append(formulas[key])

        if key in terms_dict:
            key = terms_dict[key]
        coeff_dict[key] = v.strip()
    
    if var in terms_dict:
        new_var = terms_dict[var]
    else:
        new_var = var
    
    #new_var = re.split('=',knownFormula)[0].strip()
    words = 'Solve for ' + new_var + ': '
    knownProblem = words + knownFormula

    if len(additionalFormulas) !=0:
        knownProblem = knownProblem + ';' + ';'.join(additionalFormulas)
    return knownProblem, coeff_dict, new_var

if __name__ == '__main__':
    eq = 'w=10;l=20'
    var = 'perimeter'
    knownFormula = 'p = 2w + 2l'
    knownProblem,coeff_dict,new_var = convert2KnownProblem(eq,var,knownFormula)
    #expected output: knownProblem = 'Solve for p: p = 2w + 2l' ; coeff_dict = {'w':10,'l':20}
    print('----')
    print(knownProblem)
    print(coeff_dict)


    eq = 'perimeter=20;l=5'
    var = 'w'
    knownFormula  = 'p = 2w + 2l'
    knownProblem,coeff_dict,new_var = convert2KnownProblem(eq,var,knownFormula)
    #expected output: knownProblem = 'Solve for w: p = 2w + 2l' ; 
    #coeff_dict = {'p':20,'l':5}
    print('----')
    print(knownProblem)
    print(coeff_dict)

    eq = 's=5'
    var='area_of_square'
    knownFormula = 'a= s^2'
    knownProblem,coeff_dict,new_var = convert2KnownProblem(eq,var,knownFormula)
    #expected output: knownProblem = 'Solve for a: a=s^2'; 
    #coeff_dict = {'s':5}
    print('----')
    print(knownProblem)
    print(coeff_dict)