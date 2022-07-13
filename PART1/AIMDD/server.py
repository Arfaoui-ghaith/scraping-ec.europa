from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np

browser = webdriver.Chrome("chromedriver.exe")

with open('Aimdd-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
base=[]
index=['Applicable legislation', 
       'EUDAMED DI code', 
       'System/Procedure which is a device in itself',
       'Risk class', 
       'Implantable', 
       'Measuring function', 
       'Reusable surgical instrument', 
       'Active device', 
       'Device intended to administer and / or remove medicinal product',
       'Device name', 
       'Presence of human tissues and cells or their derivatives',
       'Presence of animal tissues and cells or their derivatives',
       'link']
print("Start Scraping Now...")
t=10
for j in data:
    row=[]
    url = "https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(j[1])
    browser.get(url)

    time.sleep(t)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    list = soup.find_all('dl')
    for i in range(7,23):
        try:
            if(list[i].find('dt').text in index):
                row.append(list[i].find('dd').text)
        except AttributeError :
            row.append(None)
    
    row.append(url)
    print(row, len(row))
    base.append(row)
    print("({0} / {1}) Done...".format(j[0],len(data)))
    items = np.asarray(base)
    pd.DataFrame(items,None,index).to_csv('Aimdd.xlsx')
    #t=10
        
browser.quit()
