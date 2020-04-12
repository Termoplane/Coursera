import csv

with open('csv_example.csv') as csv_fd:
        reader = csv.reader(csv_fd, delimiter = ';')
        next(reader)
        for row in reader:
            print(row[0])