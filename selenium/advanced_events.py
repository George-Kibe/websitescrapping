"""
Play Cookie Clicker: click the big cookie and buy upgrades when affordable.

Usage:
    python advanced_events.py [--clicks 5000]
"""

import argparse

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser import make_driver

URL = "https://orteil.dashnet.org/cookieclicker/"


def parse_number(text: str) -> int:
    """'1,234 cookies' -> 1234; 0 if the text has no number yet."""
    first = text.split(" ")[0].replace(",", "")
    return int(first) if first.isdigit() else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Cookie Clicker bot.")
    parser.add_argument("--clicks", type=int, default=5000)
    args = parser.parse_args()

    driver = make_driver()
    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 30)

        # First visit asks for a language.
        wait.until(EC.element_to_be_clickable((By.ID, "langSelect-EN"))).click()
        cookie = wait.until(EC.element_to_be_clickable((By.ID, "bigCookie")))
        cookie_count = driver.find_element(By.ID, "cookies")

        for _ in range(args.clicks):
            cookie.click()
            count = parse_number(cookie_count.text)
            # Check the two cheapest products, most expensive first.
            for product_id in ("productPrice1", "productPrice0"):
                try:
                    price = driver.find_element(By.ID, product_id)
                    if 0 < parse_number(price.text) <= count:
                        ActionChains(driver).move_to_element(price).click().perform()
                except StaleElementReferenceException:
                    pass  # the store re-rendered; try again on the next click
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
