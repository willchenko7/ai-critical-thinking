import torch
from generate_with_gumbel import generate_with_gumbel
from generate import generate
from customTokenizer import loadCustomTokenizer
from equation_checker import equation_checker
from train_on_new_problem import train_on_new_problem
import torch.nn as nn

'''
Goal: test the model that you have trained on a problem outside of the training set by having it try 1 time to generate a solution to the problem
(no gumbel noise, no reinforcement learning)
'''

if __name__ == '__main__':
    #give test prompt
    prompt = "Expand B: B(x - y - z) = A -->"
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    #load model
    model = torch.load('models/basic_model-final.pth',map_location =device)
    #define criterion and optimizer
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    optimizer = torch.optim.Adam(model.parameters())
    for it in range(1):
        response = generate(prompt,model,tokenizer,device)
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