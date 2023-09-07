'''
Convert dictionary of various formulas to a hypergraph

formulas: y = B + C;z=2A; z= E + F, y = F + g,E=A

formula_map ={
    'r0':[x,y,z,A]
    'r1':[y,B,C],
    'r2':[z1,A],
    'r3':[z,E],
    'r4':[y,F,g],
    'r5':[E,A],
    'r6':[z,g]
}
'''
from formulaStrings2JSON import formulaStrings2JSON

def formulas2Hypergraph(formulas):
    fhg = {}
    for eq_name,formula in formulas.items():
        unique_chars = sorted(list(set([char for char in formula if char.isalpha()])))
        fhg[eq_name] = unique_chars
    return fhg


if __name__ == '__main__':
    formula_strings = 'y = B + C;z=2A; z= E + F; y = F + g;E=A'
    formulas = formulaStrings2JSON(formula_strings)
    print(formulas)
    fhg = formulas2Hypergraph(formulas)
    print(fhg)
