#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:08:14 2019

@author: gabrielpundrich


#SC 13D/A	

"""


#SET UP MACROS
 
#path to your own code (where this file is located)
path_code = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/finance_accounting_data_science/"

#path to sec index, first time leave it empty
path_sec  = path_code+"/index_SEC/"

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
from bs4 import BeautifulSoup
import sys
import pickle
import os

from  tools.tools_scrapping import *


#RUN THIS JUST FIRST TIME

#get index files from SEC EDGAR, you should provide the folder to download and starting year
import edgar
edgar.download_index(path_sec, 1994)




file_name_pickle_SC13D = get_index("SC 13D",path_sec,path_code+"/pickles",0)
print("Got a new pickle name!", file_name_pickle_SC13D)

#filter just DEF14A or 10K files, etc
file_name_pickle = get_index("DEF 14A",path_sec,path_code,0)
file_name_pickle_10k = get_index("10-K",path_sec,path_code,0)
file_name_pickle_10kALL = get_index("10-K",path_sec,path_code,1)


