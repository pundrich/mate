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
    import html2text
    from bs4 import BeautifulSoup
    import re
    import csv
    import time
    from bs4 import BeautifulSoup
    import sys
    import pickle
    import os
    
    from tools.tools_scraping import *
    import os
    
    
    
    file_name_pickle  = "../build_sec_index/pickles/filtered_index DEF 14A.pkl"
    
    #LOAD PICKLE FILE WITH FILTERED DEF 14A
    sec_index = pickle.load( open(path_code + file_name_pickle, "rb" ) )
    sec_index.file_type.unique()
    
    
    sec_index.columns
    
    
    
    #GET LIST OF FIRMS THAT WE ARE INTERESTED IN COLLECTING DATA
    #get index file
    df_cik_firms = pd.read_csv(path_input + "find_ceo_age_text.csv", sep=',',header=0) 
    
    
    
    
    #get slice to calculate year
    year_report =  (sec_index["report_date"].str[:4])
    
    sec_index['Year'] = year_report
    
    df_cik_firms.columns
    df_cik_firms.dtypes
    df_cik_firms.cik.unique
    
    
    #change datatype of pandas
    sec_index['Year'] = sec_index['Year'].apply(lambda x: int(x))
    
    #merge pandas: inner - intersection, outer - n:n, left (master) and right (using)
    # left join in python
    #it has a larger number of rows than left df because of duplicates on using data: df.merge(df2.drop_duplicates(subset=['A']), how='left')
    
    
    combined = pd.merge(sec_index, df_cik_firms, on=['cik'], how='left')
    combined.cik.unique
    
    
    #clean, get only documents where you have SDC data, i.e., not missing year
    df_clean = combined[pd.notnull(combined['year_ann'])]
    
    
    
    #listtest = df_clean.cik.unique()
    
    df_clean.cik.unique
    df_clean.columns
    combined.cik.unique()
    
    #sort by year
    df_clean = df_clean.sort_values(['cik', 'Year'],ascending=[True, True])
    df_clean.cik.unique()
    
    
    df_clean = df_clean.drop_duplicates(subset='cik', keep="last")
    
    #restart index
    df_clean = df_clean.reset_index(drop=True)
    df_clean.file_type.unique()
    df_clean.dtypes
    
    ceo_name_list = []
    for index, row in df_clean.iterrows():
    
        #get text and html urls from sec
        url_txt = (url_sec + row['file_url_txt'])
        url_html = (url_sec + row['file_url_html'])           
        ceo_target = row['surname']
    
        try: 
            year = int(row['Year'])
            
        except:
            print("Warning: couldnt convert year to int" + index)
            print(row)
        
        
        
        #request url from sec server
        response = urllib.request.urlopen(url_txt)
        
        #your response, i.e., webpage with form, is on this variable
        full_text =response.read().decode('utf-8').lower()
        
    #    name_file_output = str(row['cik'])+ "_"+ str(year) + "_"+ ceo_target +"_"+ ".html"
    #    text_file = open(path_output  +   name_file_output, "w")
    #    text_file.write(str(full_text))
    #    text_file.close()
        
        myList = [item for item in full_text.split('\n')]
        newString = ' '.join(myList)
    
        clean_text = cleanjusthtml(newString)
    
    #Test: uncomment and check file for new patterns!
        
    #    name_file_output = str(row['cik'])+"_"+str(year)+"_clean.html"
    #    text_file = open(path_output  +   name_file_output, "w")
    #    text_file.write(str(clean_text))
    #    text_file.close()
    #
    #
    #    name_file_output2 = str(row['cik'])+"_"+str(year)+"_html_clean.html"
    #    text_file = open(path_output  +   name_file_output2, "w")
    #    text_file.write(str(full_text))
    #    text_file.close()
    
    
    
        ceo_name_list = []
        ceo_name_list.append(str(url_html))            
        ceo_name_list.append(ceo_target)

    
    
        
     
    #    r1 = re.findall(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,5} years old (?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,5}", clean_text)
        r1 = re.findall(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,5} age (?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,3}", clean_text)
        #print (r1)
    
        r1 = re.findall(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,0}"+ ceo_target+ "(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,10}", clean_text)
    
        if r1:
            
            for chunk in r1:
                
                #Another pattern            
                #if (ceo_target in chunk) and ("born" in chunk)              and (("$" not in chunk) and ("%" not in chunk) and ("share" not in chunk)  and ("/" not in chunk) ):
    
                if (ceo_target in chunk) and (" age " in chunk):
                    print(chunk)
            
                    found = str(chunk)
            
                    ceo_name_list = []
                    
                  
                    ceo_name_list.append(str(row['cik']))
                    ceo_name_list.append(str(year))
                    ceo_name_list.append(str(url_html))            
                    ceo_name_list.append(ceo_target)
                    ceo_name_list.append(str(found))
                    
                    print("FOUND the age" + found)
                    
                    with open(path_output+'ceo_age_text.csv', 'a') as writeFile:
                        writer = csv.writer(writeFile)
                        writer.writerows([ceo_name_list])
                    writeFile.close()
    
    
