from bs4 import BeautifulSoup
import requests

url="https://www.pararius.com/apartments/amsterdam/page-1"

page=requests.get(url)
#print(page)

soup=BeautifulSoup(page.content, 'html.parser')
#print(soup)

lists = soup.find_all('section', { 'div': 'listing-search-item__label' })

print(lists)

for list in lists:
    title = lists.find('a', class_="listing-search_item__title")
    location = lists.find('div', class_="listing-search-item__location")
    price = lists.find('div', class_="listing-search-item__price")
    area = lists.find('li', class_="illustrated-features__item--surface-area")
    info=[title, location, price, area]
    #print(info)
