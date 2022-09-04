from scripts.download import yahoo_downloader  # Noqa

import os
import pandas as pd
from datetime import datetime, timedelta


# Read tickers
T = pd.read_csv('C:/Projects/Investing/QuantitativeML_Investing/Database/Ticker_Lookup.csv', skiprows=1)
print(T.head())


# Dates
start = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')


########################################################################################################################
########################################################################################################################


###################
# Spain
###################
tickers = (
    ['^IBEX', 'INDC.MC']
    + T['^IBEX'].dropna().tolist() + T['INDC.MC'].dropna().tolist()
)

qlib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Qdata", "SPAIN")
yahoo_downloader(
    tickers, start=start, end=end, qlib_dir=qlib_dir,
    append_index_data='^IBEX',
    dump_mode="dump_update",
    # python_path=python_path
)

###################
# US
###################
"""
tickers = (
    ['^GSPC', '^SP600']
    + T['^GSPC'].dropna().tolist() + T['^SP600'].dropna().tolist()
)
"""
