from reinforce_step import reinforce_step
import numpy as np
import torch
from datetime import datetime


def train_on_new_problem(model,criterion,optimizer,epochs,model_name,problem,in_temperature,tokenizer,device):
  train_losses = np.zeros(epochs)

  num_in_a_row = 0
  max_num_in_a_row = 3
  prev_loss = float(0.0)
  ignore_list = []
  for it in range(epochs):
    model.train()
    t0 = datetime.now()
    train_loss = []
    
    if it > 1 and loss < 5:
      temperature = 1.2
    else:
      temperature = in_temperature

    loss,response,num_in_a_row,max_num_in_a_row,ignore_list = reinforce_step(model,problem,temperature,prev_loss,num_in_a_row,max_num_in_a_row,ignore_list,tokenizer,device,optimizer)
    prev_loss = float(loss)
    train_loss.append(loss)

    train_loss = np.mean(train_loss)
    train_losses[it] = train_loss
    dt = datetime.now() - t0
    if it % 10 == 0 or train_loss <= 0.0:
      #torch.save(model, f'/content/gdrive/My Drive/models/{model_name}-{str(it)}.pth')
      print(f'Epoch: {it+1}/{epochs}, Train Loss: {train_loss:.4f}, Duration: {dt}')
      print(response)
    if train_loss == 0.0:
      break
  #torch.save(model, f'/content/gdrive/My Drive/models/{model_name}-final.pth')
  return train_losses,response,it