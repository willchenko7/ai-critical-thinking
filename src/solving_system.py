import torch
from generate import generate
from customTokenizer import loadCustomTokenizer
from train_on_new_problem import train_on_new_problem
import torch.nn as nn
import re
from formulaConversions import convertFormulaWithNumbers2Coefficients,fillFormulaWithCoefficients,simplify_formula

def solving_system(problem):
    problem = problem.replace('−', '-')
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    #load words model
    words_model = torch.load('models/basic-words-final.pth',map_location =device)
    #load math model
    math_model = torch.load('models/basic-math-final.pth',map_location =device)
    #convert problem into generic problem
    problem_parts = re.split(': ',problem.replace('-->',''))
    new_formula, coeff_dict = convertFormulaWithNumbers2Coefficients(problem_parts[1])
    problem = problem_parts[0] + ': ' + new_formula + ' -->'
    #generate response to problem
    response = generate(problem,words_model,tokenizer,device)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')
    print(response)
    #split the response into steps
    steps = re.split(' --> ',response)
    eq = re.split(': ',steps[0])[1]
    print(eq)
    print(coeff_dict)
    #for each step, generate a response
    #return
    for i in range(1,len(steps)):
        step = steps[i]
        print(step)
        prompt = step + ': ' + eq + ' -->'
        print(prompt)
        #define criterion and optimizer
        criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
        optimizer = torch.optim.Adam(math_model.parameters())
        _,response,_ = train_on_new_problem(math_model,criterion,optimizer,epochs=1000,model_name='test-new-problem',problem=prompt,in_temperature=1.5,tokenizer=tokenizer,device=device)
        print(response)
        eq = re.split(' --> ',response)[1]
    eq = fillFormulaWithCoefficients(eq, coeff_dict)
    eq = simplify_formula(eq)
    return eq

if __name__ == '__main__':
    #problem = "Solve for x: Ax + B = C -->"
    problem = "Expand: (2x - 4)/(2x) = 1 -->"
    solving_system(problem)
    print('FINAL ANSWER')
    print(eq)
    print('-----')