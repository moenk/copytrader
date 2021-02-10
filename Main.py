import os
import tempfile
import wikifolio
import onvista
import pandas as pd
import configparser
import colorama


# Const
ov_betrag = 1200
wf_portfolios = "wf00bb1912,wf0stwtech"


# config einlesen
config = configparser.ConfigParser()
config.read('../../Dokumente/smartbroker.ini')
wf_username = config['wikifolio']['username']
wf_password = config['wikifolio']['password']
ov_username = config['onvista']['username']
ov_password = config['onvista']['password']
portfolios = wf_portfolios.split(",")

# tempfiles sicherstellen
mytempfolder = tempfile.gettempdir()
wf_datei = mytempfolder + os.sep + "portfolio.csv"
ov_datei = mytempfolder + os.sep + "depot.csv"
print("Wikifolio:", wf_datei)
if os.path.isfile(wf_datei):
    os.remove(wf_datei)
print("Onvista:", ov_datei)
if os.path.isfile(ov_datei):
    os.remove(ov_datei)

# und los gehts
driver = wikifolio.wikifolio_browser_aufmachen()
wikifolio.wikifolio_login(driver, wf_username, wf_password)
wf_dataframe = pd.DataFrame(columns=['isin', 'perc'])

# alle portfolios abfragen
for portfolio in portfolios:
    wf_dataframe = wikifolio.parse_portfolio(driver, portfolio, wf_dataframe)

# aggregieren der isin und anteile summieren
wf_dataframe = wf_dataframe.groupby("isin").sum()
# wf_dataframe = wf_dataframe[wf_dataframe['perc'] >= 5.0]
wf_dataframe = wf_dataframe.sort_values(by='perc', ascending=False)

# und ausgabe
print("*** Wikifolio Positionen")
print(wf_dataframe)
wf_dataframe.to_csv(wf_datei)

# und raus aus wikifolio
driver.close()
driver.quit()

# onvista depot abholen
driver = onvista.onvista_browser_aufmachen()
driver.get("https://webtrading.onvista-bank.de/login")
onvista.onvista_login_desktop(driver, ov_username, ov_password)
onvista.onvista_close_all(driver)
onvista.onvista_download_depot(driver, ov_datei)

# lesen depot in DF
ov_dataframe = pd.read_csv(ov_datei, delimiter=";", skiprows=5)
ov_dataframe = ov_dataframe.dropna()
print("\n*** Onvista Depot")
print(ov_dataframe)

# lesen portfolio in WF
wf_dataframe = pd.read_csv(wf_datei)
print(wf_dataframe)

# Verkaufen durchfuehren
print("\n*** Abwicklung Verkauf")
for index, row in ov_dataframe.iterrows():
    ov_isin = row['ISIN']
    ov_anzahl = int(row['Bestand'])
    found = wf_dataframe[wf_dataframe['isin'] == ov_isin]
    if (len(found) == 0) or (float(found['perc']) < 3.0):
        print(colorama.Fore.LIGHTRED_EX, "Verkaufen:", ov_isin, row['Name'], ov_anzahl, colorama.Style.RESET_ALL)
        # onvista.onvista_close_all(driver)
        # onvista.onvista_kaufen(driver, ov_isin, ov_anzahl)
    else:
        print(colorama.Fore.LIGHTYELLOW_EX, "Halten:", ov_isin, row['Name'], ov_anzahl, colorama.Style.RESET_ALL)

# Kaufen durchfuehren
print("\n*** Abwicklung Kauf")
for index, row in wf_dataframe.iterrows():
    wf_isin = row['isin']
    wf_perc = row['perc']
    if wf_perc >= 5.0:
        found = ov_dataframe[ov_dataframe['ISIN'] == wf_isin]
        if len(found) == 0:
            print(colorama.Fore.LIGHTGREEN_EX, "Kaufen:",wf_isin, colorama.Style.RESET_ALL)
            # onvista.onvista_close_all(driver)
            # onvista.onvista_kaufen(driver, wf_isin, ov_betrag)
        else:
            print(colorama.Fore.LIGHTYELLOW_EX, "Halten:",wf_isin, colorama.Style.RESET_ALL)
    else:
        print("Ignoriert:", wf_isin)

# und onvista schliessen
driver.close()
driver.quit()
