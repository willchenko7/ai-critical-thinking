import torch
from generate_with_gumbel import generate_with_gumbel
from generate import generate
from customTokenizer import loadCustomTokenizer
from equation_checker import equation_checker
from train_on_new_problem import train_on_new_problem
import torch.nn as nn
import re
from formulaConversions import convertFormulaWithNumbers2Coefficients,fillFormulaWithCoefficients,simplify_formula


'''
Goal: test the model that you have trained on a problem outside of the training set by having it try 1 time to generate a solution to the problem
(no gumbel noise, no reinforcement learning)
'''

if __name__ == '__main__':
    #give test prompt
    problem = "Solve for x: Ax + B = C - D -->"
    #convert problem into generic problem
    #problem_parts = re.split(': ',problem.replace('-->',''))
    #new_formula, coeff_dict = convertFormulaWithNumbers2Coefficients(problem_parts[1])
    #problem = problem_parts[0] + ': ' + new_formula + ' -->'
    print(problem)
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    #load model
    model = torch.load('models/sss-final.pth',map_location =device)
    #define criterion and optimizer
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    optimizer = torch.optim.Adam(model.parameters())
    for it in range(1000):
        response = generate(problem,model,tokenizer,device)
        response = response.replace('- - >','-->')
        response = response.replace('[CLS]','')
        response = response.replace('[SEP]','')

        try:
            reward, _ = equation_checker(response)
        except:
            reward = 100

        if reward == 0:
            print(response)
            print(f'Iteration: {it}, Score: {reward}')
            break
        else:
            if it % 10 == 0:
                print(response)
                print(f'Iteration: {it}, Score: {reward}')