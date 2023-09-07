import re

def formulaStrings2JSON(formula_strings):
    formula_strings = re.split(';',formula_strings)
    fj = {}
    i = 0
    for fs in formula_strings:
        k = f'eq{i}'
        fj[k] = fs
        i += 1
    return fj

if __name__ == '__main__':
    formula_strings = 'y = B + C;z=2A; z= E + F; y = F + g;E=A'
    fj = formulaStrings2JSON(formula_strings)
    print(fj)