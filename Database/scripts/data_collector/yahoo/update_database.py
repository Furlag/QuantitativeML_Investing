from pathlib import Path
import sys, shutil

import pandas as pd
from loguru import logger
from datetime import datetime, timedelta

# Relative imports
from collector import YahooCollectorUS, Run


# Append dump_bin to sys.path
CUR_DIR = Path().resolve()
sys.path.append(str(CUR_DIR.parent.parent))

from dump_bin import DumpDataAll, DumpDataUpdate, DumpDataFix


# Target database
qlib_dir = Path().resolve().parent.parent.parent.joinpath("qlib_data_US")
qlib_dir

# --------------------------------------------------------------------------------------------

# Rewrite YahooCollectorUS.get_instrument_list
tickers_sp500 = pd.read_csv(qlib_dir.joinpath("instruments/sp500_only_new.txt"), sep='\t', header=None, names=['symbol', 'start_date', 'end_date'])
tickers_sp400 = pd.read_csv(qlib_dir.joinpath("instruments/sp400_only_new.txt"), sep='\t', header=None, names=['symbol', 'start_date', 'end_date'])


tickers = (
    ['^GSPC']  # '^MID', '^SP600'
    + tickers_sp500['symbol'].tolist()
    + tickers_sp400['symbol'].tolist()
)
tickers = [ticker.replace('.', '-') for ticker in tickers]


def f(self):

    logger.info("get US stock symbols......")

    symbols = tickers

    logger.info(f"get {len(symbols)} symbols.")
    return symbols


YahooCollectorUS.get_instrument_list = f

# --------------------------------------------------------------------------------------------

r = Run(region="US", interval="1d")


r.download_data(
    max_collector_count=2,
    delay=0.5,
    start=(datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'),
    end=(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
)


r.normalize_data()

# --------------------------------------------------------------------------------------------

# Dump
_dump = DumpDataAll(
    data_path=Path().resolve().joinpath("source"),
    qlib_dir=qlib_dir,
    exclude_fields="symbol,date",
    max_workers=4,
)
_dump.dump()

# --------------------------------------------------------------------------------------------

# Clear
shutil.rmtree(Path().resolve().joinpath("source"))
shutil.rmtree(Path().resolve().joinpath("normalize"))
