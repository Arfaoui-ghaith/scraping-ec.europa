from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 

ivdr = "https://ec.europa.eu/tools/eudamed/api/devices/udiDiData?page={0}&pageSize=50&size=300&sort=primaryDi,ASC&sort=versionNumber,DESC&iso2Code=en&applicableLegislation=refdata.applicable-legislation.ivdr&includeHistoricalVersion=true&languageIso2Code=en"
print('Requesting The IVDR Search Now...')

with urllib.request.urlopen(ivdr.format(0)) as url:
    data = json.loads(url.read().decode())

totalPages = data["totalPages"]

print("Gathering The Result Id's From {0} Page Now...".format(totalPages))
ids=[]

for p in range(totalPages):
    with urllib.request.urlopen(ivdr.format(p)) as url:
        dataPage = json.loads(url.read().decode())
    for i in dataPage["content"]:
        ids.append(i["uuid"])
    print("Page {0} - {1} / {2} Done.".format(p,len(ids),data["totalElements"]))

print(len(ids), " Has Been Scraped.")

items = np.asarray(ids)
pd.DataFrame(items).to_csv('Ivdr-Ids.csv')