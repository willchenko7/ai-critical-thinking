import os
import pandas as pd
'''
fp = "data/train-very-basic-raw.csv"

df = pd.read_csv(fp)
#combine Question and Answer columns
df["sentence"] = df["Question"] + " " + df["Answer"]
#drop the Question and Answer columns
df = df.drop(columns=["Question","Answer"])

#writes the dataframe to a csv file
df.to_csv("data/train-very-basic.csv",index=False)
'''

def rawTrain2train(f_in,f_out):
    df = pd.read_csv(f'data/{f_in}')
    #combine Question and Answer columns
    df["sentence"] = df["Question"] + " --> " + df["Answer"]
    #drop the Question and Answer columns
    df = df.drop(columns=["Question","Answer"])

    #remove duplicate rows
    df = df.drop_duplicates(subset=["sentence"])

    #writes the dataframe to a csv file
    df.to_csv(f"data/{f_out}",index=False)
    return

if __name__ == '__main__':
    f_in = "train-very-basic-raw.csv"
    f_out = "train-very-basic.csv"
    rawTrain2train(f_in,f_out)