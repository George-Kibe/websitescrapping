from tableauscraper import TableauScraper as TS
import requests
from bs4 import BeautifulSoup

init_url = "https://tabexternal.dshs.texas.gov/t/THD/views/Deaths/Deaths?%3Aembed=y&showTabs=true&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link"
r = requests.get(init_url)
soup = BeautifulSoup(r.text, "html.parser")
print(soup)
paramTags = dict([
    (t["name"], t["value"])
    for t in soup.find("div", {"class": "tundra tableau"}).findAll("param")
])

url = f'{paramTags["host_url"]}trusted/{paramTags["ticket"]}{paramTags["site_root"]}/views/{paramTags["name"]}'

ts = TS()
ts.loads(url)
dashboard = ts.getWorkbook()

for t in dashboard.worksheets:
    # show worksheet name
    print(f"WORKSHEET NAME : {t.name}")
    # show dataframe for this worksheet
    print(t.data)

print("all is well")