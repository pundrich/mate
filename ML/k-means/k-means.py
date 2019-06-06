#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Tue Feb  5 15:02:40 2019

Multidimensional data analysis in Python
https://www.geeksforgeeks.org/multidimensional-data-analysis-in-python/

@author: gabrielpundrich
"""



import pandas as pd 
import matplotlib.pyplot as plot
#import scipy
import numpy
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans 
import time

timestr = time.strftime("%Y%m%d-%H%M%S")


path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"


base_dir = path_env + "/ML/k-means/"
output_dir =base_dir + "/output/"



firm_data_pre = pd.read_csv(base_dir + "/input/input_compustat.csv", encoding = 'utf-8', 
                              index_col = ["gvkey"]) 

print(firm_data_pre.columns)

cluster_map_final= pd.DataFrame()

for year_selected in range(1998,1999):
    print (year_selected)
    
    
  #  year_selected = 2000 
    #select year
    firm_data = firm_data_pre.loc[firm_data_pre['fyear'] == year_selected]
    
    #select columns
    #cluster 1
    firm_data = firm_data[[ 'evs', 'pb',  'lev', 'rnoa', 'roe', 'rd','consensus_me','profit_margin','intro', 'gro', 'mat', 'decltot', 'shaketot']].copy()
    
    
      
    #cluster 2
    #firm_data = firm_data[[ 'mkvalt2','dltt','dlc','pstk','mib','ch','sale', 'pb',  'lev', 'rnoa', 'roe', 'rd','consensus_me','profit_margin','intro', 'gro', 'mat', 'decltot', 'shaketot']].copy()
    
    #cluster 3 lifecycle
    #firm_data = firm_data[[ 'mkvalt2','dltt','dlc','pstk','mib','ch','sale','fincf','ivncf','oancf']].copy()
    #firm_data = firm_data[[ 'mkvalt2','dltt','dlc','pstk']].copy()
    
    
    
    # print first 5 rows of zoo data  
    print(firm_data.head())
    
    
    
     
     
    
#    # Python code to Standardize data (0 mean, 1 stdev) 
    from sklearn.preprocessing import StandardScaler 
    array = firm_data.values 
      
    scaler = StandardScaler().fit(array)
    rescaledX = scaler.transform(array)
      
    # summarize transformed data
    numpy.set_printoptions(precision=3)
    print(rescaledX[0:5,:])



    #Step N ##################################################################
    #Rescale variables#
    array = firm_data.values
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    rescaledX = scaler.fit_transform(array)
    # summarize transformed data
    numpy.set_printoptions(precision=3)
    print(rescaledX[0:5,:])
     
   
    
    
    #Step N ##################################################################
    #Evaluate and Find the number of clusters
    wcss = []
    for i in range (1,16): #15 cluster
#        kmeans = KMeans(n_clusters = i, init='k-means++', random_state=0) 
        
        kmeans = KMeans(n_clusters=i, init='k-means++', 
            max_iter=100, n_init=1, verbose=0, random_state=3425)

        
        
        kmeans.fit(rescaledX)
        wcss.append(kmeans.inertia_)
    
    plot.plot(range(1,16),wcss)
    plot.title('Elbow Method')
    plot.xlabel('Number of clusters')
    plot.ylabel('wcss')
    plot.show()
    
    ##########################################################################
    
    #clusters = 20 works great without cycle!
    
    clusters = 20
      
    kmeans = KMeans(n_clusters = clusters) 
    kmeans.fit(rescaledX) 
    
    print(kmeans.labels_)
    print (kmeans.inertia_)
    
    #append data to clustermap
    
    cluster_map = pd.DataFrame()
    cluster_map['gvkey'] = firm_data.index.values
    cluster_map['cluster'] = kmeans.labels_
    cluster_map['fyear'] = year_selected
    
    cluster_map_final = cluster_map_final.append(cluster_map)

#output clustermap to csv
cluster_map_final.to_csv(output_dir + "output_clusters.csv", sep=',', encoding='utf-8')


cluster_map_final.groupby(['cluster']).agg(['mean', 'count'])


df = cluster_map_final.drop(['gvkey','fyear'], axis=1)

df['each_item'] =1 
print(df.columns)

g = df.groupby('cluster')


out = g.count()

out.columns

out.plot()





