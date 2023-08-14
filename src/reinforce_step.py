from generate_with_gumbel import  generate_with_gumbel
from equation_checker import equation_checker
import torch

def reinforce_step(model,problem,temperature,prev_loss,num_in_a_row,max_num_in_a_row,ignore_list,tokenizer,device,optimizer):
    '''
    # Forward pass through the policy network
    response,action_probabilities = generate(problem,model,temperature=temperature)
    #action = torch.multinomial(action_probabilities, 1)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')
    #print(response)
    '''
    # Forward pass
    #response = generate_with_gumbel(problem, model,temperature)
    response,all_probabilities = generate_with_gumbel(problem, model,tokenizer,device, temperature)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')

    try:
      reward, _ = equation_checker(response)
    except:
      reward = 100

    reward = float(reward)
    if reward in ignore_list or reward*100 in ignore_list:
      reward = max(ignore_list)

    #print(f'Prev: {prev_loss}')
    #print(f'Current: {reward}')
    #print(ignore_list)
    if reward == float(prev_loss):
      #print('same')
      num_in_a_row += 1
    else:
      #print('not same')
      num_in_a_row = 0

    if num_in_a_row > max_num_in_a_row:
      ignore_list.append(reward)
      reward = reward*100
      ignore_list.append(reward)
    
    #print(reward)
    loss = torch.tensor(reward, requires_grad=True)
    #print(loss)

    # Backward pass and optimization
    loss.backward()
    optimizer.step()

    return loss.item(), response, num_in_a_row,max_num_in_a_row,ignore_list