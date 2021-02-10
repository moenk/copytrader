import os
import time
import pyautogui
import tempfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tradegate import get_tradegate_price


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def wait_for_xpath_element(driver, xpathstr):
    fertig = False
    versuch = 0
    while not(fertig) and (versuch<100):
        try:
            el=driver.find_element_by_xpath(xpathstr)
            fertig = True
        except:
            versuch = versuch+1
            if (versuch > 60):
                raise Exception('Timeout waiting for: '+xpathstr)
            fertig = False
        time.sleep(1)
    return el

def onvista_browser_aufmachen():
    time.sleep(3)
    chromeService = webdriver.chrome.service.Service(executable_path='c:/webdriver/chromedriver.exe')
    chromeOptions = webdriver.ChromeOptions()
    userdatadir = tempfile.gettempdir() + os.sep + "onvista"
    print("User Data Dir:", userdatadir)
    chromeOptions.add_argument("user-data-dir=" + userdatadir)
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_experimental_option("prefs", {"download.prompt_for_download": True})
    driver = webdriver.Chrome(service=chromeService, options=chromeOptions)
    return driver


def onvista_login_desktop(driver, username, password):
    time.sleep(3)
    el = driver.find_element_by_link_text("Sicherheitstastatur ausblenden")
    el.send_keys(Keys.RETURN)
    time.sleep(3)
    el= driver.find_element_by_name('password')
    for char in password:
        el.send_keys(char)
        time.sleep(0.2)
    el= driver.find_element_by_name('login')
    for char in username:
        el.send_keys(char)
        time.sleep(0.2)
    time.sleep(3)
    el = driver.find_element_by_id('performLoginButton')
    el.send_keys(Keys.RETURN)


def onvista_download_depot(driver, ov_file):
    time.sleep(5)
    driver.find_element_by_xpath("//a[text()='Depot & Konto ']").click()
    driver.find_element_by_xpath("//a[@block='bank-konto']").click()
    time.sleep(5)
    try:
        driver.find_element_by_xpath("//button[@ng-show='paginationData.displayShowAllButton']").click()
        time.sleep(3)
    except:
        pass
    driver.find_element_by_xpath("//div[@class='dropdown dropdown-boxmenu']").click()
    driver.find_element_by_xpath("//a[@class='icon-export--right']").click()
    time.sleep(3)
    pyautogui.hotkey('alt', 'n')
    pyautogui.write(ov_file)
    time.sleep(3)
    pyautogui.hotkey('enter')
    time.sleep(3)


def onvista_close_all(driver):
    time.sleep(5)
    fertig = False
    while not(fertig):
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//div[@class='dropdown dropdown-boxmenu']").click()
            driver.find_element_by_xpath("//a[@class='icon-close--right']").click()
        except:
            fertig = True


def onvista_quick_order(driver, quickorder):
    time.sleep(5)
    driver.find_element_by_xpath("//a[text()='Handeln ']").click()
    driver.find_element_by_xpath("//a[@block='trading-quick-order']").click()
    time.sleep(2)
    print("*** Order:", quickorder)
    el = driver.find_element_by_xpath("//*[@placeholder='Bitte geben Sie hier Ihre Quick-Order ein.']")
    for char in quickorder:
        el.send_keys(char)
        time.sleep(0.2)
    time.sleep(3)
    # abschicken
    el = driver.find_element_by_xpath("//*[@class='btn btn-primary btn-sm pull-right']")
    el.send_keys(Keys.RETURN)
    time.sleep(5)
    # bestaetigung klicken
    el = driver.find_element_by_xpath("//*[@class='btn btn-primary btn-sm']")
    el.send_keys(Keys.RETURN)
    time.sleep(10)
    # kein druck
    el = driver.find_element_by_xpath("//*[@class='btn btn-default btn-sm icon-cancel']")
    el.click()


def onvista_verkaufen(driver, isin, anzahl):
    time.sleep(5)
    print("*** Verkaufen:", isin)
    markt = "EDE"
    quickorder = "V;" + markt + ";" + isin + ";" + str(anzahl) + ";M"
    onvista_quick_order(driver, quickorder)


def onvista_kaufen(driver, isin, betrag):
    time.sleep(5)
    preis = get_tradegate_price(isin)
    anzahl = int(betrag // preis)
    print("*** Kaufen:", isin)
    print("Preis:", preis)
    print("Anzahl:", anzahl)
    if anzahl > 0:
        if isin.upper().startswith("DE"):
            markt = "EDE"
        else:
            markt = "EDF"
        quickorder = "K;" + markt + ";" + isin + ";" + str(anzahl) + ";M"
        onvista_quick_order(driver, quickorder)

