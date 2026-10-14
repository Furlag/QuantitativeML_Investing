from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

from data_collector.yfinance.collector import download_data
from dump_bin import DumpDataUpdate, DumpDataFix

########################################################################################################################

BASE_DIR = Path(__file__).resolve().parents[1]
qlib_dir = BASE_DIR / "Qdata/EU"
components_dir = BASE_DIR / "components"

########################################################################################################################

def run_pipeline():

    tickers = pd.read_csv(components_dir / "components_STOXX600.csv", sep=',')

    tickers = tickers[tickers['currency'] == 'EUR']

    tickers = (
        ['EXSA.DE']
        + tickers['ticker'].tolist()
    )

    download_data(
        tickers,
        start=(datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d'),
        end=(datetime.today() - timedelta(days=0)).strftime('%Y-%m-%d'),

        append_index_data=True,
        append_index_data__index_name="EXSA.DE",
        append_index_data__features=['close'],
        
        target_dir=qlib_dir / "_raw_data_from_yfinance"
    )

    _dump = DumpDataUpdate(
        data_path=qlib_dir / "_raw_data_from_yfinance",
        qlib_dir=qlib_dir,
        exclude_fields="symbol,date",
        max_workers=4,
    )

    _dump.dump()

########################################################################################################################

if __name__ == "__main__":
    run_pipeline()