# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from urllib import request
from bs4 import BeautifulSoup
import re
from math import ceil
import csv
 
# Determine the number of pages to webscrape
scac = "http://securities.stanford.edu/filings.html"
page = request.urlopen(scac)
soup = BeautifulSoup(page, 'html.parser')
heading = soup.find_all('h4')[-1].get_text()
total_record_num = re.findall(r'\d+', heading)[0]
total_page_num = ceil(int(total_record_num) / 20)
 
# Webscrape all pages
container = [("filing_name", "filing_date", "district_court", "exchange", "ticker")]
i = 1
while i <= total_page_num:
    url = scac + "?page=" + repr(i)
    print(url)
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', class_ = 'table table-bordered table-striped table-hover')
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        columns = row.find_all('td')
        c1 = re.sub(r'[\t\n]', '', columns[0].get_text()).strip()
        c2 = re.sub(r'[\t\n]', '', columns[1].get_text()).strip()
        c3 = re.sub(r'[\t\n]', '', columns[2].get_text()).strip()
        c4 = re.sub(r'[\t\n]', '', columns[3].get_text()).strip()
        c5 = re.sub(r'[\t\n]', '', columns[4].get_text()).strip()
        container.append((c1, c2, c3, c4, c5))
    i = i + 1
 
    # Write to a CSV file
    with open('scac.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(container)