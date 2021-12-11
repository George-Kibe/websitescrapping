from bs4 import BeautifulSoup
import requests
from csv import writer

url= "https://www.knightfrank.co.ke/properties/residential/for-sale/kenya/all-types/all-beds;pricemin=318750000;currency=KES"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
lists = soup.find_all('article', class_="mh-estate-vertical")

print(lists)

with open('housing.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Title', 'Location', 'Price', 'Area']
    thewriter.writerow(header)

    for list in lists:
        title = list.find('a', class_="listing-search-item__link--title").text.replace('\n', '')
        location = list.find('div', class_="listing-search-item__location").text.replace('\n', '')
        price = list.find('span', class_="listing-search-item__price").text.replace('\n', '')
        area = list.find('span', class_="illustrated-features__description").text.replace('\n', '')
        
        info = [title, location, price, area]
        #thewriter.writerow(info)
