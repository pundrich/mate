"""
This code extracts the MD&A sections from 10K financial statements.  The list of paths for the respective 10K's
are obtained from the SEC's master files giving paths to all of the public documents that are filed with the SEC
in each quarter.  The repository includes that actual download links (i.e. downloadindex.sas7bdat and downloadlist.txt) 
that we use in our study.  Our links include all filings classified as '10-K','10-K/A','10-K405/A','10-K405','10-KSB',
'10-KSB/A','10KSB','10KSB/A','10KSB40','10KSB40/A' from 2002 to 2016. 

Adapted from:

10K-MDA-Section
These programs (i.e., MDA Extractor.py and MDA Cleaner and Tone Calculator.py) will extract the Management Discussion and Analyses (MD&A) section from 10K Financial Statements and calculate the tone of these sections. You must use the attached files that contain the list of 10K files paths on the SEC servers. The program will output the sections that are potential MD&A sections and calculate the tone accordingly. For details as to how this data is used, please refer to "Do Tone Changes in Financial Statements Predict Acquisition Behavior?" by John Berns, Patty Bick, Ryan Flugum and Reza Houston. A detailed list of the included documents and programs in this repository are as follows:

downloadindex.csv
This is a csv file that includes all of the SEC filings classified as '10-K','10-K/A','10-K405/A','10-K405','10-KSB', '10-KSB/A','10KSB','10KSB/A','10KSB40','10KSB40/A' from 2002 to 2016. This data is obtained from the SEC archive located here https://www.sec.gov/Archives/edgar/full-index/. Note that this dataset contains the number of each filing that I assign. You will use this index throughout the process as 'filing' is the main identifier that I use for each filing.

downloadlist.txt
This is the text file that includes the filing number and links to be used in the MDA Extractor.py program. This text file is a subset of the downloadindex sas dataset and includes only the 'filing' and 'link' columns.

Word Dictionary Files
This file includes the Positive and Negative word dictionaries that are used to calculate the tone of the MD&A sections. Specifically, the POSITIVE.txt and NEGATIVE.txt files are used in the MDA Cleaner and Tone Calculator.py programs. These dictionaries were contructed by Tim Loughran and Bill McDonald and are used in Loughran and McDonald (2011). These dictionaries, as well as other word classifications, can be obtained at https://sraf.nd.edu/.

MDA_Tone.csv
This is the sas dataset that includes the final output of Managment Discussion and Analysis tone of each financial statement. If you would not like to understand the attached programs and would just like the resulting output, use this dataset. Also, please note that some filings have multiple possible MD&A sections - please evaluate the data carefully and make sure that each filing has only one tone measurement.

MDA Data Construction.sas
This is a sas program that constructs MDA_Tone.csv. The program uses the SampleData.txt output from running the MDA Cleaner and Tone Calculator.py program. Note that you must convert SampleData.txt to an excel document before using this program because I import data via excel into the sas program.

MDA Extractor.py
This is the python program that extracts the possible Management Discussion and Analysis (MD&A) section/s from 10K financial statements. The input file for this program is downloadlist.txt. In order to identify possible MD&A sections, we search for combinations of "Item 7. Managements Discussion and Analysis" that include:

"item 7. managements discussion and analysis" "item 7.managements discussion and analysis" "item7. managements discussion and analysis" "item7.managements discussion and analysis" "item 7. management discussion and analysis" "item 7.management discussion and analysis" "item7. management discussion and analysis" "item7.management discussion and analysis" "item 7 managements discussion and analysis" "item 7managements discussion and analysis" "item7 managements discussion and analysis" "item7managements discussion and analysis" "item 7 management discussion and analysis" "item 7management discussion and analysis" "item7 management discussion and analysis" "item7management discussion and analysis" "item 7: managements discussion and analysis" "item 7:managements discussion and analysis" "item7: managements discussion and analysis" "item7:managements discussion and analysis" "item 7: management discussion and analysis" "item 7:management discussion and analysis" "item7: management discussion and analysis" "item7:management discussion and analysis"

The program includes all sections of the financial statement that begin with one of the above phrases, copy each section of text into a new text document to be further cleaned and verified.

MDA Cleaner and Tone Calculator.py
This is the python program that cleans the output text files from MDA Extractor.py. The input files for this program are all of the output text files from MDA Extractor.py, the POSTIVE and NEGATIVE word dictionaries, and the downloadlog.txt file created from MDA Extractor.py. The output is SampleData.txt which include the number of postive, negative, and total words, along with the tone, of a verified MD&A section. In order to be classified as an MD&A section, the first 5 sentences of the respective section must include one of the following phrases: "the following discussion", "this discussion and analysis", "should be read in conjunction", "should be read together with", "the following managements discussion and analysis". Additionally, we identify possible acquisition terms that include: "Acquisition", "acquisition", "merger", "Merger", "Buyout", "buyout". The tone of the respective section is the difference between the number of negative and positive words, scaled by the total number of words in the section.
"""

import csv
import requests
import re
import os

######################################################################################
######################################################################################
# This section is for functions that are used throughout the scrape
######################################################################################
######################################################################################

########################## Obtain file Information ###################################
def parse(file1, file2):
    hand=open(file1)
    IDENTITY=""
    for line in hand:
        line=line.strip()
        if re.findall('^COMPANY CONFORMED NAME:',line):
            k = line.find(':')
            comnam=line[k+1:]
            comnam=comnam.strip()
            IDENTITY='<HEADER>\nCOMPANY NAME: '+str(comnam)+'\n'                                         
            break
        
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^CENTRAL INDEX KEY:',line):
            k = line.find(':')
            cik=line[k+1:]
            cik=cik.strip()
            #print cik
            IDENTITY=IDENTITY+'CIK: '+str(cik)+'\n'
            break
        
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^STANDARD INDUSTRIAL CLASSIFICATION:',line):
            k = line.find(':')
            sic=line[k+1:]
            sic=sic.strip()
            siccode=[]
            for s in sic: 
                if s.isdigit():
                    siccode.append(s)    
            #print siccode
            IDENTITY=IDENTITY+'SIC: '+''.join(siccode)+'\n'
            break
        
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^CONFORMED SUBMISSION TYPE:',line):
            k = line.find(':')
            subtype=line[k+1:]
            subtype=subtype.strip()
            #print subtype
            IDENTITY=IDENTITY+'FORM TYPE: '+str(subtype)+'\n'
            break
            
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^CONFORMED PERIOD OF REPORT:',line):
            k = line.find(':')
            cper=line[k+1:]
            cper=cper.strip()
            #print cper
            IDENTITY=IDENTITY+'REPORT PERIOD END DATE: '+str(cper)+'\n'
            break
            
    hand=open(file1)
    for line in hand:
        line=line.strip()
        if re.findall('^FILED AS OF DATE:',line):
            k = line.find(':')
            fdate=line[k+1:]
            fdate=fdate.strip()
            #print fdate                                
            IDENTITY=IDENTITY+'FILE DATE: '+str(fdate)+'\n'+'</HEADER>\n'
            break
            
    with open(file2, 'a') as f:
        f.write(str(IDENTITY))
        f.close()
    hand.close()

###########################  DELETE HEADER INFORMATION  #######################################

def headerclean(temp, temp1):
    mark0=0
    strings1=['</SEC-HEADER>','</IMS-HEADER>']
    hand=open(temp)
    hand.seek(0)
    for x, line in enumerate(hand):
        line=line.strip()
        if any(s in line for s in strings1):
            mark0=x
            break
    hand.seek(0)
    
    newfile=open(temp1,'w')
    for x, line in enumerate(hand):
        if x>mark0:
            newfile.write(line)
    hand.close()
    newfile.close()
    
    newfile=open(temp1,'r')
    hand=open(temp,'w')        
    for line in newfile:
        if "END PRIVACY-ENHANCED MESSAGE" not in line:
            hand.write(line)                
    hand.close()                
    newfile.close()

###########################  XBRL Cleaner  ###################################################

def xbrl_clean(cond1, cond2, str0):
    locations=[0]
    #print locations
    placement1=[]
    str0=str0.lower()
    for m in re.finditer(cond1, str0):
        a=m.start()
        placement1.append(a)
    #print placement1
    
    if placement1!=[]:
        placement2=[]
        for m in re.finditer(cond2, str0):
            a=m.end()
            placement2.append(a)
    #    print placement2
        
        len1=len(placement1)
        placement1.append(len(str0))
        
        for i in range(len1):
            placement3=[]
            locations.append(placement1[i])
            for j in placement2:
                if (j>placement1[i] and j<placement1[i+1]):
                    placement3.append(j)
                    break
            if placement3!=[]:
                locations.append(placement3[0])
            else:
                locations.append(placement1[i])
    
    #print locations
    return locations

###########################  Table Cleaner  ###################################################

def table_clean(cond1, cond2, str1):
    Items0=["item 7", "item7", "item8", "item 8"]
    Items1=["item 1", "item 2","item 3","item 4","item 5","item 6","item 9", "item 10", "item1", "item2","item3","item4","item5","item6","item9", "item10"]
    
    str2=str1.lower()
    placement1=[]
    for m in re.finditer(cond1, str2):
        a=m.start()
        placement1.append(a)
    n=len(placement1)
    placement1.append(len(str2))
    
    placement2=[]
    for m in re.finditer(cond2, str2):
        a=m.end()
        placement2.append(a)
        
    if (placement1!=[] and placement2!=[]):
        current=str1[0:placement1[0]]
        
        for i in range(n):
            begin=placement1[i]
            for j in placement2:
                if j>begin:
                    end=j
                    break
            
            if end=="":
                current=current+str1[begin:placement1[i+1]]
            else:
                str2=""
                str2=str1[begin:end].lower()
                str2=str2.replace("&nbsp;"," ")
                str2=str2.replace("&NBSP;"," ")
                p = re.compile(r'&#\d{1,5};')
                str2=p.sub("",str2)
                p = re.compile(r'&#.{1,5};')
                str2=p.sub("",str2)
                if any(s in str2 for s in Items0):
                    if not any(s in str2 for s in Items1):
                        current=current+str2
                    
                current=current+str1[end:placement1[i+1]]
                end=""
    else:
        current=str1
    return current
