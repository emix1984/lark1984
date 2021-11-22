# import csv
#
# mydict = {}
#
# with open('oliveyoung category 20211119.csv', mode='r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     dict_from_csv = {rows[0:]:rows[1] for rows in reader}
# print(dict_from_csv)
import csv
import pandas as pd
dict_from_csv = pd.read_csv('oliveyoung category 20211119.csv', header=None, index_col=0, squeeze=True).to_dict()
print(dict_from_csv)
keys = dict_from_csv.keys()
print(keys)