# from scripts.data_collector.us_index.collector import SP500Index, SP400Index
from collector import download_data


import pandas as pd
from datetime import datetime, timedelta

from dump_bin import DumpDataAll, DumpDataUpdate, DumpDataFix

from pathlib import Path
import sys


# Append dump_bin to sys.path
CUR_DIR = Path().resolve()
sys.path.append(str(CUR_DIR.parent.parent))


# Target database
qlib_dir = Path().resolve().parent.parent.parent.joinpath("qlib_data_US")


# ------------------------------------------------------------------------------


# Read tickers
tickers_sp500 = pd.read_csv(qlib_dir.joinpath("instruments/sp500_only_new.txt"), sep='\t', header=None, names=['symbol', 'start_date', 'end_date'])
tickers_sp400 = pd.read_csv(qlib_dir.joinpath("instruments/sp400_only_new.txt"), sep='\t', header=None, names=['symbol', 'start_date', 'end_date'])


# Dates
start = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')


########################################################################################################################
########################################################################################################################

tickers = (
    ['^GSPC']  # '^MID', '^SP600'
    + tickers_sp500['symbol'].tolist()
    # + tickers_sp400['symbol'].tolist()
)
tickers = [ticker.replace('.', '-') for ticker in tickers]


download_data(
    tickers,
    start=start, end=end,
    # append_index_data='^GSPC'
)


""" dump_mode: str
    "dump_all": Creates Qdata from zero. If a data for the same company already exists it will be deleted.
    "dump_update": Updates the data on existing dataset. Existing values wont be changed.
    "dump_fix": Replaces values on existing dataset.
"""

_dump = DumpDataAll(
    csv_path=Path().resolve().joinpath("source"),
    qlib_dir=qlib_dir,
    exclude_fields="symbol,date",
    max_workers=4,
)
_dump.dump()
