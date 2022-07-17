import urllib.request, json 
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
from requests.exceptions import HTTPError,ConnectionError

link0 = "https://ec.europa.eu/tools/eudamed/api/referenceValues?typeCode=APPLICABLE_LEGISLATION&sort=displayOrder&languageIso2Code=en"
link = "https://ec.europa.eu/tools/eudamed/api/devices/basicUdiData/udiDiData/{0}?languageIso2Code=en"

with open('Ivdr-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
    data.pop(0)
    
base=[]
index=['Actor ID/SRN',
       'Actor/Organisation name',
        'Applicable legislation', 
       'Basic UDI-DI code', 
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
with urllib.request.urlopen(link0) as url:
        appLig = json.loads(url.read().decode())


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
                row.append(appLig[1]["translationText"])
            except:
                row.append("")
            try:
                row.append("{0} / {1}".format(dataPage["basicUdi"]["code"], dataPage["basicUdi"]["issuingAgency"]["code"].split('.')[-1].upper()))
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["kit"] else "No")
            except:
                row.append("")
           
            try:
                row.append(dataPage["riskClass"]["code"].split('.')[-1].upper())
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["companionDiagnostics"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["nearPatientTesting"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["selfTesting"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["professionalTesting"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["reagent"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["instrument"] else "No")
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
                row.append("Yes" if dataPage["microbialSubstances"] else "No")
            except:
                row.append("")
            try:
                row.append("https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(data[p][1]))
            except:
                row.append("")
            
            base.append(row)
            print("({0} / {1}) Done...".format(data[p][0],len(data)))
            items = np.asarray(base)
            pd.DataFrame(items,None,index).to_csv('Ivdr.csv')
    except:
        print("cant acces to ",link.format(data[p][1]))
