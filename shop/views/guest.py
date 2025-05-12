# coding=utf-8

import datetime


print(datetime.datetime.now().strftime("%y%m%d%H%M%S"))
print(datetime.datetime.timestamp(datetime.datetime.now()))
digit = int(datetime.datetime.timestamp(datetime.datetime.now()))
print(datetime.datetime.fromtimestamp(timestamp=digit))