from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError,ConnectionError
import pandas as pd
import numpy as np
import json
import urllib.request, json 

aimdd = "https://ec.europa.eu/tools/eudamed/api/devices/udiDiData?page={0}&pageSize=300&applicableLegislation=refdata.applicable-legislation.aimdd&includeHistoricalVersion=true&size=300"
print('Requesting The AIMDD Search Now...')

with urllib.request.urlopen(aimdd.format(0)) as url:
    data = json.loads(url.read().decode())

totalPages = data["totalPages"]

print("Gathering The Result Id's From {0} Page Now...".format(totalPages))
ids=[]

for p in range(totalPages):
    with urllib.request.urlopen(aimdd.format(p)) as url:
        dataPage = json.loads(url.read().decode())
    for i in dataPage["content"]:
        ids.append(i["uuid"])
    print("Page {0} Done.".format(p))

print(len(ids), " Ids Has Been Scraped.")

items = np.asarray(ids)
pd.DataFrame(items).to_csv('Aimdd-Ids.csv')