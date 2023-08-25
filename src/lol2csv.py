import csv

def lol2csv(filepath,data):
    # Writing to the CSV file
    with open(filepath, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write each row to the CSV
        for row in data:
            csvwriter.writerow(row)
    return

if __name__ == '__main__':
    data = [['This','is'],['a','test']]
    fp = 'results/test.csv'
    lol2csv(fp,data)