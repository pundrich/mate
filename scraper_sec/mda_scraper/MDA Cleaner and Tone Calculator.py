"""
This program first identifies valid MD&A sections and then computes the tone of these sections.  The final output file will by 
SampleData.txt and it is saved in the file that you designate as filepath3.
"""
import csv
import re
import os

###############################################################################
#CHANGE THIS TO YOUR PATH
path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
###############################################################################


path_code = path_env + "/scraper_sec/mda_scraper/"

#This is the filepath of the Financial Statement text documents. This must be changed to your respective filepath.
filepath=path_code+"/downloaded_mda/"


#This is the filepath of the word dictionary files.  This must be changed to your respective filepath.
filepath2=path_code+"/Word_Dictionaries"

#if doesnt exist, create an output  folder
if not os.path.exists(path_code+"cleaned_mda"):
    os.makedirs(path_code+"cleaned_mda")

#This is where you would like the cleaned / identified MD&A section text files to be written.  This file must also include the 
#downloadlog file from the previously run MASTERSCRAPE.py program.
filepath3=path_code+"/cleaned_mda"

NEGATIVE=os.path.join(filepath2,"NEGATIVE.txt")
POSITIVE=os.path.join(filepath2,"POSITIVE.txt")
SD=os.path.join(filepath3,"Result_Analysis.csv")
download=os.path.join(filepath,"DOWNLOADLOG.txt")

'''
This section will upload the dictionaries
'''
NEGATIVE=open(NEGATIVE, 'r').readlines()
NEGATIVE=map(str.strip, NEGATIVE)
NEGATIVE=[x.lower() for x in NEGATIVE]
POSITIVE=open(POSITIVE, 'r').readlines()
POSITIVE=map(str.strip, POSITIVE)
POSITIVE=[x.lower() for x in POSITIVE]
'''
DONE
'''

'''
The following are the phrases that must be identified for a particular section to be considered a MD&A section.
'''
sayings=["the following discussion","this discussion and analysis","should be read in conjunction", "should be read together with", "the following managements discussion and analysis"]
acq=["Acquisition","acquisition","merger","Merger","Buyout","buyout"]    
'''
DONE
'''



'''
Beginning of the program
'''

#Add columns to the output file
Column_names = ["File_Num","Company Name","CIK","SIC","Disclosure Date","Sections","Number of Words","POSITIVE","NEGATIVE","ACQUISITION","TONE"]

with open(SD, mode='a') as f:
    f = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f.writerow(Column_names)


with open(download, 'r') as txtfile:
    reader = csv.reader(txtfile, delimiter='\t')
    for line in reader:

        try:
            FileNUM=line[0].strip()
            Sections=(int(line[1].strip()))
        except:
            print ("Warning: couldn't parse to integer. Ignore if is first row")
            Sections = "not an integer"
        
        if Sections!=0 and isinstance(Sections, int):
        
            Filer=os.path.join(filepath,str(FileNUM)+".txt")
            CLEAN=os.path.join(filepath3,str(FileNUM)+".txt")
            SIC=""
            Info=[str(FileNUM)]
            hand=open(Filer)
            
            
            for line in hand:    
                line=line.strip()
                if re.findall('^COMPANY NAME:',line):
                    COMNAM=line.replace("COMPANY NAME: ","")
                if re.findall('^CIK:',line):
                    CIK=line.replace("CIK: ","")
                if re.findall('^SIC:',line):
                    SIC=line.replace("SIC: ","")
                if re.findall('^REPORT PERIOD END DATE:',line):
                    REPDATE=line.replace("REPORT PERIOD END DATE: ","")
            Info.append(COMNAM)
            Info.append(CIK)
            if SIC=="":
                SIC='9999'
                Info.append(SIC)
            else:
                Info.append(SIC)
                
            Info.append(REPDATE)
            Info.append(str(Sections))
         
            str1=open(Filer).read()
            locations=[]
            for m in re.finditer("<SECTION>",str1):
                a=m.end()
                locations.append(a)
            for m in re.finditer("</SECTION>",str1):
                a=m.start()
                locations.append(a)
            if locations!=[]:
                locations.sort()
                            
            if Sections==1:
                substring1=str1[locations[0]:locations[1]]
                substring1=substring1.lower()
                substring1=re.sub('\d','',substring1)
                substring1=substring1.replace(',','')
                substring1=substring1.replace(':',' ')
                substring1=substring1.replace('?','')
                substring1=substring1.replace('.','')
                substring1=substring1.replace('$','')
                substring1=substring1.replace('(','')
                substring1=substring1.replace(')','')
                substring1=substring1.replace('%','')
                substring1=substring1.replace('"','')
                substring1=substring1.replace('-',' ')
                substring1=substring1.replace('[','')
                substring1=substring1.replace(';',' ')
                substring1=substring1.replace(']','')
                substring1=substring1.replace('_','')
                substring1=substring1.replace('|','')
                substring1=substring1.replace('/','')
                substring1=substring1.replace('`','')
                substring1=substring1.replace("'",'')
                substring1=substring1.replace('&','')
                substring1=substring1.split()
                TWORD=0
                TWORD=len(substring1)
                

                
                
                Post=[]
                
                
                Post.extend(Info)
                Post.append(str(TWORD))
                PLUS=0
                NEG=0
                ACQ=0
                for s in substring1:
                    if s in POSITIVE:
                        PLUS=PLUS+1    
                    if s in NEGATIVE:
                        NEG=NEG+1
                    if s in acq:
                        ACQ=ACQ+1
                
                Post.append(str(PLUS))
                Post.append(str(NEG))
                Post.append(str(ACQ))
                
                #The tone of the respective section is the difference between the number of negative and positive words, scaled by the total number of words in the section.
                TONE = (PLUS-NEG)/TWORD
                Post.append(str(TONE))
                
                
                
                
                
                with open(CLEAN,'a') as f:
                    f.write("<SECTION>\n")
                    f.write(' '.join(substring1)+"\n")
                    f.write("</SECTION>\n")
                    f.close()
                    
                with open(SD, mode='a') as f:
                    f = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    f.writerow(Post)

                print (Post)
                Post=[]
            else:
                for k in range(0,len(locations),2):
                    filed=0
                    substring1=str1[locations[0+k]:locations[1+k]]
                    substring1=substring1.lower()
                    substring1=substring1.split(". ")
                    if len(substring1)>5:
                        for j in range(0,6):
                            if any(s in substring1[j] for s in sayings):
                                filed=1
                                break
                    if filed==1:
                        substring1=str1[locations[0+k]:locations[1+k]]
                        substring1=substring1.lower()
                        substring1=re.sub('\d','',substring1)
                        substring1=substring1.replace(',','')
                        substring1=substring1.replace(':',' ')
                        substring1=substring1.replace('?','')
                        substring1=substring1.replace('.','')
                        substring1=substring1.replace('$','')
                        substring1=substring1.replace('(','')
                        substring1=substring1.replace(')','')
                        substring1=substring1.replace('%','')
                        substring1=substring1.replace('"','')
                        substring1=substring1.replace('-',' ')
                        substring1=substring1.replace('[','')
                        substring1=substring1.replace(';',' ')
                        substring1=substring1.replace(']','')
                        substring1=substring1.replace('_','')
                        substring1=substring1.replace('|','')
                        substring1=substring1.replace('/','')
                        substring1=substring1.replace('`','')
                        substring1=substring1.replace("'",'')
                        substring1=substring1.replace('&','')
                        substring1=substring1.split()
                        TWORD=0
                        TWORD=len(substring1)
                        Post=[]
                        Post.extend(Info)
                        Post.append(str(TWORD))
                        PLUS=0
                        NEG=0
                        ACQ=0
                        for s in substring1:
                            if s in POSITIVE:
                                PLUS=PLUS+1
                            if s in NEGATIVE:
                                NEG=NEG+1
                            if s in acq:
                                ACQ=ACQ+1
                        Post.append(str(PLUS))
                        Post.append(str(NEG))
                        Post.append(str(ACQ))
                        
                        #The tone of the respective section is the difference between the number of negative and positive words, scaled by the total number of words in the section.
                        TONE = (PLUS-NEG)/TWORD
                        Post.append(str(TONE))

                        
                        with open(CLEAN,'a') as f:
                            f.write("<SECTION>\n")
                            f.write(' '.join(substring1)+"\n")
                            f.write("</SECTION>\n")
                            f.close()
                            
                        with open(SD, mode='a') as f:
                            f = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            f.writerow(Post)

                        print (Post)
                        Post=[]
