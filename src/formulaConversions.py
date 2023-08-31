import re

def is_generic_formula(formula):
    # Check if there's a standalone number not followed by an exponent
    if re.search(r'\d+(?![\^\s])', formula):
        return False
    
    # Check for standalone lowercase letters without a preceding coefficient or operation.
    if re.search(r'(?<=[^A-Z\s])[a-z]', formula):
        return False

    return True

def convertFormulaWithNumbers2Coefficients(formula):
    #check if the formula is already in generic format
    if is_generic_formula(formula):
        return formula,{}

    # Match coefficients with variables (and optional exponents), standalone variables, operations, and standalone numbers
    #matches = re.findall(r'([+\-=*/()]|\d*\.\d+|\d+|[a-z]\^\d+|[a-z])', formula)
    matches = re.findall(r'([+\-=*/()]|\d*\.\d+|\d+|[a-z]\^\d+|[a-z])', formula)

    generic_variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    new_formula_parts = []
    coeff_dict = {}
    variable_index = 0

    skip_next = False

    for i, part in enumerate(matches):
        if skip_next:
            skip_next = False
            continue

        if part in ['+', '-', '*', '/', '(', ')', '=']:
            new_formula_parts.append(part)

        # If a standalone number
        elif part.isdigit() or '.' in part:
            if (i+1) < len(matches) and matches[i+1] not in ['+', '-', '*', '/', '(', ')', '=']:
                # Number with a variable, skip the variable in the next iteration
                skip_next = True
                new_formula_parts.append(generic_variables[variable_index] + matches[i+1])
                coeff_dict[generic_variables[variable_index]] = float(part)
                variable_index += 1
            else:
                new_formula_parts.append(generic_variables[variable_index])
                coeff_dict[generic_variables[variable_index]] = float(part)
                variable_index += 1

        # If a variable (with optional exponent)
        else:
            new_formula_parts.append(generic_variables[variable_index] + part[-2:] if '^' in part else part)
            coeff_dict[generic_variables[variable_index]] = 1.0 if part[0].isalpha() else float(part[:-2])
            variable_index += 1

    new_formula = ' '.join(new_formula_parts)
    return new_formula, coeff_dict

'''
def fillFormulaWithCoefficients(formula, coeff_dict):
    for coeff, value in coeff_dict.items():
        formula = formula.replace(coeff, str(value))
    return formula
'''

def fillFormulaWithCoefficients(formula, coeff_dict):
    # Identify coefficients and introduce multiplication signs between them
    formula = re.sub(r'(?<=[A-Za-z])(?=[A-Za-z])', ' * ', formula)
    
    # Replace multi-character coefficients
    for coeff, value in sorted(coeff_dict.items(), key=lambda x: len(x[0]), reverse=True):
        formula = formula.replace(coeff, str(value))
    
    return formula

def simplify_formula(formula):
    try:
        # Extract variable and expression
        var, expression = formula.split('=')
        #evaluate rhs
        try:
            rhs = eval(expression)
        except:
            rhs = expression
        
        #evalute lhs
        try:
            lhs = eval(var)
        except:
            lhs = var
        
        return f'{str(lhs).strip()} = {str(rhs).strip()}'
    except:
        return formula

if __name__ == '__main__':
    #formula = '12x^2 + (3y - y) - (4/5)*z = 5'
    #formula = 'Ax + By - Cz = D'
    #formula = '4(x - 2) = 1'
    #formula = 'Wx - AC = D'
    #new_formula, coeff_dict = convertFormulaWithNumbers2Coefficients(formula)
    new_formula = 'AC = x'
    coeff_dict = {'A':40,'C':2}
    print(f'New1: {new_formula}')
    new_formula = fillFormulaWithCoefficients(new_formula, coeff_dict)
    print(f'New2: {new_formula}')
    new_formula = simplify_formula(new_formula)
    print(new_formula)