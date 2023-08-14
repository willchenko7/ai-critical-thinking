import torch

def generate(prompt,model,tokenizer,device):
  tokenized_prompt = tokenizer(prompt,return_tensors='pt')
  input_ids = tokenized_prompt['input_ids'][:,:-1].to(device)
  mask = tokenized_prompt['attention_mask'][:,:-1].to(device)
  for _ in range(80):
    outputs = model(input_ids,mask)
    prediction_id = torch.argmax(outputs[:,-1,:],axis=-1)
    input_ids = torch.hstack((input_ids,prediction_id.view(1,1)))
    mask = torch.ones_like(input_ids)

    if prediction_id == tokenizer.sep_token_id:
      break
  return tokenizer.decode(input_ids[0])