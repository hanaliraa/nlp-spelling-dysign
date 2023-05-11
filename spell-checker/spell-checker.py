import csv
import os
import pandas as pd

#functions
def dataset(folder):
    s_list = list()
    tgt_file = 'D:\OneDrive - Habib University\Kaavish\\nlp-spelling-dysign/data.csv'
    for x in os.listdir(folder):

        with open(folder+x, mode='r', newline='\n') as file:
            line = file.readlines()
            # print(id, line[0])
            s_list.append([x[:-4], line[0]])
    with open(tgt_file, mode='w', newline='\n') as file:
        writer = csv.writer(file)
        for x in s_list:
            writer.writerow(x)
def scoring(df):
    print(df['sentence'])
folder1 = 'D:\OneDrive - Habib University\Kaavish\\nlp-spelling-dysign\Data\data_transcibed/'
data = 'D:\OneDrive - Habib University\Kaavish\\nlp-spelling-dysign/data.csv'

# dataset(folder1)   #creating a csv
word_dict = {
    1: 'the',
    2: 'beautiful',
    3: 'ducks',
    4: 'swam',
    5: 'in',
    6: 'big',
    7: 'blue',
    8: 'lake',
    9: 'their',
    10: 'feathers',
    11: 'were',
    12: 'very',
    13: 'pretty',
    14: 'and',
    15: 'quite',
    16: 'often',
    17: 'would',
    18: 'jump',
    19: 'out',
    20: 'of',
    21: 'water',
}

df = pd.read_csv(data)
scoring(df)
