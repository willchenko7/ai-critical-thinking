from generate import generate
from equation_checker import equation_checker


def reward_model(model):
  scores = 0
  prompts = [
      "Add A to both sides: x + A = C -->",
      "Subtract D from both sides: x - D = B -->",
      "Divide both sides by A: Ay = B -->",
      "Multiply both sides by A: y/A = B -->",
      "Add A to both sides: y + A = B -->",
      "Subtract A from both sides: z - A = B -->",
      "Divide both sides by Q: Qy = B -->",
      "Add A to both sides: x + A = C -->",
      "Subtract D from both sides: x - D = B -->",
      "Divide both sides by A: Ay = B -->",
      "Multiply both sides by A: y/A = B -->",
      "Add A to both sides: y + A = B -->",
      "Subtract A from both sides: z - A = B -->",
      "Divide both sides by Q: Qy = B -->"
  ]
  for prompt in prompts:
    #print(prompt)
    #give model 3 tries
    for i in range(0,3):
      response = generate(prompt,model)
      response = response.replace('- - >','-->')
      response = response.replace('[CLS]','')
      response = response.replace('[SEP]','')
      score, l_sympy_eq = equation_checker(response)
      if score == 0:
        break
    scores += score
  return scores