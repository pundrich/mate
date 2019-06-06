#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 06:46:11 2019

@author: gabrielpundrich
"""
import pandas as pd
from tool.install_package import *


###########################################################################################################
#path to your enviroment "/"
path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
###########################################################################################################



path_code = path_env + "/python101/"





# List of lists
students = [ ['Jack', 34, 'Australia'] ,['Peter', 30, 'Brazil' ] ,['James', 16, 'USA'] ]

for each_row in students:
    print(each_row)
    
    for  each_cell in each_row:
        print (each_cell)


# List of lists2
students2 = [ ['Peter', 23, 'UK'] ,['Pietro', 20, 'Italy' ] ,['Juan', 44, 'Australia'] ]






dfObj = pd.DataFrame(students, columns = ['Name', 'Age','Country']) 

dfObj.columns

for each_columnName in dfObj.columns:
    print (each_columnName)

dfObj['Country'].unique()

dfObj2 = pd.DataFrame(students2, columns = ['Name', 'Age','Country']) 

sum_age = dfObj["Age"]+dfObj2["Age"]




countries = [ ['Australia', 20] ,['Brazil', 200 ] ,['UK', 66],['Italy', 60],['USA', 327] ]

df_Countries = pd.DataFrame(countries, columns = ['Country','Population'])

#concat
concatList = pd.concat([dfObj,dfObj2])
    

mergeDfs = pd.merge(concatList,df_Countries, on=['Country'], how='left')

len(mergeDfs.Country.unique())

len(mergeDfs.Country)


#remove column
mergeDfs['NewColumn']  = 3


del mergeDfs['NewColumn'] 


mergeDfs.to_csv(path_code+"/output.csv")





new_file = pd.read_csv(path_code+'/output.csv')






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



#csv read write
import csv
countries

with open(path_code+'testcsv.csv', 'a') as writeFile:
    writer = csv.writer(writeFile)
    for row in countries:
        writer.writerows([row])
writeFile.close()



#add column name

countries.insert(0,["Country","Population"])



with open(path_code+'testcsv.csv', 'a') as writeFile:
    writer = csv.writer(writeFile)
    for row in countries:
        writer.writerows([row])
writeFile.close()







#READ CSV
#With pandas
cereal_df2 = pd.read_csv(path_code+'testcsv.csv')


#With csv library
import csv
with open(path_code+'testcsv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print (row)
