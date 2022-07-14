from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 
import csv

with open('../Aimdd-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

link = "https://ec.europa.eu/tools/eudamed/api/devices/udiDiData/{0}?languageIso2Code=en"
print('Requesting The AIMDD Search Now For Market distribution details...')

base=[]
index=[
       'Device Name',
       'Markets',
       'link'
       ]
print("Start Scraping Now...")

for p in range(1,len(data)):
    row=[]
    try:
        with urllib.request.urlopen(link.format(data[p][1])) as url:
            dataPage = json.loads(url.read().decode())
        if(url.getcode() == 200):
           
            try:
                row.append(dataPage["tradeName"]["texts"][0]["text"])
            except:
                row.append("")
            
            try:
                row.append(" | ".join([ "{0}. (From {1} to {2})".format(el["country"]["name"],el["startDate"],el["endDate"]) for el in dataPage["marketInfoLink"]["msWhereAvailable"] ]))
            except:
                row.append("")
           
            try:
                row.append("https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(data[p][1]))
            except:
                row.append("")
            
            base.append(row)
            print("({0} / {1}) Done...".format(data[p][0],len(data)))
            items = np.asarray(base)
            pd.DataFrame(items,None,index).to_csv('Markets.csv')
    except:
        print("cant acces to ",link.format(data[p][1]))
    
    
