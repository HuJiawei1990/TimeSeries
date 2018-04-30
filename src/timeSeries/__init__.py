# C:\lib\Python\Python36 python.exe
# -*- coding:utf-8 -*-
"""
@file       __init__.py.py
@project    TimeSeries
--------------------------------------
@author     hjw
@date       2018-04-25 14:13
@version    0.0.1.20180425
--------------------------------------
<enter description here>
"""

import sys
from .timeSeries import *
from .Analysis import *
import logging

logging.basicConfig(filename='../logs/datageek.log',
                    format='%(asctime)s\t%(filename)s[%(lineno)d]\t%(levelname)s\t%(message)s',
                    datefmt='[%Y-%m_%d %H:%M:%S]',
                    level=logging.INFO)




