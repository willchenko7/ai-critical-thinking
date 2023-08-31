'''
Goal: given an equation, break it down into a simpler, yet equivalent eqn
'''
import re


def encapsulate_eq(problem):
    eq_dict = {}
    #split problem into words, math_problem and var
    words,math_problem = re.split(':',problem)
    math_problem = math_problem.replace('-->','')
    math_problem = math_problem.strip()
    var = words[-1]
    new_var = var
    all_vars = [char for char in math_problem if char.islower()]

    #can the entire lhs or rhs be encapsulated
    lhs,rhs = re.split('=',math_problem)
    lhs = lhs.strip()
    rhs = rhs.strip()
    if var not in lhs and ('+' in lhs or '-' in lhs):
        all_coeffs = [char for char in math_problem if char.isupper()]
        all_coeffs = all_coeffs  + list(eq_dict.keys())
        new_coeff  = get_next_coeff(all_coeffs)
        eq_dict[new_coeff] = lhs
    if var not in rhs and ('+' in rhs or '-' in rhs or '/' in rhs or '*' in rhs):
        all_coeffs = [char for char in math_problem if char.isupper()]
        all_coeffs = all_coeffs  + list(eq_dict.keys())
        new_coeff  = get_next_coeff(all_coeffs)
        eq_dict[new_coeff] = rhs

    #can any parantheses be encapsulated
    pars = get_pars(math_problem)
    for par in pars:
        if par != lhs and par != rhs:
            if var in par:
                #print(all_vars)
                all_vars = all_vars + list(eq_dict.keys())
                #print(all_vars)
                new_var = get_next_var(all_vars)
                eq_dict[new_var] = par
            else:
                all_coeffs = [char for char in math_problem if char.isupper()]
                all_coeffs = all_coeffs  + list(eq_dict.keys())
                new_coeff  = get_next_coeff(all_coeffs)
                eq_dict[new_coeff] = par
    
    if eq_dict != {}:
        new_words = words[:-1] + new_var + ': '
        new_eq = math_problem
        for k,v in eq_dict.items():
            new_eq = new_eq.replace(v,k)

        new_problem = new_words + new_eq + ' -->'
    else:
        new_problem = problem
    return new_problem,eq_dict
        

def get_pars(math_problem):
    open_pars = []
    closed_pars = []
    #check for parathenses that can be encapsulated
    if '(' in math_problem and ')' in math_problem:
        for i in range(0,len(math_problem)):
            if math_problem[i] == '(':
                open_pars.append(i)
            elif math_problem[i] == ')':
                closed_pars.append(i)
    pars = []
    for i in range(0,len(open_pars)):
        pars.append(math_problem[open_pars[i]:closed_pars[i]+1])
    return pars

def get_next_var(all_vars):
    ords = [ord(i) for i in all_vars]
    max_ord = max(ords)
    min_ord = min(ords)
    for i in range(122,96,-1):
        if i not in ords:
                return chr(i)
    return None

def get_next_coeff(all_coeffs):
    ords = [ord(i) for i in all_coeffs]
    for i in range(65,91):
        if i not in ords:
            return chr(i)
    return None



if __name__ == '__main__':
    ex1 = 'Solve for w: A(Bw - C) = D -->' #new_eq = 'Solve for x: Ax = D';eq_dict = {'x':'(Bw - C)'}
    new_problem,eq_dict = encapsulate_eq(ex1)
    print(f'Ex1: {eq_dict}')
    print(f'Ex1: {new_problem}')
    
    ex2 = 'Solve for w: w(Aw + B) = D -->' #new_eq = None; eq_dict=None
    new_problem,eq_dict = encapsulate_eq(ex2)
    print(f'Ex2: {eq_dict}')
    print(f'Ex2: {new_problem}')
    
    ex3 = 'Solve for x: A(x) = B -->' #new_eq = None; eq_dict=None
    new_problem,eq_dict = encapsulate_eq(ex3)
    print(f'Ex3: {eq_dict}')
    print(f'Ex3: {new_problem}')

    ex4 = 'Solve for x: Ax + C = B -->' #new_eq = None; eq_dict=None
    new_problem,eq_dict = encapsulate_eq(ex4)
    print(f'Ex4: {eq_dict}')
    print(f'Ex4: {new_problem}')

    ex5 = 'Solve for y: A(By+C) + D(E +Fy) = G' #new_eq = None; eq_dict=None
    new_problem,eq_dict = encapsulate_eq(ex5)
    print(f'Ex5: {eq_dict}')
    print(f'Ex5: {new_problem}')

    ex6 = 'Solve for w: ABw = D + AC -->' #new_eq = 'Solve for ABw = F -->' ; eq_dict = {'E':'AB','F':'D + AC'}
    new_problem,eq_dict = encapsulate_eq(ex6)
    print(f'Ex6: {eq_dict}')
    print(f'Ex6: {new_problem}')
    
    ex7 = 'Solve for w: ( Bw - C ) = D/A -->'
    new_problem,eq_dict = encapsulate_eq(ex7)
    print(f'Ex7: {eq_dict}')
    print(f'Ex7: {new_problem}')