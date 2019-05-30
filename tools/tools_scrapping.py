#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 10:23:41 2019

@author: gabrielpundrich
"""
import os
import sys
import pickle
import pandas as pd
import re
from itertools import chain
import math

def get_index(file_type,sec_index_files_path,path_code,greedy):
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
        



