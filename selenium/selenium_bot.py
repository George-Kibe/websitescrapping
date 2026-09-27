"""
Search a site and print the matching article summaries.

Usage:
    python selenium_bot.py                 # searches techwithtim.net for "test"
    python selenium_bot.py python --headless
"""

import argparse

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser import make_driver

URL = "https://techwithtim.net"


def main() -> None:
    parser = argparse.ArgumentParser(description="Search techwithtim.net with Selenium.")
    parser.add_argument("query", nargs="?", default="test")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    driver = make_driver(args.headless)
    try:
        driver.get(URL)
        print("Page title:", driver.title)

        search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "s")))
        search.send_keys(args.query, Keys.RETURN)

        main_area = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
        for article in main_area.find_elements(By.TAG_NAME, "article"):
            summaries = article.find_elements(By.CLASS_NAME, "entry-summary")
            print("-", (summaries[0] if summaries else article).text.strip()[:200])
    except TimeoutException:
        print("The page did not show the expected elements; the site layout may have changed.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
