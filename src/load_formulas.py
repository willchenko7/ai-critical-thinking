import json

def load_formulas():
    with open('data/formulas.json', 'r') as file:
        formulas = json.load(file)
    return formulas