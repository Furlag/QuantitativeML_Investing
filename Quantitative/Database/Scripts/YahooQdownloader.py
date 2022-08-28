import os
import shutil
import pathlib

import time

import yfinance as yf


def YahooQdownloader(
    tickers, start=None, end=None, period="max",
    append_index_data='',
    qlib_dir="QData", dump_mode="dump_all",
    sleep=5, batch_size=50,
    threads=True, python_path=None
):
    '''
        tickers : str, list
            List of tickers to download
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
        qlib_dir: str
            qlib(dump) data director
        dump_mode: str
            "dump_all": Creates Qdata from zero. If a data for the same company already exists it will be deleted.
            "dump_update": Updates the data on existing dataset. Existing values wont be changed.
            "dump_fix": Replaces values on existing dataset.
        sleep: int
            Number of seconds to wait after each batch download.

        Other possible parameters for yf.download can be seen in:
        https://github.com/ranaroussi/yfinance/blob/master/yfinance/multi.py
    '''

    ################################
    # Create docking folder
    ################################

    dock_folder = "QLib_Yahoo_Data_Dock_Folder"

    # Change the current directory to this file directory
    path = str(pathlib.Path(__file__).parent.resolve())
    os.chdir(path)

    try:  # Try to create the directory
        os.mkdir(dock_folder)
    except OSError:  # The directory already exists
        shutil.rmtree(dock_folder)
        os.mkdir(dock_folder)

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
    if append_index_data != '':
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

        # Save .csv's in dock
        for ticker in ticker_batch:
            ticker_data = yahoo_data[ticker].reset_index()
            ticker_data.columns = ticker_data.columns.str.lower()

            if append_index_data != '':
                ticker_data = ticker_data.merge(index_data, on='date', how='left', suffixes=("", "_idx"))

            ticker_data.to_csv("%s/%s/%s.csv" % (path, dock_folder, ticker))

    # -------------------------------------------------------

    ################################
    # Dump data and clean memory
    ################################

    # Dump Data as Qlib database
    python_path = "python" if python_path is None else python_path
    cmd_command = (
        python_path + " " + path + "/dump_bin.py " + dump_mode
        + " --csv_path " + path + "/" + dock_folder
        + " --qlib_dir " + qlib_dir
        + " --date_field_name date"
        + """ --include_fields open,close,high,low,volume,
            open_idx,high_idx,low_idx,close_idx,volume_idx
        """
    )
    os.system(cmd_command)

    # Delete dock folder
    shutil.rmtree(dock_folder)
