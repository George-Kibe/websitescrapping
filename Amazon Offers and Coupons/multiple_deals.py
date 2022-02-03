from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
import requests
import time

s = HTMLSession()

offer_and_coupon_items =["laptops","coupons","offers","monitors","iphones", "cabinets","Arts & Crafts","Automotive",
"Baby","Beauty & Personal Care","Books","Digital Music","Computers","Tools & Home Improvement",
"Deals","Industrial & Scientific","Kindle Store","Luggage","Men's Fashion", "Music, CDs & Vinyl",
"Pet Supplies","Software","Sports & Outdoors","Video Games","Women's Fashion","All Departments"]

telegram_url="https://api.telegram.org/bot5198206552:AAG6-73A47O0GnzNJcLWkG57OD8ICeV6eGU/sendPhoto"


def get_offer_url(offer_and_coupon_items):
    offer_and_coupon_item = random.choice(offer_and_coupon_items)
    url = f'https://www.amazon.com/s?k={offer_and_coupon_item}&i=black-friday'
    print(offer_and_coupon_item)
    return url

def getdata(url):
    r = s.get(url)
    r.html.render(timeout=20) #prevent being blocked by amazon
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getdeals(soup): 
    offer_or_coupon_items = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in offer_or_coupon_items:
        title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        link = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
        refined_link= "https://www.amazon.com"+link
        image_url= item.find('img',{'class': 's-image'})['src']
        try:
            saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('$','').replace(',','').strip())
            oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('$','').replace(',','').strip())
        except:
            saleprice="Missing"
            oldprice="Missing"            
        try:
            reviews = item.find('span', {'class', 'a-size-base'}).text.strip()
        except:
            reviews=0
        #print(short_title, refined_link, image_url, saleprice, oldprice)

        parameters = {
            "chat_id": "-743974581", #specific chat id
            "photo": image_url, #image to send
            "caption": title+"\n"+refined_link+"\nPreviously being sold at $"+str(oldprice)+"\nCurrently being sold at $"+str(saleprice),
        }
        resp=requests.get(telegram_url, data=parameters)
        print("Notification sent to telegram")

        sleep_time = random.randint(60, 200)        
        time.sleep(sleep_time)


def getnextpage(soup): 
    pages = soup.find('span', {'class': 's-pagination-strip'})

    if not pages.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled'}): #last page
        url = 'https://www.amazon.com' + str(pages.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
        return url
    else:
        return

while True:
    url=get_offer_url(offer_and_coupon_items)
    soup = getdata(url)    
    try:
      getdeals(soup)
      url2 = getnextpage(soup)
      soup = getdata(url2) 
      getdeals(soup)
    except:
      pass
    
    sleep_time = random.randint(10, 20) 
    time.sleep(sleep_time)
      
