from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore


def most_active_shares() -> list:
    url = "https://finance.yahoo.com/most-active"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    tab = soup.find("tbody")
    tickers = tab.find_all("a", class_="Fw(600) C($linkColor)")
    return [t.text for t in tickers]
