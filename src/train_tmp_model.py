import re
import torch
from basic_training_fn import basic_training_fn
from append2csv import append2csv

def train_tmp_model(model,problem):
    #add problem as tmp solution to problem
    math_problem = re.split('-->',problem)[0]
    math_problem = re.split(': ',math_problem)[1]
    math_problem = math_problem.strip()
    problem = problem + ' ' + math_problem
    #append to tmp dataset
    data_path = 'data/tmp.csv'
    append2csv(data_path,[problem])
    #train basic model
    model_name = 'sss-tmp'
    tmp_model = basic_training_fn(data_path,model_name)
    return tmp_model

if __name__ == '__main__':
    problem = 'Solve for x: A(Bx - C) = D -->'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.load('models/sss-final.pth',map_location =device)
    tmp_model = train_tmp_model(model,problem)