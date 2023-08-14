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

def gumbel_softmax_sample(logits, temperature):
    """ Draw a sample from the Gumbel-Softmax distribution"""
    uniform = torch.rand_like(logits)
    gumbel_noise = -torch.log(-torch.log(uniform + 1e-20) + 1e-20)
    y = logits + gumbel_noise
    return F.softmax(y / temperature, dim=-1)

def gumbel_softmax(logits, temperature, hard=False):
    """Sample from the Gumbel-Softmax distribution and optionally discretize."""
    y = gumbel_softmax_sample(logits, temperature)
    if hard:
        # Hard sampling: this part is not differentiable
        _, max_index = y.max(dim=-1, keepdim=True)
        y_hard = torch.zeros_like(logits).scatter_(-1, max_index, 1.0)
        y = (y_hard - y).detach() + y
    return y


def generate_with_gumbel(prompt, model,tokenizer,device, temperature=1.0):
    tokenized_prompt = tokenizer(prompt, return_tensors='pt')
    input_ids = tokenized_prompt['input_ids'][:,:-1].to(device)
    mask = tokenized_prompt['attention_mask'][:,:-1].to(device)
    all_probabilities = []
    for _ in range(80):
        outputs = model(input_ids, mask)
        
        # Adjust logits with temperature
        adjusted_logits = outputs[:,-1,:] / temperature
        
        # Use softmax to get probabilities
        probabilities = F.softmax(adjusted_logits, dim=-1)
        all_probabilities.append(probabilities)
        
        # Sample from the distribution or take the argmax
        prediction_id = torch.multinomial(probabilities, num_samples=1).squeeze()
        # Or if you want to stick with argmax: 
        # prediction_id = torch.argmax(adjusted_logits, axis=-1)
        #print(input_ids)
        input_ids = torch.hstack((input_ids, prediction_id.view(1, 1)))
        mask = torch.ones_like(input_ids)

        if prediction_id == tokenizer.sep_token_id:
            break
    all_probabilities = torch.stack(all_probabilities, dim=1)        
    return tokenizer.decode(input_ids[0]),all_probabilities