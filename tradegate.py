import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_tradegate_price(isin):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    data = requests.get('https://www.tradegate.de/orderbuch.php?isin=' + isin, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    longprice = soup.find("td", attrs={"class": "longprice"}).get_text()
    longprice = longprice.replace(" ","")
    longprice = longprice.replace(".","")
    longprice = longprice.replace(",",".")
    price = float(longprice.strip())
    return price

