#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:23:41 2019

@author: Gabriel Pündrich

Bocconi University
"""
import os
import sys
import pickle
import pandas as pd
import re
from itertools import chain
import math

def get_index(file_type,sec_index_files_path,path_code,greedy=0):
    
    count=0
    path_sec = sec_index_files_path
    df = pd.DataFrame()

    list_files = os.listdir(path_sec)
    #list_files = ['1999-QTR3.tsv','1999-QTR4.tsv']
    
    #create a for to iterate through all files in the folder of sec
    for file_sec in list_files:
        
        print ("filtering" + file_sec)
        count  = count+1
        try:
            #get index file
            sec_index = pd.read_csv(path_sec + file_sec, sep='|',header=None) 
            
            sec_index.head(3)
            sec_index.columns
            
            #set column names to file
            sec_index.columns = ['cik', 'firm_name','file_type','report_date','file_url_txt','file_url_html']
            
            #how our data looks like?
            sec_index.shape
            
            #show all types of files in the index
            sec_index.file_type.unique()
            
            #create empty df to aggregate all filtered dataframes
            sec_index_aggregated = pd.DataFrame()
            #greedy takes all files similar to the start as 10-k 10-k14 10-K5XX
            if greedy:
                
                #get all similar columns and put in "alike_file_types"
                alike_file_types = []
                for columns_alike in sec_index.file_type.unique():
                    if file_type in columns_alike:
                        alike_file_types.append(columns_alike)

                #filter all columns with file types alike
                for file_type_column in alike_file_types:
                    print (file_type_column)
                
                    sec_index_ite = sec_index.drop(sec_index[sec_index.file_type != file_type_column].index)
                    sec_index_aggregated = sec_index_aggregated.append(sec_index_ite)
               
                
                sec_index=  sec_index_aggregated
                file_type_clean=file_type + "_greedy"
#, ignore_index=True

            else:
                #restrict data only to "def14A" filetypes, you delete because you want to clean your ram as much as you can (drawback of pandas and R).
                sec_index = sec_index.drop(sec_index[sec_index.file_type != file_type].index)
                file_type_clean=file_type
            #what shape we have now?
            sec_index.shape
            
            #save pickle file
        
            
            outputFilename = str("filtered_index " + file_type_clean + ".pkl")
            df = df.append(sec_index)
            
            #pickle.dump( sec_index, open( path_code +  outputFilename, "ab" ) )
            
        except:
            print ("Error when trying year" + str(file_sec) + " " + str(sys.exc_info()[0]))
            
    pickle.dump( df, open( path_code +  outputFilename, "ab" ) )

            
    return outputFilename
    




def cleanhtml(raw_html):

    cleantext = re.sub(re.compile('\n'), ' ', raw_html)
    
    
    #clean tags
    cleantext = re.sub(re.compile('<.*?>'), ' ', cleantext)
   
    #clean spaces
    cleantext = re.sub(re.compile('&nbsp;'), ' ', cleantext)
    
    #clean general noise
    #cleantext = re.sub(re.compile('&.*?;'), ' ', cleantext)

    #remove empty spaces
    cleantext = re.sub(re.compile(' +'), ' ', cleantext)

#    cleantext = re.sub(re.compile('&#160;'), ' ', cleantext)

        
    return cleantext



def cleanjusthtml(raw_html):    
    #clean tags
    cleantext = re.sub(re.compile('<.*?>'), ' ', raw_html)
    cleantext = re.sub(re.compile(' +'), ' ', cleantext)
    cleantext = re.sub(re.compile('\n'), ' ', raw_html)
    cleantext = re.sub(re.compile('&nbsp;'), ' ', cleantext)
    return cleantext




def cleanjustspace(raw_html):    
    #clean tags
    cleantext = re.sub(re.compile(' +'), ' ', raw_html)
    cleantext = re.sub(re.compile('\n'), ' ', raw_html)
    cleantext = re.sub(re.compile('&nbsp;'), ' ', cleantext)
    return cleantext


# reorder columns
def set_column_sequence(dataframe, seq, front=True):
    '''Takes a dataframe and a subsequence of its columns,
       returns dataframe with seq as first columns if "front" is True,
       and seq as last columns if "front" is False.
    '''
    cols = seq[:] # copy so we don't mutate seq
    for x in dataframe.columns:
        if x not in cols:
            if front: #we want "seq" to be in the front
                #so append current column to the end of the list
                cols.append(x)
            else:
                #we want "seq" to be last, so insert this
                #column in the front of the new column list
                #"cols" we are building:
                cols.insert(0, x)
    return dataframe[cols]

# select columns containing a word and return the position                       
def search_item_list(list_names,word_searched):
    pos_name_col = 0
    for name_col in list_names:
        if name_col == word_searched:
            return pos_name_col
        pos_name_col = pos_name_col+1
    return False

#change order of one element in a list
def rearrange_list(original_position,new_position,size_column):
    #original list order
    original_order = []
    for pos_list in range(0,size_column):
        original_order.append(pos_list)
        
                               
    #Put age in column 4
    new_order = []
    for pos_list in original_order:
        if pos_list==new_position:
            new_order.append(original_position)
        
        if pos_list==original_position:
            #remove the old record for position age
            pass
        else:
            new_order.append(pos_list)

    return new_order
    
    
#this function rearrange the dataframe columns into the ones requested 
def align_columns(new_column_position,old_dataframe,name_column,size_column):
    #search for any element in the list with the word age so we can re-order and leave in the same column as other files that may leave age in different column    
    #configure the new position of the "age" or any variable would like to reorganize
    
    cols = old_dataframe.columns.values
    position_column = (search_item_list(cols,name_column))
    
    if position_column!=new_column_position and position_column :
        print ("reorganizing")
        #original_position,new_position,size_column
        new_order = rearrange_list(position_column,new_column_position,size_column)
        
        #reorganize list
        cols2 = [cols[i] for i in new_order]
    
        #reorganize columns on dataframe                              
        old_dataframe_reorganized = set_column_sequence(old_dataframe, cols2)

        return old_dataframe_reorganized
    else:
        return old_dataframe
    
    
    
def prepend_text(file, text, after=None):
    ''' Prepend file with given raw text '''
    f_read = open(file, 'r')
    buff = f_read.read()
    f_read.close()
    f_write = open(file, 'w')
    inject_pos = 0
    if after:
        pattern = after
        inject_pos = buff.find(pattern)+len(pattern)
    f_write.write(buff[:inject_pos] + str(text) + buff[inject_pos:])
    f_write.close()

    
#flat a multidimensional list in a 1D
def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)



def getNumbers(str): 
    array = re.findall('\d*\.?\d+',str)

    #array = re.findall(r'[0-9]+', str) 
    return array 



#check if age is present
def has_age(text):
    
    #eliminate all commas
    text = re.sub(re.compile(','), '', text)
    
    numbers = getNumbers(text)
    for eachnumber in numbers:
        #print( eachnumber)
        #print (type(eachnumber))
        eachnumber = float(eachnumber)
        frac, whole = math.modf(eachnumber)
        
        if (eachnumber<=100 and eachnumber>=20) and frac==0:
            #print (eachnumber)
            #print ("oi")
        
            return True
    return False
        



def build_index_sec(start_year,end_period,path_sec):
    import traceback
    try:
        #Download SEC files
            
#        start_year = 1996
#        end_period = 1998
##        
#        path_sec  = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/scraper_sec/build_sec_index/index_SEC/"
##        
#        
        import os
        
        
        
        if not os.path.exists(path_sec):
            os.makedirs(path_sec)
        
        
        for each_year in range(start_year,end_period):
            print(each_year)
            for each_quarter in range(1,5):
                print(each_quarter)
                
                
                
                
                sec_url = "https://www.sec.gov/Archives/edgar/full-index/"
                full_adress = sec_url + str(each_year) + "/QTR"+str(each_quarter) + "/master.zip" 
        
                name_quarter_file_zip = str(each_year)+"-QTR"+str(each_quarter)+".zip"
                name_quarter_file_tsv = str(each_year)+"-QTR"+str(each_quarter)+".tsv"
                
                try:
                    from six.moves import urllib
                    urllib.request.urlretrieve(full_adress, path_sec+name_quarter_file_zip)
                
                    
                    path_to_zip_file = path_sec+name_quarter_file_zip
                    
                    
                    import zipfile
                    with zipfile.ZipFile(path_to_zip_file,"r") as zip_ref:
                        zip_ref.extractall(path_sec)
                    
                    
                    os.rename(path_sec+"master.idx", path_sec+name_quarter_file_tsv) 
                    
                    
                    #skiprows=1 will skip first line and try to read from second line
                    df = pd.read_csv(path_sec+name_quarter_file_tsv, skiprows=9, sep='|',encoding = "ISO-8859-1" )
                    df.columns

                    #add a column with url
                    df["url"] =  df["Filename"].replace('.txt','-index.html',regex=True)
    
                    #clean first rows
                    new_df = df.iloc[1:]
                    new_df.head()
                    df.head()
                    
                    
                    
                    
                    new_df.to_csv(path_sec+name_quarter_file_tsv, sep='|',index=False, header=False)
                    
                    print("Download "+ name_quarter_file_tsv)
                except:
                    print("Could not download for "+str(each_year))
    except:
        print(traceback.format_exc())
    
       
    try:
        #Clean ZIP files
        test = os.listdir(path_sec)
        
        for item in test:
            if item.endswith(".zip"):
                os.remove(os.path.join(dir_name, item))
                
                
    except:
       print("Warning, coult not clean all zip files") 
     
   








#
#
##GET LIST OF FIRMS THAT WE ARE INTERESTED IN COLLECTING DATA
#df_cik_firms = pd.read_csv(path_input + "collect_mda.csv", sep=',',header=0) 
#
##get slice to calculate year
#year_report =  (sec_index["report_date"].str[:4])
#
#sec_index['Year'] = year_report
#
#df_cik_firms.columns
#df_cik_firms.dtypes
#
#sec_index.columns
#sec_index.dtypes
#
##change datatype of pandas
#sec_index['Year'] = sec_index['Year'].apply(lambda x: int(x))
#
##merge pandas: inner - intersection, outer - n:n, left (master) and right (using)
## left join in python
##it has a larger number of rows than left df because of duplicates on using data: df.merge(df2.drop_duplicates(subset=['A']), how='left')
#combined = pd.merge(sec_index, df_cik_firms, on=['cik'], how='left')
#
#
##clean, get only documents where you have SDC data, i.e., not missing year
#df_clean = combined[pd.notnull(combined['CEO_TARGET'])]
##listtest = df_clean.cik.unique()
#
#df_clean.columns
#
##get latest year - year before M&A
#df_clean = df_clean.sort_values(['cik', 'Year'],ascending=[True, True])
#df_clean.cik.unique()
#df_clean = df_clean.drop_duplicates(subset='cik', keep="last")


