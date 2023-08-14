import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import dataset
import matplotlib.pyplot as plt
import os
from datetime import datetime
from reward_model import reward_model
from genericDecoder import Decoder

def train_model(model,criterion,optimizer,train_loader,epochs,b_rlhf,model_name,tokenizer,device):
  train_losses = np.zeros(epochs)

  for it in range(epochs):
    model.train()
    t0 = datetime.now()
    train_loss = []
    for batch in train_loader:
      batch = {k: v.to(device) for k,v in batch.items()}
      optimizer.zero_grad()
      targets = batch['input_ids'].clone().detach()
      targets = torch.roll(targets,shifts=-1,dims=1)
      targets[:,-1] = tokenizer.pad_token_id
      outputs = model(batch['input_ids'],batch['attention_mask'])
      loss = criterion(outputs.transpose(2,1),targets)

      if b_rlhf == True:
        #rlhf
        try:
          scores = reward_model(model)
        except:
          scores = 10
        loss += scores

      loss.backward()
      optimizer.step()
      train_loss.append(loss.item())

    train_loss = np.mean(train_loss)
    train_losses[it] = train_loss
    dt = datetime.now() - t0
    print(f'Epoch: {it+1}/{epochs}, Train Loss: {train_loss:.4f}, Duration: {dt}')
    if it % 50 == 0 or train_loss <= min(x for x in train_losses if x != 0):
      #torch.save(model, f'models/{model_name}-{str(it)}.pth')
      do_nothing = 0
  torch.save(model, f'models/{model_name}-final.pth')
  return train_losses