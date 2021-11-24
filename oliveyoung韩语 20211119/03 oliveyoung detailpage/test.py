import csv

with open('oliveyoung_listing.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)
    # print(fieldnames)
    csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # self._fieldnames = fieldnames
    # list of keys for the dict 以list的形式存放键名
    for row in csv_reader:
        d = {}
        for k, v in row.items():
            d[k] = v
        urls_detailpage = list(d.values())[5]