# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       Entropy.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-07-13 10:47
@version    0.0.1.20180713
--------------------------------------
Approximate Entropy
计算序列的各类熵值:
    - 样本熵 - Sample entropy
    - 近似熵 - Approximate entropy
    - 排列熵 - Permutation entropy

Reference
https://en.wikipedia.org/wiki/Sample_entropy
https://en.wikipedia.org/wiki/Approximate_entropy#cite_note-Pincus21991-23


"""


from scipy.spatial.distance import pdist, squareform
from scipy.stats import entropy
from numpy import log, std
from datetime import datetime
import logging

logger = logging.getLogger('ApEntropy')


class Entropy(object):
    """
    通常选择参数m=2或m=3；r的选择在很大程度上取决于实际应用场景，通常选择r=0.2∗std，其中std表示原时间序列的标准差.
    """
    
    
    def __init__(self, values=[], n_cols=None, min_dist=None, dist_type='chebychev'):
        self.values = values
        self.length = len(values)
        self.n_cols = 3 if n_cols is None else n_cols
        self.n_rows = None
        
        self.std = std(self.values)
        ## minimal distance to define a neighbour set
        ## set to 2*std by default
        self.min_dist = min_dist if min_dist is not None else 2*self.std
        
        self.dist_type = dist_type  ## distance type

        self.sample_entropy_val = None
        self.approximate_entropy_val = None
        
        self.permutations = None
        self.permutation_unique = []
        self.permutation_count = []
        self.permutation_entropy_val = None
    
    
    def reshape(self, n_cols, n_rows=None):
        """
        transform the values list into a 2-dim matrix n_cols×n_rows
        :param n_cols: number of columns
        :param n_rows: optional, set to be [N - n_cols + 1] by default
                    number of rows
        :return: matrix of values
        """
        if n_rows is None:
            n_rows = self.length - n_cols + 1
        
        self.n_rows = n_rows
        value_matrix = [
            self.values[i:i + n_cols] for i in range(n_rows)
        ]
        
        return value_matrix
    
    '''
    ## Approximate entropy
    '''
    def _phi1(self, m, r, dist_type='chebychev'):
        """
        φ1 value defined when compute approximate entropy
        :param m:int    number of dimension in each window list
        :param r:float  minimal distance between vectors
        :param dist_type:str   type of distance
                        all distance supported in scipy.spatial.distance
        :return:float   phi value
        """
        value_matrix = self.reshape(n_cols=m)
        
        N = self.n_rows
        
        logger.debug(">> calculating distance between {} vectors with type [{}].".format(N, dist_type.upper()))
        dist_matrix = squareform(pdist(value_matrix, dist_type))
        
        ## define the neighbour set of Xi whose distance < r
        appr_nb = [sum([1 if d < r else 0 for d in row]) / N for
                   row in dist_matrix]
        
        phi = sum([log(c) for c in appr_nb]) / N
        
        return phi
    
    
    def approximate_entropy(self, m: int, r: float, dist_type: str) -> float:
        """
        compute approximate entropy
        :param m:
        :param r:
        :param dist_type:
        :return:
        """
        return self._phi1(m, r, dist_type) - self._phi1(m + 1, r, dist_type)
    
    
    def get_ap_entropy(self):
        logger.info("*" * 10 + " begin of compute approximate entropy " + "*" * 10)

        start_time = datetime.now()

        ap_entropy = self.approximate_entropy(self.n_cols, self.min_dist, self.dist_type)
        self.approximate_entropy_val = ap_entropy
        
        end_time = datetime.now()
        logger.info('>> It takes %.3f seconds to compute approximate entropy.' %
                    ((end_time - start_time).seconds + (end_time - start_time).microseconds / 1e6)
                    )
        logger.info("*" * 10 + " end of compute approximate entropy " + "*" * 10)

    '''
    ## permutation entropy
    '''
    def _phi2(self, m, r, dist_type='chebychev', case='approximate'):
        """
        φ1 value defined when compute sample entropy
        :param m:int    number of dimension in each window list
        :param r:float  minimal distance between vectors
        :param dist_type:str   type of distance
                        all distance supported in scipy.spatial.distance
        :return:float   phi value
        """
        value_matrix = self.reshape(n_cols=m)
    
        N = self.n_rows
    
        logger.debug(">> calculating distance between {} vectors with type [{}].".format(N, dist_type.upper()))
        dist_matrix = squareform(pdist(value_matrix, dist_type))
    
        appr_nb = [sum([1 if d < r else 0 for d in row]) / N for
                   row in dist_matrix]
        phi = sum(appr_nb) / N
    
        return phi


    def sample_entropy(self, m: int, r: float, dist_type: str) -> float:
        """
        compute sample entropy of a list
        :param m:
        :param r:
        :param dist_type:
        :return:
        """
        return log(self._phi2(m, r, dist_type, case='sample')
                   / self._phi2(m + 1, r, dist_type, case='sample'))
    
        
    
    
    def get_samp_entropy(self):
        logger.info("*" * 10 + " begin of compute sample entropy " + "*" * 10)
        
        start_time = datetime.now()

        self.sample_entropy_val = self.sample_entropy(self.n_cols, self.min_dist, self.dist_type)

        end_time = datetime.now()
        logger.info('>> It takes %.3f seconds to compute sample entropy.' %
                    ((end_time - start_time).seconds + (end_time - start_time).microseconds / 1e6)
                    )
        logger.info("*" * 10 + " end of compute sample entropy " + "*" * 10)
    
    
    ##########################
    ## permutation entropy  ##
    ##########################
    def index_sort(self, l1):
        """
        对l1元素排序, 并输出对应的下标
        :param l1:
        :return:
        """
        res = sorted(enumerate(l1), key=lambda x: x[1])
        res1 = [i[0] for i in res]
        
        #logger.debug(">>> sort list: " + str(l1))
        #logger.debug(">>> index after sorting: " + str(res1))
        
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
    
    
    def permutation_entropy(self):
        self.permutation_entropy_val = entropy(self.permutation_count, base=10)
    
    
    def get_permutation_entropy(self):
        logger.info("*" * 10 + " begin of compute permutation entropy " + "*" * 10)
        
        start_time = datetime.now()
        self.permutation()
        self.permutation_entropy()
        
        end_time = datetime.now()
        logger.info('>> It takes %.3f seconds to compute permutation entropy.' %
                    ((end_time - start_time).seconds + (end_time - start_time).microseconds / 1e6)
                    )
        logger.info("*" * 10 + " end of compute permutation entropy " + "*" * 10)


def get_entropy(l1, en_type='sample', **kw):
    if (en_type.lower() == 'sample') or (en_type.lower() == 'sampen') or (en_type.lower() == 'sampentropy'):
        ## sample entropy
        Q_ref = Entropy(l1, **kw)
        Q_ref.get_samp_entropy()
        return Q_ref.sample_entropy_val
    elif (en_type.lower() == 'approximate') or (en_type.lower() == 'apen') or (en_type.lower() == 'apentropy'):
        ## approximate entropy
        Q_ref = Entropy(l1, **kw)
        Q_ref.get_ap_entropy()
        return Q_ref.approximate_entropy_val
    elif (en_type.lower() == 'permutation') or (en_type.lower() == 'peen') or (en_type.lower() == 'peentropy'):
        ## permutation entropy
        Q_ref = Entropy(l1, **kw)
        Q_ref.get_permutation_entropy()
        return Q_ref.permutation_entropy_val
    else:
        raise ValueError("Unknown entropy type [%s]!" % en_type)
