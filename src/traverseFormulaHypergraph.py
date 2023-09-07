from formulaStrings2JSON import formulaStrings2JSON
from formulas2Hypergraph import formulas2Hypergraph

def get_edges(fhg,voi):
    #get eqs containg variable of interest
    edges = []
    for k,v in fhg.items():
        if voi in v:
            edges.append(k)
    return edges

def traverseFormulaHypergraph(formula_strings,var):
    formulas = formulaStrings2JSON(formula_strings)
    print(formulas)
    fhg = formulas2Hypergraph(formulas)
    print(fhg)
    print('---')
    vars_solvable = {}
    def traverse(vars_solvable):
        vars_looked_at = []
        edges_looked_at = []
        stack = [var]
        i = 0
        while len(stack) > 0:
            i += 1
            voi = stack.pop()
            #print(f'VOI: {voi}')
            vars_looked_at.append(voi)
            edges = get_edges(fhg,voi)
            for edge in edges:
                #print(edge)
                neighbors = fhg[edge]
                if len(neighbors) == 1:
                    vars_solvable[neighbors[0]] = edge
                    #print('vars solvable')
                elif len([i for i in neighbors if i not in vars_solvable]) ==1:
                    vars_solvable[[i for i in neighbors if i not in vars_solvable][0]] = edge
                else:
                    for neighbor in neighbors:
                        if neighbor not in vars_solvable and neighbor not in stack and edge not in edges_looked_at and neighbor != voi:
                            stack.append(neighbor)
                edges_looked_at.append(edge)
            #print(stack)
            #print(vars_looked_at)
            #print(vars_solvable)
        return vars_solvable

    j = 0
    while var not in vars_solvable and j < 100:
        j += 1
        old_len = len(vars_solvable)
        vars_solvable = traverse(vars_solvable)
        print(vars_solvable)
        if old_len == len(vars_solvable):
            break

    solve_statements = []
    if var in vars_solvable:
        #make list of solve_statements
        for v,eq in vars_solvable.items():
            ss = f'Solve for {v}: {formulas[eq]} -->'
            solve_statements.append(ss)
            if v == var:
                break
        #print(solve_statements)
    return solve_statements

if __name__ == '__main__':
    var = 'x'
    #formula_strings = 'x = y + z + A + q;A=1;B=2;C=3;y=B + C;z=w;g=h;w=C+A;z=h;x=r;q=1'
    #formula_strings = 'A + x = B;B=10'
    formula_strings = 'x + y = 5;y+x=6;y=1'
    solve_statements = traverseFormulaHypergraph(formula_strings,var)
    print(solve_statements)