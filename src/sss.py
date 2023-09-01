import torch
from generate import generate
from customTokenizer import loadCustomTokenizer
from train_on_new_problem import train_on_new_problem
import torch.nn as nn
import re
from formulaConversions import convertFormulaWithNumbers2Coefficients,fillFormulaWithCoefficients,simplify_formula
from check_if_var_solved import check_if_var_solved
from equation_checker import equation_checker
from ea import ea
from train_tmp_model import train_tmp_model
from encapsulate_eq import encapsulate_eq
from load_formulas import load_formulas
from convert2KnownProblem import convert2KnownProblem
from isKnownFormula import isKnownFormula
from append2csv import append2csv

#synthetic solving system (sss)
def sss(problem,solving_method='gumbel',b_train_tmp=False,b_encapsulate=False,b_try_first=True):
    
    #load formulas
    formulas = load_formulas()
    
    problem = problem.replace('−', '-')
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    #load model
    model = torch.load('models/sss-final.pth',map_location =device)
    #convert problem into generic problem
    problem_parts = re.split(': ',problem.replace('-->',''))
    words = problem_parts[0]
    var = re.split(' ',words)[-1]
    eq = problem_parts[1]
    known_coeff_dict = {}
    print(problem)
    print(formulas)
    print(var)
    knownFormula = isKnownFormula(problem,formulas,var)
    #print(f'Is known? {knownFormula}')
    if knownFormula is not None:
        #convert to knownPorblem
        print('---')
        print(eq)
        print(var)
        print(knownFormula)
        problem, known_coeff_dict, new_var = convert2KnownProblem(eq,var,knownFormula)
        print(problem)
        problem_parts = re.split(': ',problem.replace('-->',''))
        words = problem_parts[0]
        #var = re.split(' ',words)[-1]
        var = new_var
        eq = problem_parts[1]
    new_formula, coeff_dict = convertFormulaWithNumbers2Coefficients(eq)
    problem = words + ': ' + new_formula + ' -->'
    coeff_dict.update(known_coeff_dict)

    print(problem)
    print(coeff_dict)
    return

    answer = new_formula
    var_solved = check_if_var_solved(answer,var)
    print(var_solved)
    if var_solved == True:
        answer = fillFormulaWithCoefficients(answer, coeff_dict)
        print(answer)
        answer = simplify_formula(answer)
        return answer
    
    var_solved = False
    i = 0
    while i < 10:
        i += 1
        b_encapsulated = False
        #generate response to problem
        #define criterion and optimizer
        criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
        optimizer = torch.optim.Adam(model.parameters())
        if b_try_first == True:
            if solving_method == 'gumbel':
                _,response,_ = train_on_new_problem(model,criterion,optimizer,epochs=1000,model_name='test-new-problem',problem=problem,in_temperature=1.5,tokenizer=tokenizer,device=device)
            elif solving_method == 'ea':
                best_network,response = ea(problem)

            response = response.replace('- - >','-->')
            response = response.replace('[CLS]','')
            response = response.replace('[SEP]','')
            print(response)
            answer = re.split(' --> ',response)[-1]
            #check validity of answer
            score, l_sympy_eq = equation_checker(response)
            print(f'Score: {score}')
        else:
            score = 1.0
        if score != 0.0:
            if b_train_tmp == True:
                #add exact answer to tmp data set, retrain model
                model = train_tmp_model(model,problem)

                if solving_method == 'gumbel':
                    _,response,_ = train_on_new_problem(model,criterion,optimizer,epochs=1000,model_name='test-new-problem',problem=problem,in_temperature=1.5,tokenizer=tokenizer,device=device)
                elif solving_method == 'ea':
                    best_network,response = ea(problem)

                response = response.replace('- - >','-->')
                response = response.replace('[CLS]','')
                response = response.replace('[SEP]','')
                print(response)
                answer = re.split(' --> ',response)[-1]
                #check validity of answer
                score, l_sympy_eq = equation_checker(response)
                print(f'Score: {score}')
                if score != 0.0:
                    #couldn't figure it out. just exit
                    return answer
            elif b_encapsulate == True:
                b_encapsulated = True
                print(f'Original Problem: {problem}')
                new_problem,eq_dict = encapsulate_eq(problem)
                print(f'Encapsualted problem {new_problem}')
                if solving_method == 'gumbel':
                    _,response,_ = train_on_new_problem(model,criterion,optimizer,epochs=1000,model_name='test-new-problem',problem=new_problem,in_temperature=1.5,tokenizer=tokenizer,device=device)
                elif solving_method == 'ea':
                    best_network,response = ea(new_problem)

                response = response.replace('- - >','-->')
                response = response.replace('[CLS]','')
                response = response.replace('[SEP]','')
                print(response)
                answer = re.split(' --> ',response)[-1]
                #check validity of answer
                score, l_sympy_eq = equation_checker(response)
                print(f'Score: {score}')
                for k,v in eq_dict.items():
                    v = v.strip()
                    if v[0] != '(' or v[-1] != ')':
                        answer = answer.replace(k,'(' + v + ')')
                    else:
                        answer = answer.replace(k,v)
                print(f'Unencapsulated answer: {answer}')
                if score != 0.0:
                    #couldn't figure it out. just exit
                    #write down problem it couldn't figure out
                    if b_encapsulated == True:
                        append2csv('data/not_solved_steps.csv',[new_problem])
                    else:
                        append2csv('data/not_solved_steps.csv',[problem])
                    return answer
            else:
                return answer

        
        #check if var is solved for
        #print(answer)
        #print(var)
        var_solved = check_if_var_solved(answer,var)
        #print(var_solved)
        if var_solved == True:
            break
        problem = words + ': ' + answer + ' -->'
    answer = fillFormulaWithCoefficients(answer, coeff_dict)
    answer = simplify_formula(answer)
    return answer

if __name__ == '__main__':
    #problem = 'Solve for w: ABw = D + AC -->'
    #problem = 'Solve for x: 3x + 2 = 5 -->'
    #problem = 'Solve for perimeter_of_square: s=10 -->'
    problem = 'Solve for circumference_of_circle: diameter=10 -->'
    solving_method = 'gumbel'
    b_train_tmp = False
    b_encapsulate = True
    b_try_first = False
    answer = sss(problem,solving_method,b_train_tmp,b_encapsulate,b_try_first)
    print('FINAL ANSWER')
    print(answer)
    print('----')