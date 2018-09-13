#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil.parser import parse

RAINFALL_THRESHOLD = 0.01

#寻找时间间隔大于规定时间的一个连续降水事件
def find_rainfall_event(preci, event_begin, max_interval):
    n = len(preci)
    interval = 0
    #find the rainfall event begin position
    while(preci[event_begin] <= RAINFALL_THRESHOLD):
        if event_begin >= n - 1:
            return n, n
        else:
            event_begin += 1

    event_end = event_begin

    #find rainfall event end position
    for i in range(event_begin+1, n):
        if preci[i] <= RAINFALL_THRESHOLD:
            interval += 1
        else:
            interval =0
            event_end = i
        if interval > max_interval or event_end >= n-1:
            break
    return event_begin, event_end

#计算一次降水事件的相关属性：起始时间，终止时间，历时，降水峰值，降水总量，降水强度，峰值/降水强度
def cal_attribute(timestart, timeend, preci, event_begin, event_end):
    start = parse(str(timestart[event_begin]))
    end = parse(str(timeend[event_end]))
    duriation = (end - start).days * 24 + (end - start).seconds / 3600
    temp = []
    for i in range(event_begin, event_end+1):
        temp.append(preci[i])

    peak = max(temp)
    amount = sum(temp)
    intensity = amount / duriation
    return [start, end, duriation, peak, amount, intensity, peak/intensity*2]

def export_csv(res, name):
    csvfile = open("result_%s.csv" % ( name ), 'w', newline='')
    writer = csv.writer(csvfile)
    # 先写入columns_name
    writer.writerow(["起始时间", "终止时间", "历时(h)", "峰值(mm)", "降水总量(mm)",
                     "平均降水强度(mm/h)", "峰值/平均降水强度", "与下一场降水间隔时间（h）"])
    writer.writerows(res)
    print("Done!")


def fun_cal(path, max_interval,name):
    df = pd.read_csv(path, encoding='utf-8')
    len_df = len(df)
    timestart = []
    timeend = []
    preci = []
    res = []

    # 提取起始时间终止时间和降水数据
    for i in df.TIMESTAMP_START:
        timestart.append(i)
    for i in df.TIMESTAMP_END:
        timeend.append(i)
    for i in df.P_F:
        preci.append(i)

    event_begin = 0
    event_end = 0
    while event_begin < len_df :

        event_begin, event_end = find_rainfall_event(preci, event_begin, max_interval)
        if event_begin <= len_df-1:

            res.append(cal_attribute(timestart, timeend, preci, event_begin, event_end))

        event_begin = event_end + 1
        event_end = event_begin

    # 计算一场降水事件到下一场降水事件的时间间隔
    for i in range(len(res) - 1):
        start = parse(str(res[i][1]))
        end = parse(str(res[i + 1][0]))
        interval = (end - start).days * 24 + (end - start).seconds / 3600
        res[i].append(interval)
    res[len(res) - 1].append(0)

    #输出为csv文件
    export_csv(res,name)

if __name__ == '__main__':

    filepath = r"CN-Cha_data.csv"
    fun_cal(filepath,0,"original")
    fun_cal(filepath,1,"0.5h")
    fun_cal(filepath,2,"1h")
    fun_cal(filepath,4,"2h")