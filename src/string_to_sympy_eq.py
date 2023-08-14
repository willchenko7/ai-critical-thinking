from sympy import symbols, Eq, parse_expr,simplify,solve, sqrt, expand, collect
import re

def insert_multiplication_signs(equation_str):
    # Handle cases like "2x" or "Ax"
    equation_str = re.sub(r'(?<=[0-9A-Za-z\)])\s*(?=[a-zA-Z\(])', '*', equation_str)

    # Avoid inserting multiplication sign in exponentiation cases like "A**x"
    equation_str = re.sub(r'\*\*\*', '**', equation_str)

    return equation_str


def string_to_sympy_eq(equation_str):
    # Split the string equation into its LHS and RHS
    lhs_str, rhs_str = equation_str.split('=')
    # Insert multiplication signs
    lhs_str = insert_multiplication_signs(lhs_str.strip())
    rhs_str = insert_multiplication_signs(rhs_str.strip())
    # Extract coefficient names using a regular expression
    #coeff_names = set(re.findall(r'\b[A-Z]+\b', equation_str))
    #coeff_names = set(re.findall(r'\b[A-Za-z][A-Za-z0-9]*\b', equation_str))
    lhs_coeff_names = set(re.findall(r'\b[A-Za-z][A-Za-z0-9]*\b', lhs_str))
    rhs_coeff_names = set(re.findall(r'\b[A-Za-z][A-Za-z0-9]*\b', rhs_str))
    coeff_names = lhs_coeff_names.union(rhs_coeff_names)
    #print(coeff_names)
    # Extract variable names (sequences of lowercase alphabets)
    var_names = set(re.findall(r'\b[a-z]+\b', equation_str))
    # Dynamically create the symbols
    all_symbols = {name: symbols(name) for name in coeff_names.union(var_names)}
    # Use SymPy's parse_expr to convert string to SymPy expression
    #print(lhs_str)
    #print(all_symbols)
    lhs_expr = parse_expr(lhs_str, all_symbols)
    #print(lhs_expr)
    rhs_expr = parse_expr(rhs_str, all_symbols)
    # Return the SymPy equation
    return Eq(lhs_expr, rhs_expr), all_symbols


def are_equations_equivalent(eq1, eq2):
    # Simplify the LHS and RHS of both equations first
    eq1_lhs_simplified = simplify(eq1.lhs)
    eq1_rhs_simplified = simplify(eq1.rhs)
    eq2_lhs_simplified = simplify(eq2.lhs)
    eq2_rhs_simplified = simplify(eq2.rhs)


    #print(str(eq1.lhs - eq1.rhs))
    #print(str(eq2.lhs - eq2.rhs))

    num_terms_1 = len([i for i in str(eq1.lhs - eq1.rhs) if i in ['-','+']])
    #print(num_terms_1)
    num_terms_2 = len([i for i in str(eq2.lhs - eq2.rhs) if i in ['-','+']])
    #print(num_terms_2)
    diff_terms = abs(abs(num_terms_2) - abs(num_terms_1))
    #print(diff_terms)
    diff = simplify((eq1_lhs_simplified - eq1_rhs_simplified) - (eq2_lhs_simplified - eq2_rhs_simplified))
    #print(diff)

    # Compare the simplified LHS and RHS
    if eq1_lhs_simplified == eq2_lhs_simplified and eq1_rhs_simplified == eq2_rhs_simplified:
        return True, diff,diff_terms

    #check str equality
    if str(eq1_lhs_simplified) == str(eq2_lhs_simplified) and str(eq1_rhs_simplified) == str(eq2_rhs_simplified):
        return True, diff,diff_terms

    # Check direct difference equivalence
    if simplify(eq1.lhs - eq2.lhs) == simplify(eq1.rhs - eq2.rhs):
        return True, diff,diff_terms

    # Check ratio equivalence
    if eq1.rhs != 0 and eq2.rhs != 0:  # Ensure we don't divide by zero
        if simplify(eq1.lhs / eq1.rhs) == simplify(eq2.lhs / eq2.rhs):
            return True, diff,diff_terms

    # Check for solutions equivalence
    common_vars = list(set(eq1.free_symbols) & set(eq2.free_symbols))

    # If one of the equations has a single term on the left or right (indicating it's probably the variable we're solving for)
    if len(eq1.lhs.free_symbols) == 1 or len(eq1.rhs.free_symbols) == 1:
        variable = list(eq1.lhs.free_symbols)[0] if len(eq1.lhs.free_symbols) == 1 else list(eq1.rhs.free_symbols)[0]
        sol_eq1 = solve(eq1, variable)
        sol_eq2 = solve(eq2, variable)

        for sol in sol_eq1:
            if any(simplify(sol - other_sol) == 0 for other_sol in sol_eq2):
                return True, diff,diff_terms

    return False, diff,diff_terms

if __name__ == '__main__':
    # Test
    #str_equation1 = "AA*x + BB*y = CB*y"
    #str_equation2 = "AAx = (CB - BB)y"
    #str_equation1 = "Ax = B"
    #str_equation2 = "x = B/A"
    #str_equation1 = "x**2 - B = A"
    #str_equation2 = "x = (A+B)**(1/2)"
    str_equation1 = "Ny^2 = O + y^3"
    str_equation2 = "Ny^2 - y^3 = O"
    sympy_eq1,all_symbols = string_to_sympy_eq(str_equation1)
    print(sympy_eq1)
    sympy_eq2,all_symbols = string_to_sympy_eq(str_equation2)
    print(sympy_eq2)
    print(are_equations_equivalent(sympy_eq1, sympy_eq2))