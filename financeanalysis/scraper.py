import time
from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By


def most_active_shares() -> list:
    url = "https://finance.yahoo.com/most-active"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    tab = soup.find("tbody")
    tickers = tab.find_all("a", class_="Fw(600) C($linkColor)")
    return [t.text for t in tickers]


def most_active_coin(top: int = 50) -> list:
    url = "https://coinmarketcap.com/all/views/all/"

    # duplicate code with (aichattelegrambot visa -> visa_checker)
    _options = webdriver.ChromeOptions()
    _options.add_argument("--headless")
    _options.add_argument("--no-sandbox")
    _options.add_argument("--disable-extensions")
    _options.add_argument("--disable-gpu")

    with webdriver.Chrome(options=_options) as _driver:
        _driver.get(url)
        screen_height = _driver.execute_script("return window.screen.height;")
        count = 1

        while True:
            _driver.execute_script(f"window.scrollTo(0, {screen_height}*{count});")
            count += 1
            time.sleep(1)

            scroll_height = _driver.execute_script("return document.body.scrollHeight;")

            if (screen_height) * count > scroll_height:
                break

        soup = BeautifulSoup(_driver.page_source, "html.parser")
        tab = soup.find("tbody")
        tickers = tab.find_all(
            "td",
            class_="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left "
            + "cmc-table__cell--hide-sm cmc-table__cell--sort-by__symbol",
        )
        return [t.text for t in tickers][:top]
