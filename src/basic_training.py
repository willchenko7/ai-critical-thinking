import torch
from train_model import train_model
from torch.utils.data import DataLoader
from transformers import PreTrainedTokenizerFast, DataCollatorWithPadding
from customTokenizer import loadCustomTokenizer
from datasets import Dataset
from datasets import load_dataset
from genericDecoder import Decoder
import torch.nn as nn

def tokenize_fn(batch):
  return tokenizer(batch['sentence'],truncation=True)

if __name__ == '__main__':
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    #create new model
    model = Decoder(
        vocab_size=tokenizer.vocab_size + 4,
        max_len=512,
        d_k=32,
        d_model=132,
        n_heads=8,
        n_layers=4,
        dropout_prob=0.1
    )
    model.to(device)
    #define criterion and optimizer
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    optimizer = torch.optim.Adam(model.parameters())
    #load dataset
    data_path = 'data/train-very-basic.csv'
    dataset = load_dataset("csv", data_files=data_path)
    #tokenize dataset
    tokenized_datasets = dataset.map(tokenize_fn,batched=True)
    tokenized_datasets = tokenized_datasets.remove_columns(['sentence'])
    train_loader = DataLoader(
        tokenized_datasets['train'],
        shuffle=True,
        batch_size=32,
        collate_fn=data_collator
    )
    #train model
    train_losses = train_model(model,
        criterion,
        optimizer,
        train_loader,
        epochs=100,
        b_rlhf=False,
        model_name='basic_model',
        tokenizer=tokenizer,
        device=device
    )
    print('Done!')
