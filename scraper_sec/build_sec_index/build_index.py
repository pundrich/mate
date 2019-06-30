#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:08:14 2019

@author: gabrielpundrich


#SC 13D/A	

"""


#SET UP MACROS
 
#path to your own code (where this file is located)
###############################################################################
path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
###############################################################################

path_code = path_env


#path_sec  = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/scraper_sec/build_sec_index/index_SEC/"

#path to sec index, first time leave it empty
path_sec  = path_code+"/scraper_sec/build_sec_index/index_SEC/"
path_pickle = path_code+"/scraper_sec/build_sec_index/pickles/"
url_sec = 'https://www.sec.gov/Archives/'


import sys
sys.path.append(path_code)

import string
import pandas as pd
import numpy as np
import seaborn as sbs
import matplotlib.pyplot as plt
from nltk import *
import urllib
import html2text
from bs4 import BeautifulSoup
import re
import csv
import time
import sys
import pickle
import os

from  tools.pundrich_sctools import *

#For teaching reasons... check this code
#get index files from SEC EDGAR, you should provide the folder to download and starting year
#import edgar

#Using old library
#edgar.download_index(path_sec,1994)

#Using Pundrich's lib: this library is beta... please report any bugs.
#build_index_sec(start_year,end_period,path_sec)

build_index_sec(1992,2020,path_sec)

file_name_pickle = get_index("DEF 14A",path_sec,path_pickle)
print("Got a new pickle name!", file_name_pickle)

file_name_pickle = get_index("10-K",path_sec,path_pickle)
print("Got a new pickle name!", file_name_pickle)

file_name_pickle = get_index("10-Q",path_sec,path_pickle)
print("Got a new pickle name!", file_name_pickle)



"""""
Note: You can choose after creating all pickles to remove the files on path_sec
and save up to 2.5Gb
"""""


