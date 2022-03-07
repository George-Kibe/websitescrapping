from http.cookiejar import Cookie
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "E:\IDLE\Webscrapping\selenium\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://orteil.dashnet.org/cookieclicker/"
driver.get(url)
driver.implicitly_wait(10)

cookie = driver.find_element(by=By.ID, value="bigCookie")
cookie_count = driver.find_element(by=By.ID, value="cookies")
items = [driver.find_element(by=By.ID, value="productPrice" + str(i))
         for i in range(1, -1, -1)]
print(items)
actions = ActionChains(driver)
actions.click(cookie)


for i in range(5000):
    actions.perform()
    count = int(cookie_count.text.split(" ")[0])
    for item in items:
        value = int(item.text)
        if value <= count:
            upgrade_actions = ActionChains(driver)
            upgrade_actions.move_to_element(item)
            upgrade_actions.click()
            upgrade_actions.perform()
