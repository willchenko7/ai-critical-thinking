

def check_if_var_solved(answer,var):
    var = var.strip()
    answer = answer.strip()
    answer = answer.replace(' ','')
    if answer.startswith(f'{var}=') or answer.endswith(f'={var}'):
        return True
    else:
        return False


if __name__ == '__main__':
    var = 'x'
    #good example
    answer = 'x = (C - B)/A'
    var_solved = check_if_var_solved(answer,var)
    print(var_solved)

    #bad example
    answer = 'x + A = B + C'
    var_solved = check_if_var_solved(answer,var)
    print(var_solved)