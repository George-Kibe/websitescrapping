# pip install selenium
# download chromedriver from https://sites.google.com/chromium.org/driver/

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "E:\IDLE\Webscrapping\selenium\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://techwithtim.net"
url2 = "https://www.ticketmaster.com/"
driver.get(url)

# close a tab and close the whole browser
#driver.close() and driver.quit()
# driver title print(driver.title)
# page source print(driver.page_source)
search = driver.find_element_by_name("s")  # searchbox
search.send_keys("test")  # search name
search.send_keys(Keys.RETURN)  # hit enter
#main = driver.find_element_by_id("main")
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main")))
    print(main.text)
    articles = main.find_elements(by=By.TAG_NAME, value="article")
    for article in articles:
        header = article.find_element(by=By.CLASS_NAME, value="entry-summary")
        print(header)
finally:
    driver.quit()
