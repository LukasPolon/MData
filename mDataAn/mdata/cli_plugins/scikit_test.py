import pandas as pd
from pandas_datareader import data as web
import datetime
import csv
import mdata.common as common
import os

# start = datetime.datetime(2017, 1, 1)
# end = datetime.date.today()

# apple = web.DataReader('GOOGL', 'yahoo', start, end)
# print (type(apple))
# print(apple.head())
# gticker='GOOG'
# dfg = web.DataReader(gticker, 'google', '2009/1/1', '2014/3/1')
# print (type(dfg))
# print(dfg)


def read_csv():
    file_name = os.path.join(common.MAIN_DIRECTORY, 'companylist.csv')
    symbols = list()
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        symbols = [i[0] for i in reader]
    return symbols




# ok = 0
# bad = 0
# for symbol in read_csv():
#     try:
#         dfg = web.DataReader(symbol, 'google', '2009/1/1', '2014/3/1')
#         print(symbol, 'ok')
#         ok += 1
#     except Exception as e:
#         print(symbol, 'bad', e)
#         bad += 1

