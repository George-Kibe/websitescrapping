from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
import requests
import time

tableau_url = "https://tabexternal.dshs.texas.gov/t/THD/views/Deaths/Deaths?%3Aembed=y&showTabs=true&%3Adisplay_count=n&%3AshowVizHome=n&%3Aorigin=viz_share_link"

s = HTMLSession()

def getdata(tableau_url):
    r = s.get(tableau_url)
    #r.html.render(timeout=60)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    print("Soup generated successfully HTTPResponse 200")
    print(soup)
    #return soup

print("So far so good")
getdata(tableau_url)

