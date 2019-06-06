#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 06:46:11 2019

@author: gabrielpundrich
"""
import pandas as pd



###########################################################################################################
#path to your enviroment "/"
path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
###########################################################################################################

path_code = path_env + "/python101/"

# List of lists
students = [ ['Jack', 34, 'Australia'] ,
['Peter', 30, 'Brazil' ] ,
['James', 16, 'USA'] ]

# List of lists2
students2 = [ ['Peter', 23, 'UK'] ,
['Pietro', 20, 'Italy' ] ,
['Juan', 44, 'Australia'] ]


dfObj = pd.DataFrame(students) 
dfObj = pd.DataFrame(students, columns = ['Name' , 'Age', 'Country'], index=['a', 'b', 'c'])
dfObj2 = pd.DataFrame(students2, columns = ['Name' , 'Age', 'Country'])

dfObj3 = dfObj['Age']+dfObj2['Age']


dfObj.columns

dfObj.to_csv(path_code+'/output.csv')





#########

countries = [ ['Australia', 20] ,
['Brazil', 200 ] ,
['UK', 66],
['Italy', 60],
['USA', 327] ]

df_Countries = pd.DataFrame(countries, columns = ['Country','Population'])

#concat
concatList = pd.concat([dfObj,dfObj2])
    

mergeDfs = pd.merge(concatList,df_Countries, on=['Country'], how='left')

mergeDfs.Country.unique

#remove column
del mergeDfs['Country']

mergeDfs['Age*Population'] = mergeDfs['Age']*mergeDfs['Population']
