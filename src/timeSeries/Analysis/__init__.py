# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       __init__.py.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-07-11 13:27
@version    0.0.1.20180711
--------------------------------------
<enter description here>
"""

import sys
from .Permutation_entropy import *
import logging

logging.basicConfig(filename='./logs/datageek.log',
                    format='%(asctime)s\t%(filename)s[%(lineno)d]\t%(levelname)s\t%(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S]',
                    level=logging.DEBUG)


