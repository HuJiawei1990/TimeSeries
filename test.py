# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       test.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-05-04 13:28
@version    0.0.1.20180504
--------------------------------------
<enter description here>
"""

import sys
from src.timeSeries.timeSeries import timeSeriesWindow, timeSeries
from src.timeSeries.Analysis import Entropy, get_entropy
import pandas as pd
import numpy as np


def run_test():
    cpu_data = {}
    
    csv_file = './data/10631_cpu.csv'
    seprator = ','
    with open(csv_file, encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if idx == 0:
                col_names = line.strip('\n\r').split(seprator)
            else:
                ts, value = line.strip('\n\r').split(seprator)[0:2]
                cpu_data[int(ts)] = float(value)
            
            if idx > 1000: break
        
        print("Load %d lines of data.. " % len(cpu_data))
    
    '''
    cpu_time_series = timeSeries(cpu_data)
    ## 时间序列的间隔为 60 seconds
    cpu_time_series.set_step(60)
    
    cpu_matrix = cpu_time_series.generate_feature_matrix()
    
    pass
    '''
    
    samp_en = get_entropy(list(cpu_data.values()), en_type='sample', n_cols=2, min_dist=3)
    ap_en = get_entropy(list(cpu_data.values()), en_type='approximate', min_dist=3)
    pe_en = get_entropy(list(cpu_data.values()), en_type='permutation')
    
    print("samp_en = %.5f" % samp_en)
    print("ap_en = %.5f" % ap_en)
    print("pe_en = %.5f" % pe_en)


if __name__ == "__main__":
    run_test()
    
    '''
    l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 3, 2, 1, 5, 2, 1]
    l2 = np.array([85, 80, 89] * 17)
    res = get_entropy(l2, en_type='sample', min_dist=3)
    
    print(res)
    '''
