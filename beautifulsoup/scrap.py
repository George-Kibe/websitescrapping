from bs4 import BeautifulSoup
import requests
import re

# get the data
data = requests.get('http://acumenvaluers.co.ke/')

# extract the phone numbers, emails, whatever
phones = re.findall(r'(\(?[0-9]{3}\)?(?:\-|\s|\.)?[0-9]{3}(?:\-|\.)[0-9]{4})', data.text)
emails = re.findall(r'([\d\w\.]+@[\d\w\.\-]+\.\w+)', data.text)

print(data)

print(phones, emails)
