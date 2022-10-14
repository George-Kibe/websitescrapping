import json
import re
import requests
from bs4 import BeautifulSoup
s = requests.Session()

init_url = "https://idph.illinois.gov/OpioidDataDashboard/"
print(f"GET {init_url}")
r = s.get(init_url)
soup = BeautifulSoup(r.text, "html.parser")
paramTags = dict([
    (t["name"], t["value"]) 
    for t in soup.find("div", {"class":"tableauPlaceholder"}).findAll("param")
])

# get xsrf cookie
session_url = f'{paramTags["host_url"]}trusted/{paramTags["ticket"]}{paramTags["site_root"]}/views/{paramTags["name"]}'
print(f"GET {session_url}")
r = s.get(session_url)

config_url = f'{paramTags["host_url"][:-1]}{paramTags["site_root"]}/views/{paramTags["name"]}'
print(f"GET {config_url}")
r = s.get(config_url,
    params = {
        ":embed": "y",
        ":showVizHome": "no",
        ":host_url": "https://interactive.data.illinois.gov/",
        ":embed_code_version": 2,
        ":tabs": "yes",
        ":toolbar": "no",
        ":showShareOptions": "false",
        ":display_spinner": "no",
        ":loadOrderID": 0,
})
soup = BeautifulSoup(r.text, "html.parser")
tableauData = json.loads(soup.find("textarea",{"id": "tsConfigContainer"}).text)

dataUrl = f'{paramTags["host_url"][:-1]}{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'
print(f"POST {dataUrl}")
r = s.post(dataUrl, data= {
    "sheet_id": tableauData["sheetId"],
})
dataReg = re.search('\d+;({.*})\d+;({.*})', r.text, re.MULTILINE)
info = json.loads(dataReg.group(1))
data = json.loads(dataReg.group(2))

print(data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])