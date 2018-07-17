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
from .Analysis import Entropy,get_entropy

logger = logging.getLogger("timeSeries")


class timeSeries(object):
    def __init__(self, time_series=None):
        if time_series is None:
            time_series = {}
        self.content = time_series
        self.values = np.array(time_series.values())
        self.size = len(time_series)
        self._step = 0
        self.timestamp_start = None if time_series == {} else min(time_series.keys())
        self.timestamp_end = None if time_series == {} else max(time_series.keys())
    
    
    def add_element(self, ts, value):
        if ts in self.content:
            logger.error("Failed to add element into time series.")
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
    
    
    ## TODO: 空值填充
    
    def sub_series(self, start, end):
        """
        截取某个时间窗口中的子时间序列
        :param start: 时间窗口开头(包含该点)
        :param end: 时间窗口结束(不包含该点)
        :return: timeSeries
        """
        sub = timeSeriesWindow({key: self.content[key]
                                for key in self.content.keys()
                                if ((key >= start) and (key < end))})
        
        ## 保留原有的时间序列间隔
        sub.set_step(self._step)
        
        return sub
    
    def split(self, window_pts=None, slide_pts=None):
        ## define the default window size:
        ##  By default, it contains 30 points in each window
        ##  and it slides 10 points every time to create the new window
        ## 定义默认的窗口长度: 包含30个时间点, 每次挪动10个时间点
        if window_pts is None: window_pts = 30 * self._step
        if slide_pts is None: slide_pts = 10 * self._step
        
        starts = range(self.timestamp_start, self.timestamp_end - window_pts + slide_pts, slide_pts)
        #ends = [start + window_size for start in starts]
        
        windows = []
        for idx, start in enumerate(starts):
            end = start + window_pts
            windows.append(self.sub_series(start, end))
            
        return windows

    #class Features(object):
        """
        compute all features of this times series. It has no NULL value by default
        计算该时间序列的各个特征量, 默认该序列没有空值
        """
        def acf(self, n=1):
            """
            TODO：compute acf of time series
            :param n:
            :return:
            """
            mean = self.values.mean()
            
            
        def through_times(self, x0):
            """
            计算时间序列曲线通过 x=x0 横线的次数
            # TODO: deal with NONE value
            :param x0:
            :return: int
            """
            ans = 0
            for idx, val in enumerate(self.values):
                if idx < self.size:
                    next_val = self.values[idx + 1]
                else:
                    return ans
                if (val <= x0 <= next_val) or (next_val <= x0 <= val):
                    ans += 1
        
        def entropy(self):
            res = 0
            
            return res
    
    
            
    def generate_feature_matrix(self, window_pts=None, slide_pts=None):
        try:
            windows = self.split(window_pts, slide_pts)
        except Exception as e:
            logger.error("Error occurs when splitting time series into small windows.")
            logger.error(e)
            
        matrix = np.array([window.features_generation().values() for window in windows])
        
        return matrix
        
        
class timeSeriesWindow(timeSeries):
    def features_generation(self):
        """
        list of features:
            - Mean      : mean of all values
            - Var       : variance of all values
            - ACF1      : first order auto-correlation, Corr(X_t, X_t-1)
            - Trend     :
            - linearity : x_n = a*n+b, return (a,b)
            - Curvature : 曲率, |y''| / ((1 + y'^2) ^ 1.5)
            - Season    : 周期
            - Peak      : 峰值
            - Trough    :
            - Entropy   : spectral entropy
            - Lumpiness : variance of block variance(block size 24/30/...)
            - Spikiness : variance of leave-one-out variances of STL remainders
            - Lshift    : maximum difference in trimmed means of consecutive moving windows of size 24
            - Vchange   : maximum difference in variances of consecutive moving windows of size 24
            - Fspots    : Discretize sample space into 10 equal-sized intervals. Find max run length in any interval.
            - Cpoints   : number of crossing points of mean line
            - KLscore   : Kullback-Leibler score: https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence
                          distribution estimators applied to consecutive windows of size 48.
            - Change.Idx: times fof maximum KL score
        :return:
        """
        
        features = {}
        ## 起始时间(使用unix 10位时间戳表示)
        features['start'] = self.timestamp_start
        features['end'] = self.timestamp_end
        ## 该时间序列窗口的长度(单位为秒)
        features['window_size'] = self.timestamp_end - self.timestamp_start
        ## 时间序列中真实存在的记录数
        features['nb_points'] = self.size
        ## 时间序列中的步长
        features['step'] = self.get_step()
        ## 时间序列窗口应有的记录数
        features['all_points'] = features['window_size'] / features['step'] + 1
        ## 时间序列的完整程度
        features['complete_rate'] = features['nb_points'] / float(features['all_points'])
        
        ## 计算时间序列中每个时间点的值
        values = np.array([self.content[ts] for ts in sorted(self.content.keys())])
        #features['values'] = values
        for idx, value in enumerate(values):
            features['value_' + str(idx)] = value
        
        features['value_max'] = max(values)
        features['value_min'] = min(values)
        
        features['value_sum'] = sum(values)
        features['value_avg'] = values.mean()
        features['value_var'] = values.var()
        features['value_std'] = np.std(values, ddof=0)
        
        ## 计算每个时间点的值变化量, 以及变换量的特征
        values_diff = np.array([values[i + 1] - values[i] for i in range(self.size - 1)])
        #features['values_diff'] = values_diff
        for idx, value in enumerate(values_diff):
            features['value_diff_' + str(idx)] = value
            
        ## compute the maximum/minimum values of differences
        features['diff_max'] = max(values_diff)
        features['diff_min'] = min(values_diff)
        features['diff_abs_max'] = max([abs(val) for val in values_diff])
        features['diff_abs_min'] = min([abs(val) for val in values_diff])
        
        features['diff_sum'] = sum(values_diff)
        features['diff_abs_sum'] = sum([abs(val) for val in values_diff])
        features['diff_avg'] = values_diff.mean()
        features['diff_abs_avg'] = features['diff_abs_sum'] / (self.size-1)
        features['diff_var'] = values_diff.var()
        features['diff_std'] = np.std(values_diff, ddof=0)
        
        
        ## 计算时间窗口中的变化率
        diff_rate = np.array([(values[i + 1] - values[i]) / values[i] for i in range(self.size - 1)])

        for idx, value in enumerate(values_diff):
            features['diff_rate_' + str(idx)] = value
        
        features['samp_entropy'] = get_entropy(self.values, en_type='sample')
        
        ## debug logs: print all features get.
        ## 日志打印: 所有特征信息
        logger.debug("all features computed:")
        for key in features:
            logger.debug("{}:\t{}".format(key, features[key]))
        
        return features
    
        
        
    
