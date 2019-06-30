#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 14:08:14 2019

@author: gabrielpundrich
"""


#SET UP MACROS

###########################################################################################################
#path to your enviroment "/"
path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
###########################################################################################################


#path to your own code (where this file is located)
path_code = path_env+"/scraper_sec/age_ceo/"

#path where your extracted variables will be put, first time should be empty 
path_output = path_code+"../downloaded_files/age_ceo/"


#input files to the code
path_input = path_code+"/../input/"


url_sec = 'https://www.sec.gov/Archives/'



import sys
sys.path.append(path_env)

import string
import pandas as pd
import numpy as np
import seaborn as sbs
import matplotlib.pyplot as plt
from nltk import *
import urllib
from bs4 import BeautifulSoup

import csv
import time
from bs4 import BeautifulSoup
import sys
import pickle
import os

from  tools.pundrich_sctools import *
import os


file_name_pickle  = "../build_sec_index/pickles/filtered_index DEF 14A.pkl"

#LOAD PICKLE FILE WITH FILTERED DEF 14A
sec_index = pickle.load( open(path_code + file_name_pickle, "rb" ) )
sec_index.columns

#GET LIST OF FIRMS THAT WE ARE INTERESTED IN COLLECTING DATA
df_cik_firms = pd.read_csv(path_input + "find_ceo_age.csv", sep=',',header=0) 

#get slice to calculate year
year_report =  (sec_index["report_date"].str[:4])

sec_index['Year'] = year_report

df_cik_firms.columns
df_cik_firms.dtypes

sec_index.columns
sec_index.dtypes

#change datatype of pandas
sec_index['Year'] = sec_index['Year'].apply(lambda x: int(x))

#merge pandas: inner - intersection, outer - n:n, left (master) and right (using)
# left join in python
#it has a larger number of rows than left df because of duplicates on using data: df.merge(df2.drop_duplicates(subset=['A']), how='left')
combined = pd.merge(sec_index, df_cik_firms, on=['cik'], how='left')


#clean, get only documents where you have SDC data, i.e., not missing year
df_clean = combined[pd.notnull(combined['CEO_TARGET'])]
#listtest = df_clean.cik.unique()

df_clean.columns

#get latest year - year before M&A
df_clean = df_clean.sort_values(['cik', 'Year'],ascending=[True, True])
df_clean.cik.unique()
df_clean = df_clean.drop_duplicates(subset='cik', keep="last")


#restart index
df_clean = df_clean.reset_index(drop=True)


for index, row in df_clean.iterrows():
    #get text and html urls from sec
    url_txt = (url_sec + row['file_url_txt'])
    url_html = (url_sec + row['file_url_html'])           
    ceo_target = row['CEO_TARGET'] 
    #print (url_html)
    
    first_word_search = ceo_target
    second_word_search = "age"

    try: 
        year = int(row['Year'])
        
    except:
        print("Warning: couldnt convert year to int" + index)
        print(row)
    


    #for debug
    if year>=2004:

        #request url from sec server
        response = urllib.request.urlopen(url_txt)
        
        #your response, i.e., webpage with form, is on this variable
        full_text =response.read().decode('utf-8').lower()
        
        #translate html into soup
        soup = BeautifulSoup(full_text,'lxml')
        
        
        
        #print(soup.prettify())
        
        
        
        #Each level is a refiner in the search, boolean would be an "AND"
        #first filter, check if there is the word 
        file_num = 0
        for tag_level1 in soup.find_all(text=re.compile(first_word_search)):
            #print (tag.findParent('table'))
            table_level1 = tag_level1.findParent('table')
            
            #second filter, check if there is the word "age" for list of members, do the same later with salary so can get compensation
            if table_level1!=None:
                for tag_level2 in table_level1.find_all(text=re.compile(second_word_search)):
                    table_level2 = tag_level2.findParent('table')
    
                    if file_num>0:
                        break
    
                    if table_level2!=None:
                        print("found a table!")
                        print (row['Year'])
                        
                        name_file_output = str(row['cik']) + "_" + str(row['report_date'])  + str(file_num) +".htm"
                        text_file = open(path_output + "/tables/" +   name_file_output, "w")
                        text_file.write(str(table_level2))
                        text_file.close()
                        file_num = file_num+1
                        
                        
                        table_level2_output = str(table_level2)
                        
                        try:
                        
                            soup_level2 = BeautifulSoup(table_level2_output, "html.parser")
                            table_level2 = soup_level2.find('table')
                            table_rows_level2 = table_level2.find_all('tr')
                            
                            
                            #transform table just captured into a dataframe so we can manipulate the data extracted
                            res = []
                            for tr in table_rows_level2:
                                td = tr.find_all('td')
                                row_local = [tr.text.strip() for tr in td if tr.text.strip()]
                                
                                #clean each element, each cell
                                for each_row_local in range(0,len(row_local)): 
                                    row_local[each_row_local] = re.sub(re.compile('\n'), ' ', row_local[each_row_local])
                                
                                if row_local:
                                    
                                    row_local.insert(0,str(row['cik']))
                                    row_local.insert(1,str(name_file_output))
                                    row_local.insert(2,str(row['report_date']))
                                    row_local.insert(2,str(index))
                            
                                    #set columns equal to 15, and reshape all lists have same size
                                    size_column = 30
                                    row_local.extend(['']*(size_column-len(row_local)))
                                    
                                    res.append(row_local)
                                            
                            #transform into a dataframe
                            df_output = pd.DataFrame(res[1:],columns=res[0])
                            
                            
                            #search for any element in the list with the word age so we can re-order and leave in the same column as other files that may leave age in different column    
                            #configure the new position of the "age" or any variable would like to reorganize
                            #position_column_age = 3
                            #df_output_reorganized = align_columns(3,df_output,"age",size_column)    
                            
                            
                            df_output.to_csv(path_output +  'tables_age.csv', mode='a', header=False)
                            
                        except:
                            print ("Unexpected error: " + str(sys.exc_info()[1]) + " " +  str(name_file_output))
                            







