from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 
import csv

with open('../Ivdr-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

link = "https://ec.europa.eu/tools/eudamed/api/devices/udiDiData/{0}?languageIso2Code=en"
link1 = "https://ec.europa.eu/tools/eudamed/api/devices/basicUdiData/udiDiData/{0}?languageIso2Code=en"

print('Requesting The IVDR Search Now For UDI-DI details...')

base=[]
index=['Actor ID/SRN',
       'Actor/Organisation name',
        'UDI-DI code', 
       'Status',
       'Nomenclature code(s)',
       'Name/Trade name(s)',
       'Reference-catalogue number',
       'Additional Product description',
       'Additional information url',
       'Clinical sizes',
       'Labelled as single use',
       'Maximum number of reuses',
       'Need for sterilisation before use',
       'Device labelled as sterile',
       'Containing Latex',
       'Storage and handling conditions',
       'Critical warnings or contra-indications',
       'Reprocessesed single use device',
       'Member state of the placing on the EU market of the device',
       'link'
       ]
print("Start Scraping Now...")

for p in range(1,len(data)):
    row=[]
    try:
        with urllib.request.urlopen(link.format(data[p][1])) as url:
            dataPage = json.loads(url.read().decode())
        with urllib.request.urlopen(link1.format(data[p][1])) as url:
            dataPage1 = json.loads(url.read().decode())
        if(url.getcode() == 200):
            try:
                row.append(dataPage1["manufacturer"]["srn"])
            except:
                row.append("")
            try:
                row.append(dataPage1["manufacturer"]["name"])
            except:
                row.append("")
            try:
                row.append(dataPage["primaryDi"]["code"]+" / "+dataPage["primaryDi"]["issuingAgency"]["code"].split('.')[-1].upper())
            except:
                row.append("")
            try:
                row.append("On the {0} Market".format(dataPage["placedOnTheMarket"]["type"].split('_')[0]))
            except:
                row.append("")
            try:
                row.append(dataPage["cndNomenclatures"][0]["code"]+": "+dataPage["cndNomenclatures"][0]["description"]["texts"][2]["text"])
            except:
                row.append("")
            try:
                row.append(dataPage["tradeName"]["texts"][0]["text"]+"[{0}]".format(dataPage["tradeName"]["texts"][0]["language"]["isoCode"].upper()))
            except:
                row.append("")
            try:
                row.append(dataPage["reference"])
            except:
                row.append("")
            try:
                row.append(dataPage["additionalDescription"]["texts"][0]["text"]+"[{0}]".format(dataPage["tradeName"]["texts"][0]["language"]["isoCode"].upper()))
            except:
                row.append("")
            try:
                row.append(dataPage["additionalInformationUrl"])
            except:
                row.append("")
            try:
                row.append(''.join(dataPage["clinicalSizes"]))
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["singleUse"] else "No")
            except:
                row.append("")
            try:
                row.append(dataPage["maxNumberOfReuses"] if dataPage["maxNumberOfReuses"] else "")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["sterilization"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["sterile"] else "No")
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["latex"] else "No")
            except:
                row.append("")
            try:
                row.append(" | ".join([ el["description"]["texts"][0]["text"] for el in dataPage["storageHandlingConditions"] ]))
            except:
                row.append("")
            try:
                row.append(" | ".join([ el["description"]["texts"][0]["text"].replace(',', '.') for el in dataPage["criticalWarnings"] ]))
            except:
                row.append("")
            try:
                row.append("Yes" if dataPage["reprocessed"] else "No")
            except:
                row.append("")
            try:
                row.append(dataPage["placedOnTheMarket"]["name"])
            except:
                row.append("")
            try:
                row.append("https://ec.europa.eu/tools/eudamed/#/screen/search-device/{0}".format(data[p][1]))
            except:
                row.append("")
            
            base.append(row)
            print("({0} / {1}) Done...".format(data[p][0],len(data)))
            items = np.asarray(base)
            pd.DataFrame(items,None,index).to_csv('UDI-DI.csv')
    except:
        print("cant acces to ",link.format(data[p][1]))
    
