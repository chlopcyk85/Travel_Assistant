import requests
from bs4 import BeautifulSoup


class Petrol:
    url_eur = "https://www.bankier.pl/waluty/kursy-walut/nbp/EUR"
    url_petrol = "https://www.autocentrum.pl/paliwa/ceny-paliw/on/"
    page_petrol = requests.get(url_petrol)
    soup = BeautifulSoup(page_petrol.text, "html.parser")

    # E95
    cena_95 = (
        soup.find("div", class_="price").text.replace("zł", "").replace(",", ".").strip()
    )
    # E98
    header_98 = soup.find("h3", class_="fuel-header", string="98")
    cena_element98 = header_98.find_next_sibling("div", class_="price")
    cena_98 = (
        cena_element98.get_text(strip=True).replace("zł", "").replace(",", ".").strip()
    )
    # ON
    header_ON = soup.find("h3", class_="fuel-header", string="ON")
    cena_elementON = header_ON.find_next_sibling("div", class_="price")
    cena_ON = (
        cena_elementON.get_text(strip=True).replace("zł", "").replace(",", ".").strip()
    )
    # LPG
    header_LPG = soup.find("h3", class_="fuel-header", string="LPG")
    cena_elementLPG = header_LPG.find_next_sibling("div", class_="price")
    cena_LPG = (
    cena_elementLPG.get_text(strip=True).replace("zł", "").replace(",", ".").strip())

