from requests_html import HTMLSession
from bs4 import BeautifulSoup
import random
import requests
import time

s = HTMLSession()

offer_and_coupon_items =["laptops","bags","books","arts","samsung","suits","macbook","monitors",
"iphones", "cabinets","Automotive","Baby","Beauty","Books","Fashion","Music","Computers","Tools",
"Kindle","Luggage","Men's Fashion","Software","Sports","Video+Games"]

telegram_url="https://api.telegram.org/bot5198206552:AAG6-73A47O0GnzNJcLWkG57OD8ICeV6eGU/sendPhoto"


def get_offer_url(offer_and_coupon_items):
    offer_and_coupon_item = random.choice(offer_and_coupon_items)
    url=f'https://www.amazon.com/hz/coupons/search?searchText={offer_and_coupon_item}'
    print(offer_and_coupon_item)
    print(url)
    return url

def getdata(url):
    r = s.get(url)
    r.html.render(timeout=20) #prevent being blocked by amazon
    soup = BeautifulSoup(r.html.html, 'html.parser')
    print("soup generated successfully HTTPResponse 200")
    return soup

def getdeals(soup): 
    offer_or_coupon_items = soup.find_all('div', {'class': 'a-section a-spacing-none a-text-left coupon'})
    for item in offer_or_coupon_items:
        title = item.find('div', {'class': 'a-section a-spacing-small coupon-description'}).text.strip()
        #short_title = item.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()[:50]
        unique_key = item['data-promoid']
        refined_link= "https://www.amazon.com/promotion/psp/"+unique_key
        image_url= item.find('img',{'class': 'a-dynamic-image coupon-image'})['src']
        
        try:
            coupon=item.find('span', {'class': 'a-size-medium a-color-success a-text-bold'}).text.replace('Save','').strip()
            coupon_mode="Applied Automatically on Checkout"
        except:
            coupon="Missing"            
        print(title, refined_link, image_url, coupon, coupon_mode)
        

        parameters = {
            "chat_id": "-743974581", #specific chat id
            "photo": image_url, #image to send
            "caption": title+"\n"+refined_link+"\nCoupon:"+coupon+"\nCoupon Code: "+coupon_mode
        }
        resp=requests.get(telegram_url, data=parameters)
        print("Notification sent to telegram")
        sleep_time = random.randint(60, 120) 
        time.sleep(sleep_time)
        pass
        



while True:
    url=get_offer_url(offer_and_coupon_items)
    soup = getdata(url)
    try:
        getdeals(soup)
    except:
        pass
    sleep_time = random.randint(10, 20)        
    time.sleep(sleep_time)

