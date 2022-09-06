import os
import shutil
import pathlib
import sys

import time

import yfinance as yf


def yahoo_downloader(
    tickers,
    qlib_dir, dump_mode="dump_all",
    start=None, end=None, period="max",
    append_index_data='',
    sleep=5, batch_size=50,
    threads=True,
    version=2
):
    '''
        tickers : str, list
            List of tickers to download.
        qlib_dir: str
            qlib(dump) data directory.
        dump_mode: str
            "dump_all": Creates Qdata from zero. If a data for the same company already exists it will be deleted.
            "dump_update": Updates the data on existing dataset. Existing values wont be changed.
            "dump_fix": Replaces values on existing dataset.
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        append_index_data: str
            Create extra columns on all the tickers from the selected ticker. Should be the index for the market.
            All extra columns will follow the convention "foo_idx".
        sleep: int
            Number of seconds to wait after each batch download.
        batch_size: int
            Size of the download batches.
        threads: bool
            Whether to use threads or not.

        Other possible parameters for yf.download can be seen in:
        https://github.com/ranaroussi/yfinance/blob/master/yfinance/multi.py


        REMEMBER: dump_bin.py must be in the same directory as this file!
    '''

    dir_path = str(pathlib.Path(__file__).parent.resolve())

    ################################
    # Create dock folder
    ################################

    dock_path = os.path.join(dir_path, "Yahoo_Data_Dock")

    try:  # Try to create the directory
        os.mkdir(dock_path)
    except OSError:  # The directory already exists
        shutil.rmtree(dock_path)
        os.mkdir(dock_path)

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
            time.sleep(sleep)  # Sleep n seconds
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

            ticker_data.to_csv("%s/%s.csv" % (dock_path, ticker))

    # -------------------------------------------------------

    ################################
    # Dump data and clean memory
    ################################

    python_path = sys.executable

    # Dump Data as Qlib database
    cmd_command = (
        python_path + " " + dir_path + "/dump_bin.py " + dump_mode
        + " --csv_path " + dock_path
        + " --qlib_dir " + qlib_dir
        + " --date_field_name date"
        + " --include_fields open,close,high,low,volume,open_idx,high_idx,low_idx,close_idx,volume_idx"
    )
    os.system(cmd_command)

    # -------------------------------------------------------

    # Delete dock folder
    shutil.rmtree(dock_path)
