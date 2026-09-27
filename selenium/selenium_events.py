"""
Click through links and use the browser's back/forward history.

Usage:
    python selenium_events.py [--headless]
"""

import argparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser import make_driver

URL = "https://techwithtim.net"


def click_link(driver, text: str, timeout: int = 10) -> None:
    link = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, text)))
    link.click()
    print("Opened:", driver.title)


def main() -> None:
    parser = argparse.ArgumentParser(description="Selenium navigation demo.")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    driver = make_driver(args.headless)
    try:
        driver.get(URL)
        click_link(driver, "Python Programming")
        click_link(driver, "Beginner Python Tutorials")

        driver.back()
        print("Back to:", driver.title)
        driver.forward()
        print("Forward to:", driver.title)
    except TimeoutException:
        print("A link was not found in time; the site layout may have changed.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
