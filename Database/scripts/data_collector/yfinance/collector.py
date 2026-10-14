import yfinance as yf

from pathlib import Path
from time import sleep


def download_data(
    tickers,
    start=None, end=None, period="max",
    append_index_data=False,
    append_index_data__index_name='^GSPC',
    append_index_data__features=['open', 'high', 'low', 'close', 'volume'],
    interval_between_downloads=10,
    batch_size=50,
    threads=True,

    target_dir=None,
):
    '''
        tickers : str, list
            List of tickers to download.
        qlib_dir: str
            qlib(dump) data directory.
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is today
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        append_index_data: str
            Create extra columns on all the tickers from the selected ticker. Should be the index for the market.
            All extra columns will follow the convention "foo idx".
        interval_between_downloads: int
            Number of seconds to wait after each batch download.
        batch_size: int
            Size of the download batches.
        threads: bool
            Whether to use threads or not.

        Other possible parameters for yf.download can be seen in:
        https://github.com/ranaroussi/yfinance/blob/master/yfinance/multi.py


        REMEMBER: dump_bin.py must be in the same directory as this file!
    '''

    if target_dir is None:
        target_dir = Path().resolve().joinpath("source")
    target_dir.mkdir(exist_ok=True, parents=True)
    

    append_index_data__features = [str(col) + '_idx' for col in append_index_data__features]
    if 'date' not in append_index_data__features: append_index_data__features.append('date')

    # -------------------------------------------------------

    ################################
    # Create ticker batches
    ################################

    ticker_batches = []

    slice_start = 0
    slice_end = batch_size

    done = False
    while not done:
        if slice_end > len(tickers):
            slice_end = len(tickers)
            done = True

        ticker_batches.append(tickers[slice_start:slice_end])

        slice_start += batch_size
        slice_end += batch_size

    # -------------------------------------------------------

    ################################
    # Download
    ################################
    if append_index_data is True:  # Download index data to add later
        index_data = yf.download(
            append_index_data__index_name, start=start, end=end, period=period,
            interval="1d", group_by="ticker", threads=threads,
            auto_adjust=True
        ).droplevel(0, axis=1)
        index_data.columns = [str(col) + '_idx' for col in index_data.columns]
        index_data = index_data.reset_index()
        index_data.columns = index_data.columns.str.lower()

    first_iteration = True
    for ticker_batch in ticker_batches:
        if not ticker_batch: continue

        if not first_iteration:
            sleep(interval_between_downloads)  # Sleep n seconds
        else:
            first_iteration = False

        # Download the data with yfinance from Yahoo!
        yahoo_data = yf.download(
            ticker_batch, start=start, end=end, period=period,
            interval="1d", group_by="ticker", threads=threads,
            auto_adjust=True
        )

        # Save .csv's in dock folder
        for ticker in ticker_batch:
            ticker_data = yahoo_data[ticker].reset_index()
            ticker_data.columns = ticker_data.columns.str.lower()

            if append_index_data is True:  # add index data if any
                ticker_data = ticker_data.merge(index_data[append_index_data__features], on='date', how='left', suffixes=("", "_idx"))

            ticker_data.to_csv("%s/%s.csv" % (target_dir, ticker), index=False)
