import requests
import pandas as pd
from fake_useragent import UserAgent
from pathlib import Path
import yfinance as yf
import time
from bs4 import BeautifulSoup
import urllib.parse


URL = "https://www.investing.com/indices"

INDEX_NAME_MAP = {
    "STOXX600": "stoxx-600-components",
}


class Investingcom_Index:

    def __init__(
        self,
        index_name: str,
        qlib_dir: [str, Path] = None
    ):
        if index_name not in INDEX_NAME_MAP:
            raise ValueError(f"Index '{index_name}' not supported.")
        self.index_name = index_name

        if qlib_dir is None:
            qlib_dir = Path(__file__).resolve().parent.joinpath("qlib_data")

        self.instruments_dir = (
            Path(qlib_dir)
            .expanduser()
            .resolve()
            .joinpath("instruments")
        )
        self.instruments_dir.mkdir(exist_ok=True, parents=True)

        self.target_url = f"{URL}/{INDEX_NAME_MAP[self.index_name.upper()]}"
        self._ua = UserAgent()

        # Simple cache for resolved tickers
        self._ticker_cache = {}


    # ----------------------------------------------------------------------
    # 1. SCRAPE COMPANY NAMES FROM INVESTING.COM
    # ----------------------------------------------------------------------
    def get_company_names(self):
        """
        Scrapes Investing.com for the list of company names.
        """
        headers = {"User-Agent": self._ua.random}

        resp = requests.get(self.target_url, timeout=10, headers=headers)
        resp.raise_for_status()
        
        try:
            tables = pd.read_html(resp.text)
        except ValueError:
            raise RuntimeError("Investing.com returned no tables. Possibly blocked or captcha triggered.")
            
        # Ensure there are enough tables
        if len(tables) < 2:
                raise RuntimeError(
                    f"Unexpected table structure from Investing.com. "
                    f"Expected at least 2 tables, got {len(tables)}."
                )
        df = tables[1]  # table with company names

        df.columns = [str(c).strip() for c in df.columns]

        name_col = [c for c in df.columns if "Name" in c][0]

        companies = df[[name_col]].rename(columns={name_col: "Company"})
        companies.dropna(inplace=True)

        return companies


    # ----------------------------------------------------------------------
    # 2. SCRAPE YAHOO FINANCE LOOKUP TO GET TICKER (ONE BY ONE)
    # ----------------------------------------------------------------------
    def yahoo_ticker_from_name(self, name):
        """
        Resolve a Yahoo Finance ticker from a company name using Yahoo Lookup.
        One-by-one version (no parallelization).
        """
        # Cache lookup
        if name in self._ticker_cache:
            return self._ticker_cache[name]

        time.sleep(0.2)  # avoid rate limits

        query = urllib.parse.quote(name)
        url = f"https://finance.yahoo.com/lookup/?s={query}"

        headers = {"User-Agent": self._ua.random}

        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")

            # First result in the lookup table
            link = soup.select_one('table tbody tr td a[href^="/quote/"]')
            if not link:
                return None

            href = link.get("href")  # "/quote/NESN.SW?p=NESN.SW"
            ticker = href.split("/quote/")[1].split("?")[0]

            # Save to cache
            self._ticker_cache[name] = ticker
            print("Found Ticker: " + ticker)
            return ticker

        except Exception as e:
            print(e)
            return None


    # ----------------------------------------------------------------------
    # 3. BUILD TICKER LIST (ONE BY ONE)
    # ----------------------------------------------------------------------
    def build_ticker_list(self):
        """
        Converts all company names into Yahoo Finance tickers (one by one).
        """
        companies = self.get_company_names()
        companies["Yahoo_Ticker"] = companies["Company"].apply(self.yahoo_ticker_from_name)
        companies = companies.dropna(subset=["Yahoo_Ticker"])
        return companies


    # ----------------------------------------------------------------------
    # 4. SAVE NEW TICKERS IN QLIB FORMAT
    # ----------------------------------------------------------------------
    def save_new_companies(
        self,
        start_date="2000-01-01",
        end_date="2099-01-01"
    ):
        """
        Exports a tab-separated CSV with ticker, start_date, end_date.
        """
        df = self.build_ticker_list()

        df = pd.DataFrame({
            "ticker": df["Yahoo_Ticker"],
            "start_date": start_date,
            "end_date": end_date
        })

        df.to_csv(
            self.instruments_dir.joinpath(f"{self.index_name.lower()}_only_new.txt"),
            sep="\t",
            index=False,
            header=None
        )
