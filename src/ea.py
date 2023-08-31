import torch
import random
from generate import generate
from customTokenizer import loadCustomTokenizer
from equation_checker import equation_checker
import torch.nn as nn
import re

def reward_fn(problem,model,tokenizer,device):
    response = generate(problem,model,tokenizer,device)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')
    print(response)
    #check if equation in prompt and response are exactly the same
    #if so, give it a score of 5 and leave
    #tries to serve as a home base, if you go to far, just go back to the original problem
    eq1 = re.split('-->',response)[0]
    eq1 = re.split(':',eq1)[1]
    eq2 = re.split('-->',response)[1]
    eq1 = eq1.replace(' ','')
    eq2 = eq2.replace(' ','')
    if eq1 == eq2:
        return 5,response
    if eq2 == 'A=D/(Bw-C)':
        return 10,response
    try:
        reward, _ = equation_checker(response)
    except:
        reward = 100
    return reward,response

def ea(problem):
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    #load model
    pre_trained_model = torch.load('models/sss-tmp-final.pth',map_location =device)

    # Initialize a population using the "pre-trained" model
    population_size = 200
    population = [pre_trained_model for _ in range(population_size)]

    # Use pre-trained weights for the entire population but introduce slight mutations for diversity
    mutation_strength = 0.001
    for model in population:
        model.load_state_dict(pre_trained_model.state_dict())
        for param in model.parameters():
            param.data += mutation_strength * torch.randn_like(param.data)

    # Evolutionary parameters
    generations = 10
    mutation_rate = 0.0001
    for generation in range(generations):
        print(f'Generation: {generation}')
        # Evaluate fitness
        fitness = []
        for nn in population:
            #output = nn(torch.tensor([1.0]))
            #fitness.append(reward_function(output))
            reward,response = reward_fn(problem,nn,tokenizer,device)
            if reward == 0.0:
                print('PROBLEM SOLVED!')
                torch.save(nn, f'models/ea-best1.pth')
                return nn, response
            fitness.append(reward)
        #print(fitness)
        
        # Select top k% of networks
        k = 20
        #n / pop_div = k --> pop_div = n/k
        pop_div = int(population_size / k)
        selected_indices = sorted(range(len(fitness)), key=lambda i: fitness[i])[:population_size // pop_div]
        selected_networks = [population[i] for i in selected_indices]
        
        # Create new population with crossover and mutation
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = random.choices(selected_networks, k=2)
            
            # Simple crossover (averaging)
            child_state_dict = {}
            for key in parent1.state_dict():
                child_state_dict[key] = (parent1.state_dict()[key] + parent2.state_dict()[key]) / 2
            
                # Mutation
                if random.random() < mutation_rate:
                    child_state_dict[key] += torch.randn_like(child_state_dict[key]) * 0.1
            
            #child = SimpleNN(1, 1)
            child = pre_trained_model
            child.load_state_dict(child_state_dict)
            new_population.append(child)
        
        population = new_population

    # Test the best evolved network
    best_network = population[selected_indices[0]]
    torch.save(best_network, f'models/ea-best1.pth')
    return best_network, problem + ' NA '

if __name__ == '__main__':
    #set device to cuda if available, else cpu
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    #load tokenizer and data_collator
    tokenizer_path = 'data/my_tokenizer'
    tokenizer,data_collator = loadCustomTokenizer(tokenizer_path,model_max_length=512)
    problem = "Solve for x: Bx = (D/A) + C -->"
    best_network,response = ea(problem)
    response = generate(problem,best_network,tokenizer,device)
    response = response.replace('- - >','-->')
    response = response.replace('[CLS]','')
    response = response.replace('[SEP]','')
    print(response)
