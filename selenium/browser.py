"""Shared Chrome setup. Selenium Manager downloads a matching chromedriver automatically."""

from selenium import webdriver


def make_driver(headless: bool = False) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=options)
