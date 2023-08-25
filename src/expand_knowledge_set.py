import torch
from generate_with_gumbel import generate_with_gumbel
from customTokenizer import loadCustomTokenizer
from equation_checker import equation_checker
from train_on_new_problem import train_on_new_problem
import torch.nn as nn
from lol2csv import lol2csv
from append2csv import append2csv
from basic_training_fn import basic_training_fn

'''
Goal: give the model an series of problems to solve with increasing difficulty.

Questions to answer: 
1. can the test_model code solve each of these problems with no modifications?
    If not, where does it fail?

2. If it fails on a prompt, try to save the model after it's learning process for each one.

3. Try adding the prompt + solution to the training set, train a new model on it, then start
'''

test_number = 3
prompts = [
    #"Expand D: D(x - y - z) = A -->",
    #"Expand D: D(w + y) = E -->",
    #"Expand D: D(x - w) = A -->",
    #"Expand D: D(x - y - w) = A -->",
    "Expand D: D(x - y - z - w) = A -->"
]
responses = []
scores = []
l_epochs = []
results = [['prompt','response','score','n_epochs']]
#set device to cuda if available, else cpu
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#load basic model
#model = torch.load('models/basic_model-final.pth',map_location =device)
model = torch.load('models/expansion-test-4-final.pth',map_location =device)
i = 1
for prompt in prompts:
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    if test_number == 1:
        model = torch.load('models/basic_model-final.pth',map_location =device)
    #define criterion and optimizer
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    optimizer = torch.optim.Adam(model.parameters())
    #response,_ = generate_with_gumbel(prompt, model,tokenizer,device, temperature=1.3)
    _,response,n_epochs = train_on_new_problem(model,criterion,optimizer,epochs=5000,model_name='test-new-problem',problem=prompt,in_temperature=1.5,tokenizer=tokenizer,device=device)
    print(response)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')
    print(response)
    responses.append(response)
    try:
        score, l_sympy_eq = equation_checker(response)
    except:
        score = 100
    print(f'Score: {score}')
    scores.append(score)
    l_epochs.append(n_epochs)
    results.append([prompt,response,score,n_epochs])
    fn = f'expansion-test-{test_number}'
    lol2csv(f'results/{fn}.csv',results)

    if score == 0.0 and test_number == 3:
        #append line to train-very-basic-expand.csv
        append2csv('data/train-very-basic-expand.csv',[response.strip()])
        #train new model with that line added
        data_path = 'data/train-very-basic-expand.csv'
        model_name = f'expansion-test-{i}'
        basic_training_fn(data_path,model_name)
        #load that model
        model = torch.load(f'models/{model_name}-final.pth',map_location =device)
    i += 1