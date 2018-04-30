# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       timeSeries.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-04-25 14:14
@version    0.0.1.20180425
--------------------------------------
<enter description here>
"""

import sys
import numpy as np
import logging

logger = logging.getLogger("timeSeries")


class timeSeries(object):
    def __init__(self, time_series={}):
        # if time_series=={}:
        self.content = time_series
        self.size = len(time_series)
        self._step = 0
        self.timestamp_start = None if time_series == {} else min(time_series.keys())
        self.timestamp_end = None if time_series == {} else max(time_series.keys())
    
    
    def add_element(self, ts, value):
        if ts in self.content:
            raise KeyError("Key [%s] already exists in time series." % ts)
        
        ## add new element into time series, refresh parameters
        self.content[ts] = value
        self.size += 1
        self.timestamp_start = min(self.timestamp_start, ts)
        self.timestamp_end = max(self.timestamp_end, ts)
        

    
    def set_step(self, step):
        """
        reset the step-length between timestamps
        :param step: step length
        """
        self._step = step
        
        
    def get_step(self):
        """
        return the step length value of time series
        :return: step length of
        """
        return self._step


class timeSeriesWindow(timeSeries):
    def features_generation(self):
        features = {}
        ## 该时间序列窗口的长度
        features['window_size'] = self.timestamp_end - self.timestamp_start
        ## 时间序列中真实存在的记录数
        features['nb_points'] = self.size
        ## 时间序列中的步长
        features['step'] = self.get_step()
        ## 时间序列窗口应有的记录数
        features['all_points'] = features['window_size'] / features['step'] + 1
        ## 时间序列的完整程度
        features['complete_rate'] = features['nb_points'] / float(features['all_points'])

        ## compute the features of values list of tine
        values = np.array([self.content[ts] for ts in sorted(self.content.keys())])
        features['values'] = values
        
        features['value_max'] = max(values)
        features['value_min'] = min(values)
        
        features['value_sum'] = sum(values)
        features['value_avg'] = values.mean()
        features['value_var'] = values.var()
        features['value_std'] = np.std(values, ddof=0)
        
        ## compute feature of differences between
        values_diff = np.array([values[i+1] - values[i] for i in range(self.size - 1)])
        features['values_diff'] = values_diff
        
        features['diff_max'] = max(values_diff)
        features['diff_min'] = min(values_diff)

        features['diff_sum'] = sum(values_diff)
        features['diff_avg'] = values_diff.mean()
        features['diff_var'] = values_diff.var()
        features['diff_std'] = np.std(values_diff, ddof=0)

        




if __name__ == "__main__":
    pass
