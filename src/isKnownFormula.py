import re

def isKnownFormula(problem,formulas,var):
    if var in formulas:
        return formulas[var]

    eq = re.split(': ',problem)[-1].replace('-->','').strip()
    #print(eq)
    vs = re.split(';',eq)
    for i in vs:
        k,v = re.split('=',i)
        if k.strip() in formulas:
            return formulas[k.strip()]
        if v.strip() in formulas:
            return formulas[v.strip()]
    return None


if __name__ == '__main__':
    formulas = {'perimeter':'p = 2w + 2l'}
    
    #problem = 'Solve for perimeter: w=2;l=10 -->'
    problem="Solve for w: perimter=20;l=5"
    var = 'perimeter'
    #expected: p = 2w + 2l
    print(isKnownFormula(problem,formulas,var))

    problem = 'Solve for w: w + A = B -->'
    var = 'w'
    #expected = None
    print(isKnownFormula(problem,formulas,var))


    problem = 'Solve for w: perimeter=20;l=5 -->'
    var = 'w'
    #expected: p = 2w + 2l
    print(isKnownFormula(problem,formulas,var))
