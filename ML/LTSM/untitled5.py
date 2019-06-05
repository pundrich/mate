#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:49:01 2019

@author: gabrielpundrich
"""
banana = 5
apple = 2

print(banana) 



if banana == 5:
    print("Banana is equal to 5")
    
    
    
fruit1 = "apple"
fruit2 = "banana" 

print("I have " + str(apple)  )


print("I have a total of " + str(apple+banana))


#Lists

teams  = ["red sox","patriots","bruins"]

#iteration: FOR LOOP

sports = []
for each_team in teams:
    #print(each_team)
    
    if each_team == "red sox":
        sports.append("Baseball")
        
    if each_team == "patriots":
        sports.append("Football")
        
    if each_team == "bruins":
        sports.append("Hockey")
        
print(sports)


print (sports[-1])



















