import yfinance as yf

from time import sleep


def collect(
    tickers,
    qlib_dir,
    start=None, end=None, period="max",
    append_index_data='',
    interval_between_downloads=5,
    batch_size=50,
    threads=True,
    data_dock_dir=None,
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
            All extra columns will follow the convention "foo_idx".
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

    if data_dock_dir is None:
        data_dock_dir = qlib_dir.resolve().joinpath("data_dock")
    data_dock_dir.mkdir(exist_ok=True, parents=True)
    
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
    if append_index_data != '':  # Download index data to add later
        index_data = yf.download(append_index_data, start=start, end=end, period=period,
                                 interval="1d", group_by="ticker", threads=threads)
        index_data.columns = [str(col) + '_idx' for col in index_data.columns]
        index_data = index_data.reset_index()
        index_data.columns = index_data.columns.str.lower()

    first_iteration = True
    for ticker_batch in ticker_batches:
        if not first_iteration:
            sleep(interval_between_downloads)  # Sleep n seconds
        else:
            first_iteration = False

        # Download the data with yfinance from Yahoo!
        yahoo_data = yf.download(ticker_batch, start=start, end=end, period=period,
                                 interval="1d", group_by="ticker", threads=threads)

        # Save .csv's in dock folder
        for ticker in ticker_batch:
            ticker_data = yahoo_data[ticker].reset_index()
            ticker_data.columns = ticker_data.columns.str.lower()

            if append_index_data != '':  # add index data if any
                ticker_data = ticker_data.merge(index_data, on='date', how='left', suffixes=("", "_idx"))

            ticker_data.to_csv("%s/%s.csv" % (data_dock_dir, ticker))
