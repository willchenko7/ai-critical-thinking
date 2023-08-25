import csv

def csv2lol(filepath):
    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        data_list = [row for row in csvreader]
    return data_list