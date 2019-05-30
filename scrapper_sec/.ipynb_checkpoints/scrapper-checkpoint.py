#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:08:14 2019

@author: gabrielpundrich


#SC 13D/A	

"""


#SET UP MACROS
#path to your own code (where this file is located)
path_code = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/finance_accounting_data_science/scrapper_sec/"

#path where your extracted variables will be put, first time should be empty 
path_output = path_code+"/downloaded_files/"

#path for no html files
path_output_no_html = path_code+"/scrapper_sec/tables_compensation/no_html/"

#input files to the code
path_input = path_code+"/input/"


url_sec = 'https://www.sec.gov/Archives/'


first_word_search = 'chief financial officer'
second_word_search = first_word_search
#second_word_search = '\Aage$'


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
import os


#select the pickle file

file_name_pickle  = "../pickles/filtered_index SC 13D.pkl"

#LOAD PICKLE FILE WITH FILTERED DEF 14A
sec_index = pickle.load( open(path_code + file_name_pickle, "rb" ) )
sec_index.file_type.unique()
sec_index.columns

#GET LIST OF FIRMS THAT WE ARE INTERESTED IN COLLECTING DATA
df_cik_firms = pd.read_csv(path_input + "ciks-table.csv", sep=',',header=0) 


df_cik_firms.columns
df_cik_firms.dtypes
df_cik_firms.cik.unique



save_full_file=0

#merge pandas: inner - intersection, outer - n:n, left (master) and right (using)
# left join vs right in python
combined = pd.merge(sec_index, df_cik_firms, on=['cik'], how='right')
combined.cik.unique
combined.columns



for index, row in combined.iterrows():
    
    try: 
        #get text and html urls from sec
        url_txt = (url_sec + row['file_url_txt'])
        url_html = (url_sec + row['file_url_html'])   
        report_date =  (row['report_date'])          
        #print (url_html)
    
    #ignore errors: careful!
    except:
        True
    
    
    #request url from sec server
    response = urllib.request.urlopen(url_txt)
    
    #your response, i.e., webpage with form, is on this variable
    full_text =response.read().decode('utf-8').lower()
    
    
    if save_full_file:
        name_file_output =  str(row['cik'])+ "_"+ str(report_date)  + ".html"
        text_file = open( path_output  + "unclean/" +   name_file_output, "w")
        text_file.write(str(full_text))
        text_file.close()
        
        myList = [item for item in full_text.split('\n')]
        newString = ' '.join(myList)

   
    
    
    



    clean_text = cleanhtml(newString)
    sc_keywords = ["cooperation agreement","exchange agreement","investment agreement","investment contract","investor agreement","investor contract","investor rights","shareholder agreement","shareholder contract","stockholder agreement","stockholder contract","support agreement"]    

    #search for a SC
    
    for keyword  in sc_keywords:
        if keyword in clean_text:
            print ("FOUND a SC! The keyword is ", keyword)
            name_file_output = str(row['cik'])+ "_"+ str(report_date)  + "_clean" + ".html"
            text_file = open(path_output  + "clean/" +   name_file_output, "w")
            text_file.write(str(clean_text))
            text_file.close()



