from Scripts.YahooQdownloader import YahooQdownloader  # Noqa
import os
import pandas as pd
from datetime import datetime, timedelta


dir_path = os.path.dirname(os.path.abspath(__file__))


# Path of the Qlib Database
path = dir_path + "/Qdata/"
print(path)


# Read tickers
T = pd.read_csv('C:/Projects/Investing/Tickers/Ticker_Lookup.csv', skiprows=1)
print(T.head())


# Dates
start = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
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
qlib_dir = path + "SPAIN"

YahooQdownloader(tickers, start=start, end=end, qlib_dir=qlib_dir, append_index_data='^IBEX', dump_mode="dump_update")

###################
# US
###################
"""
tickers = (
    ['^GSPC', '^SP600']
    + T['^GSPC'].dropna().tolist() + T['^SP600'].dropna().tolist()
)
qlib_dir = path + "US"
YahooQdownloader(tickers, start=start, end=end, qlib_dir=qlib_dir, dump_mode="dump_update")
"""
