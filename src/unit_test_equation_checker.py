'''
Goal: test the fuctionality of the equation_checker.py module on data/train-very-basic.csv
'''
import unittest
from equation_checker import equation_checker
import pandas as pd

class TestEquationChecker(unittest.TestCase):
    def test_equation_checker(self):
        #read in the csv file
        df = pd.read_csv("data/train-very-basic.csv")
        for i in range(len(df)):
            #get the sentence
            sentence = df["sentence"][i]
            print(sentence)
            #get the score and list of sympy equations
            score,l_sympy_eq = equation_checker(sentence)
            print(l_sympy_eq)
            #check if the score is 0
            self.assertEqual(score,0)
    
if __name__ == '__main__':
    unittest.main()
