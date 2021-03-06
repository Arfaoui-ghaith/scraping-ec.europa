from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 
import csv

with open('../Ivdd-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

link = "https://ec.europa.eu/tools/eudamed/api/devices/basicUdiData/udiDiData/{0}?languageIso2Code=en"
print('Requesting The IVDD Search Now For Certificates details...')

base=[]
index=['Actor ID/SRN',
       'Actor/Organisation name',
       'Device Name',
       'NB ID, name',
       'Certificate number',
       'Certificate revision',
       'Certificate issue date',
       'Certificate expiry date',
       'Certificate status',
       'link'
       ]
print("Start Scraping Now...")

for p in range(1,len(data)):
    row=[]
    try:
        with urllib.request.urlopen(link.format(data[p][1])) as url:
            dataPage = json.loads(url.read().decode())
        if(url.getcode() == 200):
            for ct in dataPage["deviceCertificateInfoList"]:
                row=[]
                try:
                    row.append(dataPage["manufacturer"]["srn"])
                except:
                    row.append("")
                try:
                    row.append(dataPage["manufacturer"]["name"])
                except:
                    row.append("")
                try:
                    row.append(dataPage["deviceName"])
                except:
                    row.append("")

                try:
                    row.append("{0}, {1}".format(ct["notifiedBody"]["srn"],ct["notifiedBody"]["name"]))
                except:
                    row.append("")
                
                try:
                    row.append(ct["certificateNumber"])
                except:
                    row.append("")
                
                try:
                    row.append(ct["certificateRevision"])
                except:
                    row.append("")
                
                try:
                    row.append(ct["issueDate"])
                except:
                    row.append("")
                
                try:
                    row.append(ct["certificateExpiry"])
                except:
                    row.append("")
                    
                try:
                    row.append(ct["status"])
                except:
                    row.append("")
            
                try:
                    row.append("https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(data[p][1]))
                except:
                    row.append("")
                
                base.append(row)
                print("({0} / {1}) Done...".format(data[p][0],len(data)))
                items = np.asarray(base)
                pd.DataFrame(items,None,index).to_csv('Certificates.csv')
    except:
        print("cant acces to ",link.format(data[p][1]))
    
    
