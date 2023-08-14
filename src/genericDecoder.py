import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import dataset
import matplotlib.pyplot as plt
import os
from datetime import datetime

class CausalSelfAttention(nn.Module):
  def __init__(self,d_k,d_model,n_heads,max_len):
    super().__init__()

    self.d_k = d_k
    self.n_heads = n_heads

    self.key = nn.Linear(d_model,d_k * n_heads)
    self.query = nn.Linear(d_model,d_k * n_heads)
    self.value = nn.Linear(d_model,d_k * n_heads)

    self.fc = nn.Linear(d_k * n_heads,d_model)

    cm = torch.tril(torch.ones(max_len,max_len))
    self.register_buffer("causal_mask",cm.view(1,1,max_len,max_len))


  def forward(self,q,k,v,pad_mask=None):
    q = self.query(q) #N x T x (hd_k)
    v = self.value(v)
    k = self.key(k)

    N = q.shape[0]
    T = q.shape[1]

    #change shape of q,v,k
    #(N,T,h,d_k) --> (N,h,T,d_k)
    q = q.view(N, T,self.n_heads,self.d_k).transpose(1,2)
    v = v.view(N, T,self.n_heads,self.d_k).transpose(1,2)
    k = k.view(N, T,self.n_heads,self.d_k).transpose(1,2)

    #compute attention weights
    #(N,h,T,d_k) X (N,h,d_k,T) --> (N,h,T,T)
    attn_scores = q @ k.transpose(-2,-1) / math.sqrt(self.d_k)

    if pad_mask is not None:
      attn_scores = attn_scores.masked_fill(
          pad_mask[:,None,None,:] == 0, float('-inf'))

    attn_scores = attn_scores.masked_fill(
        self.causal_mask[:,:,:T,:T] == 0, float('-inf'))

    attn_weights = F.softmax(attn_scores,-1)

    #(N,h,T,T) X (N,h,T,d_k) --> (N,h,T,d_k)
    A = attn_weights @ v

    A = A.transpose(1,2) # (N,h,T,d_k) --> (N,T,h,d_k)

    #(N,T,h,d_k) --> (N,T,d_k * h)
    A = A.contiguous().view(N,T,self.d_k * self.n_heads)

    return self.fc(A)

class TransformerBlock(nn.Module):
  def __init__(self,d_k,d_model,n_heads,max_len,dropout_prob=0.1):
    super().__init__()

    self.mha = CausalSelfAttention(d_k,d_model,n_heads,max_len)

    self.ln1 = nn.LayerNorm(d_model)
    self.ln2 = nn.LayerNorm(d_model)

    self.ann = nn.Sequential(
        nn.Linear(d_model,d_model*4),
        nn.GELU(),
        nn.Linear(d_model * 4,d_model),
        nn.Dropout(dropout_prob)
    )

    self.dropout = nn.Dropout(p=dropout_prob)


  def forward(self,x,pad_mask=None):
    x = self.ln1(x + self.mha(x,x,x,pad_mask))
    x = self.ln2(x + self.ann(x))
    x = self.dropout(x)
    return x

class PositionalEncoding(nn.Module):
  def __init__(self,d_model,max_len=2048,dropout_prob=0.1):
    super().__init__()
    self.dropout = nn.Dropout(p=dropout_prob)

    position = torch.arange(max_len).unsqueeze(1)
    exp_term = torch.arange(0,d_model,2)
    div_term = torch.exp(exp_term*(-math.log(10000.0)/d_model))
    pe = torch.zeros(1,max_len,d_model)
    pe[0,:,0::2] = torch.sin(position * div_term)
    pe[0,:,1::2] = torch.cos(position * div_term)
    self.register_buffer('pe',pe)

  def forward(self,x):
    x = x + self.pe[:,:x.size(1),:]
    return self.dropout(x)

class Decoder(nn.Module):
  def __init__(self,vocab_size,max_len,d_k,d_model,n_heads,n_layers,dropout_prob):
    super().__init__()

    self.embedding = nn.Embedding(vocab_size,d_model)
    self.pos_encoding = PositionalEncoding(d_model,max_len,dropout_prob)
    transformer_blocks = [
        TransformerBlock(
            d_k,
            d_model,
            n_heads,
            max_len,
            dropout_prob
        ) for _ in range(n_layers)
    ]
    self.transformer_blocks = nn.Sequential(*transformer_blocks)

    self.ln = nn.LayerNorm(d_model)
    self.fc = nn.Linear(d_model,vocab_size)

  def forward(self,x,pad_mask=None):
    x = self.embedding(x)
    x = self.pos_encoding(x)
    for block in self.transformer_blocks:
      x = block(x,pad_mask)
    x = self.ln(x)
    x = self.fc(x) #many outputs
    return x

if __name__ == '__main__':
    #test model with random input
    model = Decoder(20_000,1024,16,644,4,2,0.1)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    model.to(device)
    print(model)