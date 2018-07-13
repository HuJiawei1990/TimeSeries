# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       Permutation_entropy.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-07-11 13:35
@version    0.0.1.20180711
--------------------------------------
<enter description here>
"""

from datetime import datetime
from scipy.stats import entropy
import logging

logger = logging.getLogger("permutation")


class Permutation_entropy(object):
    def __init__(self, values=[], n_cols=1, n_rows=None):
        self.values = values
        
        ## transform the list into 2-d matrix format
        ## 将数列转化为2维矩阵的形式
        self.n_cols = n_cols
        self.n_rows = len(values) - n_cols if n_rows is None else n_rows
        self.value_matrix = [self.values[i:i + self.n_cols]
                             for i in range(self.n_rows)]
        
        ## 矩阵每一行的排序后的下标顺序
        self.permutations = []
        self.permutation_unique = []
        self.permutation_count = []
        
        ## permutation entropy
        ## 排序熵
        self.permutation_entropy = None


    def index_sort(self, l1):
        """
        对l1元素排序, 并输出对应的下标
        :param l1:
        :return:
        """
        res = sorted(enumerate(l1), key=lambda x: x[1])
        res1 = [i[0] for i in res]
        
        logger.debug("--- sort list: " + str(l1))
        logger.debug("--- index after sorting: " + str(res1))
        
        return res1
    
    
    def permutation(self):
        """
        对矩阵中每一行数据进行排序, 得到有序数列的下标顺序
        
        :return:
        """
        start = datetime.now()
        res = []
        for r in self.value_matrix:
            res.append(self.index_sort(r))
        
        self.permutations = res
        
        end1 = datetime.now()
        logger.info("--- Sorted {} listed with length {}.".format(self.n_rows, self.n_cols))
        logger.info('--- It takes %.3f seconds to sort data.' %
                    ((end1 - start).seconds + (end1 - start).microseconds / 1e6)
                    )
        logger.info("*" * 10 + " end of permutation " + "*" * 10)

        for i in res:
            if i in self.permutation_unique:
                find_index = self.permutation_unique.index(i)
                self.permutation_count[find_index] += 1
            else:
                self.permutation_unique.append(i)
                self.permutation_count.append(1)
    
    
    def compute_entropy(self):
        self.permutation_entropy = entropy(self.permutation_count, base=10)
    
    
    def get_permutation_entropy(self):
        logger.info("*" * 10 + " begin of compute permutation entropy " + "*" * 10)
        
        start_time = datetime.now()
        self.permutation()
        self.compute_entropy()
        
        end_time = datetime.now()
        logger.info('--- It takes %.3f seconds to compute permutation entropy.' %
                    ((end_time - start_time).seconds + (end_time - start_time).microseconds / 1e6)
                    )
        logger.info("*" * 10 + " end of compute permutation entropy " + "*" * 10)
