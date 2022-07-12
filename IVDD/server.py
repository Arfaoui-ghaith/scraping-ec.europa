from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np

browser = webdriver.Chrome("chromedriver.exe")

with open('Ivdd-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
base=[]
index=['Applicable legislation', 
       'EUDAMED DI code', 
       'Kit', 
       'Risk class', 
       'Companion diagnostic', 
       'Near patient testing', 
       'Patient self testing', 
       'Professional testing', 
       'Reagent', 
       'Instrument', 
       'Device name', 
       'Presence of human tissues and cells or their derivatives',
       'Presence of animal tissues and cells or their derivatives',
       'Presence of cells or substances of microbial origin', 'link']
print("Start Scraping Now...")
t=5
for j in data:
    row=[]
    url = "https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(j[1])
    browser.get(url)

    time.sleep(t)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    list = soup.find_all('dl')
    for i in range(7,21):
        try:
            row.append(list[i].find('dd').text)
        except AttributeError :
            row.append(None)
    
    row.append(url)
    base.append(row)
    print("({0} / {1}) Done...".format(j[0],len(data)))
    items = np.asarray(base)
    pd.DataFrame(items,None,index).to_csv('Ivdd.xlsx')
    t=1.5
        
browser.quit()
