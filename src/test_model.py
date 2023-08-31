import torch
from generate_with_gumbel import generate_with_gumbel
from customTokenizer import loadCustomTokenizer
from equation_checker import equation_checker
from train_on_new_problem import train_on_new_problem
import torch.nn as nn

if __name__ == '__main__':
    #give test prompt
    prompt = "Solve for x: Ax = C -D - B -->"
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
    temp = 1.5
    _,response,_ = train_on_new_problem(model,criterion,optimizer,epochs=1000,model_name='test-new-problem',problem=prompt,in_temperature=temp,tokenizer=tokenizer,device=device)
    print(response)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')
    print(response)
    score, l_sympy_eq = equation_checker(response)
    print(f'Score: {score}')