# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       ApEn.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-07-13 10:47
@version    0.0.1.20180713
--------------------------------------
Approximate Entropy
计算序列的近似熵

Reference
https://en.wikipedia.org/wiki/Approximate_entropy#cite_note-Pincus21991-23
"""

from scipy.spatial.distance import pdist, squareform
from scipy.stats import entropy
from numpy import array, log
from datetime import datetime
import logging

logger = logging.getLogger('ApEntropy')


class Entropy(object):
    """
    通常选择参数m=2或m=3；r的选择在很大程度上取决于实际应用场景，通常选择r=0.2∗std，其中std表示原时间序列的标准差.
    """
    
    
    def __init__(self, values=[], m=3, min_dist=None, dist_type='chebychev'):
        self.values = values
        self.length = len(values)
        self.m = m
        self.min_dist = min_dist
        self.dist_type = dist_type
        self.ap_entropy_val = None
        self.permutation_unique = []
        self.permutation_count = []
        self.permutations = None
        self.permutation_entropy_val = None
    
    
    def reshape(self, n_cols, n_rows=None):
        if n_rows is None:
            n_rows = self.length - n_cols + 1
        
        value_matrix = [
            self.values[i:i + n_cols] for i in range(n_rows)
        ]
        
        return value_matrix
    
    
    '''
    Sample Entropy
    '''
    
    def _phi(self, m, r, dist_type='chebychev', case='approximate'):
        value_matrix = self.reshape(n_cols=m)
        
        N = len(value_matrix)
        
        logger.info(">> calculating distance between {} vectors with type [{}].".format(N, dist_type.upper()))
        dist_matrix = squareform(pdist(value_matrix, dist_type))
        
        appr_nb = [sum([1 if d < r else 0 for d in row]) / N for
                   row in dist_matrix]
        
        phi = sum([log(c) for c in appr_nb]) / N if case == 'approximate' \
            else sum(appr_nb) / N
        
        return phi
    
    
    def approximate_entropy(self, m: int, r: float, dist_type: str) -> float:
        return self._phi(m, r, dist_type) - self._phi(m + 1, r, dist_type)
    
    
    def get_ap_entropy(self):
        ap_entropy = self.approximate_entropy(self.m, self.min_dist, self.dist_type)
        self.ap_entropy_val = ap_entropy
    
    
    def sample_entropy(self, m: int, r: float, dist_type: str) -> float:
        return log(self._phi(m, r, dist_type, case='sample')
                   / self._phi(m + 1, r, dist_type, case='sample'))
    
    
    def get_samp_entropy(self):
        self.samp_entropy_val = self.sample_entropy(self.m, self.min_dist, self.dist_type)
    
    
    '''
    permutation entropy
    '''
    
    
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
    
    
    def permutation(self, n_cols=3, n_rows=None):
        """
        对矩阵中每一行数据进行排序, 得到有序数列的下标顺序

        :return:
        """
        start = datetime.now()
        res = []
        for r in self.reshape(n_cols, n_rows):
            res.append(self.index_sort(r))
        
        self.permutations = res
        
        end1 = datetime.now()
        logger.debug(">> Sorted {} listed with length {}.".format(n_rows, n_cols))
        logger.debug('>> It takes %.3f seconds to sort data.' %
                     ((end1 - start).seconds + (end1 - start).microseconds / 1e6)
                     )
        logger.debug("*" * 10 + " end of permutation " + "*" * 10)
        
        for i in res:
            if i in self.permutation_unique:
                find_index = self.permutation_unique.index(i)
                self.permutation_count[find_index] += 1
            else:
                self.permutation_unique.append(i)
                self.permutation_count.append(1)
    
    
    def compute_entropy(self):
        self.permutation_entropy_val = entropy(self.permutation_count, base=10)
    
    
    def get_permutation_entropy(self):
        logger.info("*" * 10 + " begin of compute permutation entropy " + "*" * 10)
        
        start_time = datetime.now()
        self.permutation()
        self.compute_entropy()
        
        end_time = datetime.now()
        logger.info('>> It takes %.3f seconds to compute permutation entropy.' %
                    ((end_time - start_time).seconds + (end_time - start_time).microseconds / 1e6)
                    )
        logger.info("*" * 10 + " end of compute permutation entropy " + "*" * 10)


def get_entropy(l1, en_type='sample', **kw):
    if (en_type.lower() == 'sample') or (en_type.lower() == 'sampen') or (en_type.lower() == 'sampentropy'):
        ## sample entropy
        Q_ref = Entropy(l1, min_dist=kw['min_dist'])
        Q_ref.get_samp_entropy()
        return Q_ref.samp_entropy_val
    elif (en_type.lower() == 'approximate') or (en_type.lower() == 'apen') or (en_type.lower() == 'apentropy'):
        ## approximate entropy
        Q_ref = Entropy(l1, min_dist=kw['min_dist'])
        Q_ref.get_ap_entropy()
        return Q_ref.ap_entropy_val
    elif (en_type.lower() == 'permutation') or (en_type.lower() == 'peen') or (en_type.lower() == 'peentropy'):
        ## permutation entropy
        Q_ref = Entropy(l1)
        Q_ref.get_permutation_entropy()
        return Q_ref.permutation_entropy_val
    else:
        raise ValueError("Unknown entropy type [%s]!" % en_type)
