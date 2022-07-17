from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 
import csv

with open('manufacturer-Ids.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

link = "https://ec.europa.eu/tools/eudamed/api/actors/{0}/publicInformation?languageIso2Code=en"
print('Requesting The IVDR Search Now...')

base=[]
index=['Actor ID/SRN', 
       'Role', 
       'Country', 
       'Actor/Organisation name',  
       'VAT number', 
       'EORI', 
       'National trade register', 
       'Street name', 
       'Street number', 
       'Address line 2', 
       'PO box',
       'City',
       'Postal Code',
       'Country',
       'Email',
       'Phone number',
       'Website',
       'link'
       ]
print("Start Scraping Now...")

for p in range(1,len(data)):
    row=[]
    try:
        with urllib.request.urlopen(link.format(data[p][1])) as url:
            dataPage = json.loads(url.read().decode())
        if(url.getcode() == 200):
            row.append(dataPage["actorDataPublicView"]["eudamedIdentifier"])
            row.append('Manufacturer')
            row.append(dataPage["actorDataPublicView"]["country"]["name"])
            row.append(dataPage["actorDataPublicView"]["name"]["texts"][0]["text"])
            row.append(dataPage["actorDataPublicView"]["europeanVatNumber"])
            row.append(dataPage["actorDataPublicView"]["eori"])
            row.append(dataPage["actorDataPublicView"]["tradeRegister"])
            row.append(dataPage["actorDataPublicView"]["actorAddress"]["streetName"])
            row.append(dataPage["actorDataPublicView"]["actorAddress"]["buildingNumber"])
            row.append(dataPage["actorDataPublicView"]["actorAddress"]["complement"])
            row.append(dataPage["actorDataPublicView"]["actorAddress"]["postbox"])
            row.append(dataPage["actorDataPublicView"]["actorAddress"]["cityName"])
            row.append(dataPage["actorDataPublicView"]["actorAddress"]["postalZone"])
            row.append(dataPage["actorDataPublicView"]["country"]["name"])
            row.append(dataPage["actorDataPublicView"]["electronicMail"])
            row.append(dataPage["actorDataPublicView"]["telephone"])
            row.append(dataPage["actorDataPublicView"]["website"])
            row.append("https://ec.europa.eu/tools/eudamed/#/screen/search-eo/{0}".format(data[p][1]))
            
            base.append(row)
            print("({0} / {1}) Done...".format(data[p][0],len(data)))
            items = np.asarray(base)
            pd.DataFrame(items,None,index).to_csv('manufacturer.csv')
    except:
        print("cant acces to ",link.format(data[p][1]))
