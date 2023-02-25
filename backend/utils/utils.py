#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： sunxuan
# datetime： 2022/1/17 16:04 
# ide： PyCharm
from  datetime import  datetime,timedelta
# def format_time(india_time_str, india_format='%Y-%m-%dT%H:%M:%S'):
#     india_dt = datetime.strptime(india_time_str, india_format)
#     local_dt = india_dt + timedelta(hours=8)
#     local_format = "%Y-%m-%d %H:%M:%S"
#     time_str = local_dt.strftime(local_format)
#     return time_str
#
#
#
# if __name__ == '__main__':
#     print(format_time(datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M:%S')))



def time_handler(target_time):
    _date = datetime.strptime(target_time, "%Y-%m-%dT%H:%M:%S")
    local_time = _date + timedelta(hours=8)
    end_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    return end_time


if __name__ == '__main__':
    start_time = "2020-08-26T06:55:33.000Z"
    time_str = time_handler(start_time)
    print(time_str)