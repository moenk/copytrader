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
    userdatadir = tempfile.gettempdir() + os.sep + "wikifolio"
    print("User Data Dir:", userdatadir)
    chromeOptions.add_argument("user-data-dir=" + userdatadir)
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
    return driver


def wikifolio_login(driver, wf_username, wf_password):
    driver.get("https://www.wikifolio.com")
    coords = pyautogui.locateCenterOnScreen('but_login.png')
    try:
        pyautogui.moveRel(x=10, y=10)
        time.sleep(1)
        driver.find_element_by_xpath("//div[text()='Einverstanden']").click()
        time.sleep(1)
    except:
        pass
    if coords != None:
        pyperclip.copy(wf_username)
        pyautogui.click(coords)
        time.sleep(5)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.hotkey("tab")
        time.sleep(1)
        pyautogui.typewrite(wf_password)
        time.sleep(1)
        pyautogui.hotkey("enter")
        time.sleep(1)
    # fertig eingeloggt?
    el_login = driver.find_elements_by_xpath("//span[text()='Login']")
    if len(el_login) > 0:
        raise Exception("Wikifolio Login")


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

