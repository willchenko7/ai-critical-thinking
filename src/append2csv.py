import csv

def append2csv(filepath,new_row):
    # Appending to the CSV file
    with open(filepath, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(new_row)
    return