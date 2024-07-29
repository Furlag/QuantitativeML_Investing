from scripts.data_collector.us_index.collector import SP500Index, SP400Index
from scripts.yfinance_collector import collect

import os
import sys
from pathlib import Path

import pandas as pd

from datetime import datetime, timedelta


qlib_dir = Path(__file__).parent.resolve().joinpath("qlib_data_US")


# Read tickers
tickers_sp500 = pd.read_csv(qlib_dir.joinpath("instruments/sp500_only_new.txt"), sep='\t', header=None, names=['symbol', 'start_date', 'end_date'])


# Dates
start = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')


########################################################################################################################
########################################################################################################################

tickers = (
    ['^GSPC']  # '^MID', '^SP600'
    + tickers_sp500['symbol'].tolist()
)
tickers = [ticker.replace('.', '-') for ticker in tickers]


collect(
    tickers,
    qlib_dir,
    start=start, end=end,
    append_index_data='^GSPC'
)


""" dump_mode: str
    "dump_all": Creates Qdata from zero. If a data for the same company already exists it will be deleted.
    "dump_update": Updates the data on existing dataset. Existing values wont be changed.
    "dump_fix": Replaces values on existing dataset.
"""
dump_mode = "dump_update"


# Dump Data as Qlib database
cmd_command = (
    sys.executable + " " + str(Path(__file__).parent.resolve().joinpath("scripts")) + "/dump_bin.py " + dump_mode
    + " --csv_path " + str(qlib_dir.joinpath("_datadock"))
    + " --qlib_dir " + str(qlib_dir)
    + " --date_field_name date"
    + " --include_fields open,close,high,low,volume,open_idx,high_idx,low_idx,close_idx,volume_idx"
)
os.system(cmd_command)
