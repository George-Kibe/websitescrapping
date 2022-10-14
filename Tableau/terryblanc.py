from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
import requests
import time

#tableau_url = "https://tabexternal.dshs.texas.gov/t/THD/views/Deaths/Deaths?%3Aembed=y&showTabs=true&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link"
combinations_url = "https://tabexternal.dshs.texas.gov/t/THD/views/Deaths/Deaths?%3Aembed=y&showTabs=true&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link"
s = HTMLSession()

def getdata(tableau_url):
    r = s.get(tableau_url)
    #r.html.render(timeout=60)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    print("Soup generated successfully HTTPResponse 200")
    print(soup)
    table_data = soup.find_all("div", {"class": "tundra tableau ff-IFrameSizedToWindow"})
    print(table_data)
    #return table_data

print("So far so good")
getdata(combinations_url)

