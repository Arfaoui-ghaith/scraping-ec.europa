import urllib.request, json 
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
from requests.exceptions import HTTPError,ConnectionError

with open('Aimdd-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
    data.pop(0)
    
link0 = "https://ec.europa.eu/tools/eudamed/api/referenceValues?typeCode=APPLICABLE_LEGISLATION&sort=displayOrder&languageIso2Code=en"
link = "https://ec.europa.eu/tools/eudamed/api/devices/basicUdiData/udiDiData/{0}?languageIso2Code=en"

print('Requesting The AIMDD Search Now For UDI-DI details...')

base=[]
index=['Actor ID/SRN',
       'Actor/Organisation name',
       'Applicable legislation',
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

with urllib.request.urlopen(link0) as url:
        appLig = json.loads(url.read().decode())

print(appLig[4]["translationText"])


for p in range(len(data)):
    row=[]
    try:
        with urllib.request.urlopen(link.format(data[p][1])) as url:
            dataPage = json.loads(url.read().decode())
        if(url.getcode() == 200):
            try:
                row.append(dataPage["manufacturer"]["srn"])
            except:
                row.append("")
            try:
                row.append(dataPage["manufacturer"]["name"])
            except:
                row.append("")
            try:
                row.append(appLig[4]["translationText"])
            except:
                row.append("")
            try:
                row.append("{0} / {1}".format(dataPage["basicUdi"]["code"], dataPage["basicUdi"]["issuingAgency"]["code"].split('.')[-1].upper()))
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["device"] else "No")
            except:
                row.append("")
           
            try:
                row.append(dataPage["riskClass"]["code"].split('.')[-1].upper())
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["implantable"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["measuringFunction"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["reusable"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["active"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["administeringMedicine"] else "No")
            except:
                row.append("")
            try:
                row.append(dataPage["deviceName"])
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["humanTissues"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["animalTissues"] else "No")
            except:
                row.append("")
            try:
                row.append("https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(data[p][1]))
            except:
                row.append("")
            
            base.append(row)
            print("({0} / {1}) Done...".format(data[p][0],len(data)))
            items = np.asarray(base)
            pd.DataFrame(items,None,index).to_csv('Aimdd.csv')
    except:
        print("cant acces to ",link.format(data[p][1]))
    
    
