import os
import time
import pyautogui
import pyperclip
import tempfile
from bs4 import BeautifulSoup
from selenium import webdriver


def wikifolio_browser_aufmachen():
    time.sleep(3)
    chromeService = webdriver.chrome.service.Service(executable_path='c:/webdriver/chromedriver.exe')
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
    return driver


def wikifolio_login(driver, wf_username, wf_password):
    pyautogui.moveTo(x=100,y=100)
    driver.get("https://www.wikifolio.com")
    pyautogui.moveTo(x=250,y=250,duration=2)
    driver.find_element_by_xpath("//div[text()='Einverstanden']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//button[@class='c-btn c-btn-link c-btn-link--grey-fossil js-login-button u-ml-3 gtm-nav-menu__login']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//input[@id='Username']").click()
    driver.find_element_by_xpath("//input[@id='Username']").send_keys(wf_username)
    time.sleep(2)
    pyperclip.paste()
    time.sleep(1)
    pyautogui.hotkey("tab")
    time.sleep(1)
    pyautogui.typewrite(wf_password)
    time.sleep(1)
    pyautogui.hotkey("enter")
    time.sleep(5)


def parse_portfolio(driver, portfolio, wf_dataframe):
    driver.get("https://www.wikifolio.com/de/de/w/" + portfolio)
    time.sleep(3)
    driver.find_element_by_xpath("//div[text()='Portfolio']").click()
    time.sleep(6)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find("tbody", attrs={"class": "c-portfolio__tbody"})
    for tr in table.find_all("tr"):
        isin_td = tr.find("div", attrs={"class": "c-portfolio__isin"})
        perc_td = tr.find("span", attrs={"class": "hidden-from-xs"})
        if isin_td:
            isin = isin_td.get_text()
            perc_td = perc_td.get_text()
            perc_td = perc_td.replace(",", ".")
            perc_td = perc_td.replace("<", "")
            perc_td = perc_td.replace("%", "")
            perc = float(perc_td.strip())
            wf_dataframe = wf_dataframe.append({"isin": isin, "perc": perc}, ignore_index=True)
    return wf_dataframe

