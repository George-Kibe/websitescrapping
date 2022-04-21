from django.shortcuts import render
from django.contrib import messages
import aiohttp
import asyncio
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import random
import requests
import time

s = AsyncHTMLSession()
telegram_url = "https://api.telegram.org/bot5198206552:AAG6-73A47O0GnzNJcLWkG57OD8ICeV6eGU/sendPhoto"

daily_offers_url = "https://www.amazon.com/gp/goldbox"


async def getdata(daily_offers_url):
    task1 = s.get(daily_offers_url)
    print("So far so good")
    r = await task1
    r.html.render(timeout=20)
    soup = await BeautifulSoup(r.html.html, 'html.parser')
    print("Soup generated successfully HTTPResponse 200")
    return soup


async def getdeals(soup):
    task = asyncio.create_task(getdata(daily_offers_url))
    await task
    daily_deals = await soup.find_all(
        'div', {'class': 'DealGridItem-module__dealItemContent_1vFddcq1F8pUxM8dd9FW32'})
    for item in daily_deals:
        title = item.find('div', {
                          'class': 'DealContent-module__truncate_sWbxETx42ZPStTc9jwySW'}).text.strip()
        refined_link = item.find(
            'a', {'class': 'a-link-normal a-color-base a-text-normal'})['href']
        image_url = item.find('img')['src']
        try:
            saleprice = float(
                item.find('span', {'class': 'a-price-whole'}).text.strip())
            offer_details = item.find(
                'span', {'class': 'a-size-small a-color-secondary'}).text.strip()
        except:
            saleprice = "Missing"
            offer_details = "Offer Expired"

        #print(title, refined_link, image_url, saleprice, offer_details)

        parameters = {
            "chat_id": "-1001715128710",  # specific chat id
            "photo": image_url,  # image to send
            "caption": title+"\n"+refined_link+"\nType: DEAL OF THE DAY\nOffer Details:"+offer_details+"\nPrice:"+str(saleprice),
        }
        resp = requests.get(telegram_url, data=parameters)
        print("Telegram notification sent")

        sleep_time = random.randint(5, 100)
        time.sleep(sleep_time)


async def home(request):
    if request.method == "POST":
        soup = await getdata(daily_offers_url)
        asyncio.run(getdeals(soup))
        #messages.success(request, "Daily offers found, Sending to Telegram")
        # getdeals(soup)
    return render(request, 'offersapp/home.html')
