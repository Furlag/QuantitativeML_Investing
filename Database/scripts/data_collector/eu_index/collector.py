# STOXX Europe 600 Index Collector
#
# Scrapes STOXX 600 components from investing.com and resolves
# Yahoo Finance ticker symbols for integration with the Qlib data pipeline.
#
# Usage (CLI via fire):
#     python collector.py save_new_companies --qlib_dir ../../qlib_data_EU
#     python collector.py save_full_mapping  --qlib_dir ../../qlib_data_EU

import re
import sys
import json
import time
from pathlib import Path
from functools import partial
from io import StringIO
from typing import Dict, List, Optional, Tuple

import fire
import requests
import pandas as pd
from tqdm import tqdm
from loguru import logger
from fake_useragent import UserAgent


CUR_DIR = Path(__file__).resolve().parent
sys.path.append(str(CUR_DIR.parent.parent))

from data_collector.index import IndexBase
from data_collector.utils import deco_retry


# ---------------------------------------------------------------------------
#  Yahoo Finance exchange-suffix mapping for European exchanges
# ---------------------------------------------------------------------------
YAHOO_EXCHANGE_SUFFIX = {
    # UK
    "London":               ".L",
    "LSE":                  ".L",
    "London Stock Exchange": ".L",
    # Germany
    "Frankfurt":            ".DE",
    "XETRA":                ".DE",
    "Xetra":                ".DE",
    # France
    "Paris":                ".PA",
    "Euronext Paris":       ".PA",
    # Netherlands
    "Amsterdam":            ".AS",
    "Euronext Amsterdam":   ".AS",
    # Belgium
    "Brussels":             ".BR",
    "Euronext Brussels":    ".BR",
    # Italy
    "Milan":                ".MI",
    "Borsa Italiana":       ".MI",
    # Spain
    "Madrid":               ".MC",
    "BME":                  ".MC",
    # Switzerland
    "Zurich":               ".SW",
    "SIX":                  ".SW",
    "Swiss Exchange":       ".SW",
    # Sweden
    "Stockholm":            ".ST",
    "OMX Stockholm":        ".ST",
    "Nasdaq Stockholm":     ".ST",
    # Finland
    "Helsinki":             ".HE",
    "OMX Helsinki":         ".HE",
    "Nasdaq Helsinki":      ".HE",
    # Denmark
    "Copenhagen":           ".CO",
    "OMX Copenhagen":       ".CO",
    "Nasdaq Copenhagen":    ".CO",
    # Norway
    "Oslo":                 ".OL",
    "Oslo Bors":            ".OL",
    "Oslo Bors":             ".OL",
    # Ireland
    "Dublin":               ".IR",
    "Irish SE":             ".IR",
    "Euronext Dublin":      ".IR",
    # Portugal
    "Lisbon":               ".LS",
    "Euronext Lisbon":      ".LS",
    # Austria
    "Vienna":               ".VI",
    "Wiener Boerse":        ".VI",
    # Poland
    "Warsaw":               ".WA",
    "WSE":                  ".WA",
    # Luxembourg
    "Luxembourg":           ".LU",
}

# Valid European exchange suffixes (used to filter Yahoo search results)
VALID_EU_SUFFIXES = set(YAHOO_EXCHANGE_SUFFIX.values())

# Yahoo Finance lookup endpoint
YAHOO_SEARCH_URL = "https://query2.finance.yahoo.com/v1/finance/search"


# =========================================================================
#  STOXX 600 Index class
# =========================================================================

class STOXX600Index(IndexBase):
    """Collector for STOXX Europe 600 index components.

    Workflow
    --------
    1. Scrape constituent list from investing.com
    2. For each company, resolve its Yahoo Finance ticker via the Yahoo
       search API (``query2.finance.yahoo.com/v1/finance/search``)
    3. Persist the result as a Qlib-compatible instruments file
       (``stoxx600_only_new.txt``) *and* a full mapping CSV.

    The class follows the same conventions as ``WIKIIndex`` / ``SP500Index``
    in ``us_index/collector.py`` so that it plugs into the existing data
    pipeline (download -> normalize -> dump_bin).
    """

    INST_PREFIX = ""
    COMPONENTS_URL = "https://www.investing.com/indices/stoxx-600-components"

    def __init__(
        self,
        index_name: str = "STOXX600",
        qlib_dir: [str, Path] = None,
        freq: str = "day",
        request_retry: int = 5,
        retry_sleep: int = 3,
        yahoo_search_delay: float = 0.35,
    ):
        """
        Parameters
        ----------
        index_name : str
            Name used for the output instruments file (default ``STOXX600``).
        qlib_dir : str or Path
            Root Qlib data directory.  Instruments are saved under
            ``{qlib_dir}/instruments/``.
        freq : str
            ``"day"`` or ``"1min"``.
        request_retry : int
            Number of retries for HTTP requests.
        retry_sleep : int
            Seconds to sleep between retries.
        yahoo_search_delay : float
            Seconds to wait between Yahoo Finance search API calls to
            avoid rate-limiting.
        """
        super().__init__(
            index_name=index_name,
            qlib_dir=qlib_dir,
            freq=freq,
            request_retry=request_retry,
            retry_sleep=retry_sleep,
        )
        self._ua = UserAgent()
        self._yahoo_search_delay = yahoo_search_delay
        self._session = requests.Session()

    # ------------------------------------------------------------------
    #  IndexBase abstract-method implementations
    # ------------------------------------------------------------------

    @property
    def bench_start_date(self) -> pd.Timestamp:
        return pd.Timestamp("2000-01-01")

    @property
    def calendar_list(self) -> List[pd.Timestamp]:
        """EU trading calendar (proxied via ^STOXX or ^GSPC)."""
        _calendar_list = getattr(self, "_calendar_list", None)
        if _calendar_list is None:
            from data_collector.utils import get_calendar_list
            _calendar_list = list(
                filter(lambda x: x >= self.bench_start_date, get_calendar_list("US_ALL"))
            )
            setattr(self, "_calendar_list", _calendar_list)
        return _calendar_list

    def get_changes(self) -> pd.DataFrame:
        """Historical constituent changes are not available for STOXX 600."""
        logger.warning("STOXX 600 historical changes are not available from this source.")
        return None

    def format_datetime(self, inst_df: pd.DataFrame) -> pd.DataFrame:
        if self.freq != "day":
            inst_df[self.END_DATE_FIELD] = inst_df[self.END_DATE_FIELD].apply(
                lambda x: (
                    pd.Timestamp(x) + pd.Timedelta(hours=23, minutes=59)
                ).strftime("%Y-%m-%d %H:%M:%S")
            )
        return inst_df

    def parse_instruments(self):
        logger.warning("STOXX 600 historical changes tracking is not supported.")

    # ==================================================================
    #  1. SCRAPING - investing.com
    # ==================================================================

    def _get_headers(self) -> dict:
        return {
            "User-Agent": self._ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.investing.com/",
        }

    def _get_ajax_headers(self) -> dict:
        h = self._get_headers()
        h.update({
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded",
        })
        return h

    @deco_retry
    def _request_components_page(self, page: int = 1) -> requests.Response:
        """Fetch a single page of STOXX 600 components from investing.com."""
        if page == 1:
            resp = self._session.get(
                self.COMPONENTS_URL, headers=self._get_headers(), timeout=30
            )
        else:
            # Subsequent pages use an AJAX POST
            resp = self._session.post(
                self.COMPONENTS_URL,
                headers=self._get_ajax_headers(),
                data={
                    "cID": "0",
                    "pNo": str(page),
                    "sortBy": "0",
                    "sortOrder": "asc",
                    "is498Group": "false",
                },
                timeout=30,
            )

        if resp.status_code != 200:
            raise ValueError(f"investing.com returned HTTP {resp.status_code}")
        return resp

    def _parse_components_html(self, html: str) -> pd.DataFrame:
        """Extract the components table from an investing.com HTML response."""
        try:
            tables = pd.read_html(StringIO(html))
            if not tables:
                return pd.DataFrame()

            # Pick the table that looks like a constituents list
            for df in tables:
                cols = [str(c).lower() for c in df.columns]
                if any(kw in cols for kw in ("name", "symbol", "company")):
                    return df

            # Fallback: largest table
            return max(tables, key=len)
        except Exception as exc:
            logger.warning(f"Could not parse investing.com HTML: {exc}")
            return pd.DataFrame()

    def scrape_components(self, use_cache: bool = True) -> pd.DataFrame:
        """Scrape all STOXX 600 components from investing.com.

        Returns a DataFrame whose columns (normalised to lowercase/underscore)
        typically include ``name``, ``symbol``, and exchange-related info.

        Results are cached locally for 7 days.
        """
        cache_path = self.cache_dir / "stoxx600_raw_components.csv"

        if use_cache and cache_path.exists():
            age_days = (time.time() - cache_path.stat().st_mtime) / 86_400
            if age_days < 7:
                logger.info(f"Using cached components ({age_days:.1f} days old)")
                return pd.read_csv(cache_path)

        logger.info("Scraping STOXX 600 components from investing.com ...")
        all_dfs: List[pd.DataFrame] = []

        # ---- page 1 ----
        resp = self._request_components_page(page=1)
        df = self._parse_components_html(resp.text)
        if df.empty:
            raise ValueError(
                "Could not parse STOXX 600 components.  "
                "investing.com may have changed its layout or is blocking the request.  "
                "You can fall back to STOXX600Index.load_components_from_csv()."
            )
        all_dfs.append(df)
        logger.info(f"  page 1 -> {len(df)} rows")

        # ---- additional pages (if <~600 rows on page 1) ----
        if len(df) < 580:
            for page in range(2, 12):        # safety cap
                time.sleep(1.5)
                try:
                    resp = self._request_components_page(page=page)
                    page_df = self._parse_components_html(resp.text)
                    if page_df.empty:
                        break
                    all_dfs.append(page_df)
                    logger.info(f"  page {page} -> {len(page_df)} rows")
                    if sum(len(d) for d in all_dfs) >= 600:
                        break
                except Exception as exc:
                    logger.warning(f"  page {page} failed: {exc}")
                    break

        result = pd.concat(all_dfs, ignore_index=True).drop_duplicates()

        # Normalise column names -> lowercase, underscores, no dots/percent
        result.columns = [
            re.sub(r"[^a-z0-9_]", "", str(c).strip().lower().replace(" ", "_"))
            for c in result.columns
        ]

        logger.info(f"Total components scraped: {len(result)}")
        result.to_csv(cache_path, index=False)
        return result

    # ==================================================================
    #  2. YAHOO FINANCE TICKER RESOLUTION
    # ==================================================================

    def _search_yahoo(self, query: str) -> Optional[Dict]:
        """Hit Yahoo Finance search API and return the best EU equity match."""
        try:
            resp = requests.get(
                YAHOO_SEARCH_URL,
                params={
                    "q": query,
                    "quotesCount": 10,
                    "newsCount": 0,
                    "listsCount": 0,
                    "enableFuzzyQuery": True,
                },
                headers={"User-Agent": self._ua.random},
                timeout=10,
            )
            if resp.status_code != 200:
                return None

            quotes = resp.json().get("quotes", [])
            if not quotes:
                return None

            # Prefer an EQUITY on a European exchange
            for q in quotes:
                if q.get("quoteType") == "EQUITY":
                    sym = q.get("symbol", "")
                    if any(sym.endswith(s) for s in VALID_EU_SUFFIXES):
                        return q

            # Fallback: first equity regardless of exchange
            for q in quotes:
                if q.get("quoteType") == "EQUITY":
                    return q

            return quotes[0]
        except Exception as exc:
            logger.debug(f"Yahoo search failed for '{query}': {exc}")
            return None

    def _build_ticker_from_suffix(
        self, investing_symbol: str, exchange: str
    ) -> Optional[str]:
        """Construct a Yahoo ticker from ``SYMBOL + .XX`` suffix."""
        if not investing_symbol or not exchange:
            return None

        suffix = YAHOO_EXCHANGE_SUFFIX.get(exchange)
        if suffix:
            return f"{investing_symbol}{suffix}"

        # Partial / fuzzy match on exchange name
        ex_lower = exchange.lower()
        for key, sfx in YAHOO_EXCHANGE_SUFFIX.items():
            if key.lower() in ex_lower or ex_lower in key.lower():
                return f"{investing_symbol}{sfx}"
        return None

    # ----- helper: find a column by candidate names -----

    @staticmethod
    def _find_col(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
        lower_map = {c.lower(): c for c in df.columns}
        for cand in candidates:
            if cand.lower() in lower_map:
                return lower_map[cand.lower()]
        return None

    # ----- batch resolution -----

    def resolve_yahoo_tickers(self, components: pd.DataFrame) -> pd.DataFrame:
        """Add ``yahoo_ticker`` and ``resolution_method`` columns.

        Resolution strategy (per company, in order):
          1. Cached result from a previous run
          2. Yahoo search by **company name** -> prefer EU equity
          3. Construct ticker from investing.com symbol + exchange suffix
          4. Yahoo search by **investing.com symbol**

        Parameters
        ----------
        components : pd.DataFrame
            Must contain a *name* column; *symbol* and *exchange* are optional.

        Returns
        -------
        pd.DataFrame
            Same DataFrame with two extra columns.
        """
        cache_path = self.cache_dir / "stoxx600_yahoo_mapping.csv"

        # Load earlier cache for incremental runs
        cached: Dict[str, Dict] = {}
        if cache_path.exists():
            for _, row in pd.read_csv(cache_path).iterrows():
                if pd.notna(row.get("yahoo_ticker")):
                    cached[row["name"]] = {
                        "yahoo_ticker": row["yahoo_ticker"],
                        "resolution_method": row.get("resolution_method", "cached"),
                    }

        name_col = self._find_col(components, ["name", "company", "company_name"])
        sym_col  = self._find_col(components, ["symbol", "ticker", "code"])
        exch_col = self._find_col(components, ["exchange", "market", "stock_exchange"])

        if name_col is None:
            raise ValueError(
                f"Cannot identify a company-name column.  Columns: {list(components.columns)}"
            )

        tickers: List[Optional[str]] = []
        methods: List[str] = []
        resolved_count = 0

        for _, row in tqdm(
            components.iterrows(), total=len(components), desc="Resolving Yahoo tickers"
        ):
            company  = str(row[name_col]).strip()
            inv_sym  = str(row[sym_col]).strip() if sym_col else ""
            exchange = str(row[exch_col]).strip() if exch_col else ""

            # 1. cache
            if company in cached:
                tickers.append(cached[company]["yahoo_ticker"])
                methods.append("cached")
                resolved_count += 1
                continue

            ticker: Optional[str] = None
            method = "unresolved"

            # 2. Yahoo search by name
            hit = self._search_yahoo(company)
            if hit:
                ticker = hit.get("symbol")
                method = "yahoo_search_name"

            # 3. suffix construction
            if ticker is None and inv_sym and exchange:
                constructed = self._build_ticker_from_suffix(inv_sym, exchange)
                if constructed:
                    ticker = constructed
                    method = "exchange_suffix"

            # 4. Yahoo search by investing.com symbol
            if ticker is None and inv_sym:
                time.sleep(self._yahoo_search_delay)
                hit = self._search_yahoo(inv_sym)
                if hit:
                    ticker = hit.get("symbol")
                    method = "yahoo_search_symbol"

            tickers.append(ticker)
            methods.append(method)
            if ticker:
                resolved_count += 1
            else:
                logger.warning(f"  [X] unresolved: {company}  ({inv_sym} / {exchange})")

            time.sleep(self._yahoo_search_delay)

        components = components.copy()
        components["yahoo_ticker"] = tickers
        components["resolution_method"] = methods

        pct = resolved_count / len(components) * 100 if len(components) else 0
        logger.info(f"Resolved {resolved_count}/{len(components)} tickers ({pct:.1f}%)")

        # Persist mapping
        mapping = components[[name_col, "yahoo_ticker", "resolution_method"]].copy()
        mapping.columns = ["name", "yahoo_ticker", "resolution_method"]
        mapping.to_csv(cache_path, index=False)

        return components

    # ==================================================================
    #  3. INSTRUMENTS FILE
    # ==================================================================

    def get_new_companies(self) -> pd.DataFrame:
        """Return current STOXX 600 constituents as a Qlib instruments DF.

        Columns: ``symbol  start_date  end_date``
        where *symbol* is the Yahoo Finance ticker.
        """
        logger.info("Building STOXX 600 instruments list ...")

        components = self.scrape_components()
        components = self.resolve_yahoo_tickers(components)

        resolved = components[components["yahoo_ticker"].notna()].copy()
        if resolved.empty:
            raise ValueError("No tickers could be resolved — check network / cache.")

        inst = pd.DataFrame({
            self.SYMBOL_FIELD_NAME: resolved["yahoo_ticker"].values,
            self.START_DATE_FIELD:  self.bench_start_date,
            self.END_DATE_FIELD:    self.DEFAULT_END_DATE,
        })
        inst[self.SYMBOL_FIELD_NAME] = inst[self.SYMBOL_FIELD_NAME].str.strip()
        inst = inst.drop_duplicates(subset=[self.SYMBOL_FIELD_NAME])

        logger.info(f"Instruments: {len(inst)} tickers ready")
        return inst

    def save_new_companies(self):
        """Save ``stoxx600_only_new.txt`` under ``{qlib_dir}/instruments/``."""
        super().save_new_companies()
        out = self.instruments_dir / f"{self.index_name.lower()}_only_new.txt"
        logger.info(f"Saved -> {out}")

    def save_full_mapping(self):
        """Save **both** the instruments txt *and* a detailed CSV mapping.

        The CSV (``stoxx600_full_mapping.csv``) includes company name,
        investing.com symbol, exchange, Yahoo ticker, and resolution method.
        """
        components = self.scrape_components()
        components = self.resolve_yahoo_tickers(components)

        csv_path = self.instruments_dir / "stoxx600_full_mapping.csv"
        components.to_csv(csv_path, index=False)
        logger.info(f"Full mapping -> {csv_path}")

        # Also write the instruments txt
        self.save_new_companies()

        # Report unresolved
        unresolved = components[components["yahoo_ticker"].isna()]
        if not unresolved.empty:
            name_col = self._find_col(components, ["name", "company", "company_name"])
            logger.warning(f"{len(unresolved)} ticker(s) remain unresolved:")
            for _, row in unresolved.iterrows():
                logger.warning(f"  - {row[name_col]}")

    # ==================================================================
    #  4. FALLBACK - load from a pre-built CSV
    # ==================================================================

    @staticmethod
    def load_components_from_csv(csv_path: [str, Path]) -> pd.DataFrame:
        """Load STOXX 600 components from a manually prepared CSV.

        Useful when investing.com blocks automated requests.
        The CSV needs at least a ``name`` column; ``symbol`` and
        ``exchange`` columns improve resolution accuracy.
        """
        return pd.read_csv(csv_path)


# =========================================================================
#  CLI entry-point  (python collector.py <method> --qlib_dir ...)
# ===========================================================================

def get_stoxx600(
    qlib_dir: str = None,
    request_retry: int = 5,
    retry_sleep: int = 3,
):
    """Return a configured ``STOXX600Index`` instance for use with ``fire``."""
    return STOXX600Index(
        index_name="STOXX600",
        qlib_dir=qlib_dir,
        request_retry=request_retry,
        retry_sleep=retry_sleep,
    )


if __name__ == "__main__":
    fire.Fire(get_stoxx600)
