import time
import pandas as pd
from pathlib import Path
import requests
import urllib.parse
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.investing.com/indices"

INDEX_NAME_MAP = {
    "STOXX600": "stoxx-600-components",
}

YAHOO_EXCHANGE_SUFFIX = {
    "United States": "",
    "United Kingdom": ".L",
    "UK": ".L",
    "GB": ".L",
    "France": ".PA",
    "Germany": ".DE",
    "Spain": ".MC",
    "Italy": ".MI",
    "Switzerland": ".SW",
    "Netherlands": ".AS",
    "Belgium": ".BR",
    "Sweden": ".ST",
    "Finland": ".HE",
    "Denmark": ".CO",
    "Norway": ".OL",
    "Ireland": ".IR",
    "Portugal": ".LS",
    "Austria": ".VI",
    "Poland": ".WA",
    "Luxembourg": ".LU",
}


class Investingcom_Index:

    def __init__(self, index_name: str):
        if index_name not in INDEX_NAME_MAP:
            raise ValueError(f"Index '{index_name}' not supported.")
        self.index_name = index_name

        self.target_url = f"{URL}/{INDEX_NAME_MAP[self.index_name.upper()]}"

        self._ticker_cache = {}


    # ----------------------------------------------------------
    # ⭐ Selenium-based component scraper
    # ----------------------------------------------------------
    def _init_driver(self, headless=True):
        options = Options()

        if headless:
            options.add_argument("--headless=new")

        # Viewport estrecho para que aparezca el ticker
        options.add_argument("--window-size=480,1000")

        # Evitar bloqueos anti-bot
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        return webdriver.Chrome(options=options)


    def get_components(self):
        driver = self._init_driver(headless=False)
        driver.get(self.target_url)

        wait = WebDriverWait(driver, 20)

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table tbody tr")
            )
        )
        rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

        print(f"Found {len(rows)} rows")

        companies, tickers, hrefs, countries = [], [], [], []

        for row in rows:
            try:
                link = row.find_element(By.CSS_SELECTOR, "a[href*='/equities/']")
                
                name = link.text.split("\n")[0].strip()
                href = link.get_attribute("href")

                if name is None or name == "": continue
            except:
                continue

            # ticker
            try:
                ticker_el = row.find_element(By.CSS_SELECTOR, "span.text-secondary")
                ticker = ticker_el.text.strip().upper()
            except:
                ticker = None

            # país
            try:
                flag_el = row.find_element(By.CSS_SELECTOR, "span[data-test^='flag-']")
                country = flag_el.get_attribute("title") or flag_el.get_attribute("aria-label")
            except:
                country = None

            companies.append(name)
            tickers.append(ticker)
            hrefs.append(href)
            countries.append(country)

        driver.quit()

        df = pd.DataFrame({
            "company_name": companies,
            "investing_ticker": tickers,
            "href": hrefs,
            "country": countries
        })

        return df

    # ----------------------------------------------------------

    def yahoo_suffix_from_country(self, country):
        if not country:
            return None
        for key, suffix in YAHOO_EXCHANGE_SUFFIX.items():
            if key.lower() in country.lower():
                return suffix
        return None

    def build_ticker_list(self):
        df = self.get_components()
        df["yahoo_suffix"] = df["country"].apply(self.yahoo_suffix_from_country)
        df["yahoo_ticker"] = df["investing_ticker"] + df["yahoo_suffix"]
        return df
