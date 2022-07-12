from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 

ivdd = "https://ec.europa.eu/tools/eudamed/api/devices/udiDiData?page={0}&pageSize=300&applicableLegislation=refdata.applicable-legislation.ivdr&includeHistoricalVersion=true&size=300"
print('Requesting The IVDR Search Now...')

with urllib.request.urlopen(ivdd.format(0)) as url:
    data = json.loads(url.read().decode())

totalPages = data["totalPages"]

print("Gathering The Result Id's From {0} Page Now...".format(totalPages))
ids=[]

for p in range(totalPages):
    with urllib.request.urlopen(ivdd.format(p)) as url:
        dataPage = json.loads(url.read().decode())
    for i in dataPage["content"]:
        ids.append(i["uuid"])
    print("Page {0} Done.".format(p))

print(len(ids), " Has Been Scraped.")

items = np.asarray(ids)
pd.DataFrame(items).to_csv('Ivdr-Ids.csv')