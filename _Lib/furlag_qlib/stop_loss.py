#  region --------------------------------------------- Imports --------------------------------------------------------
import json

import pandas as pd  # noqa
import numpy as np  # noqa

from qlib.data.dataset.loader import QlibDataLoader
from qlib.data.dataset.handler import DataHandler
#  endregion


#######################################################################################################################
#  region --------------------------------------- Stop-loss classes ---------------------------------------------------

class StopLoss():
    def __init__(
        self,

        threshold_logics=[],

        instruments=None,
        start_time=None,
        end_time=None,
        freq="day",
    ):
        """
            TODO
        """

        # Dictionary for the stop_loss orders (thresholds) and their last update date
        self.stop_loss = {}

        # BASIC MARKET DATA
        print("Stop_Loss basic market data initializing...")
        self.market_dh = DataHandler(
            instruments=instruments,
            start_time=start_time,
            end_time=end_time,
            data_loader=QlibDataLoader(config={"data": (['$open', '$high', '$low', '$close'],
                                                        ["OPEN", "HIGH", "LOW", "CLOSE"])},
                                       freq=freq)
        )
        self.market_data = self.market_dh.fetch(selector=slice(start_time, end_time))

        # STOP LOSS THRESHOLDS DATA
        print("Stop_Loss thresholds data initializing...")
        threshold_names = ["Threshold_" + str(n) for n in list(range(0, len(threshold_logics)))]
        self.thresholds_dh = DataHandler(
            instruments=instruments,
            start_time=start_time,
            end_time=end_time,
            data_loader=QlibDataLoader(config={"thresholds": (threshold_logics, threshold_names)},
                                       freq=freq)
        )
        self.thresholds_data = self.thresholds_dh.fetch(selector=slice(start_time, end_time))

    def config(self, instruments=None, start_time=None, end_time=None):
        """
            Used to change the configuration for DataHandler's.
            This method will be used when loading pickled object.
        """

        # BASIC MARKET DATA
        self.market_dh.config(instruments=instruments, start_time=start_time, end_time=end_time)

        # STOP LOSS THRESHOLDS DATA
        self.thresholds_dh.config(instruments=instruments, start_time=start_time, end_time=end_time)

    def setup_data(self):
        """
            Used to load data again into self.market_data and self.thresholds_data.
        """

        # BASIC MARKET DATA
        print("Stop_Loss basic market data setting up...")
        self.market_dh.setup_data()
        self.market_data = self.market_dh.fetch(selector=slice(None, None))

        # STOP LOSS THRESHOLDS DATA
        print("Stop_Loss thresholds data setting up...")
        self.thresholds_dh.setup_data()
        self.thresholds_data = self.thresholds_dh.fetch(selector=slice(None, None))

    def clean_memory(self):
        """
            Used to save memory if you are going to save the class and you plan
            on loading it again with different data.
        """

        # BASIC MARKET DATA
        self.market_data = None

        # STOP LOSS THRESHOLDS DATA
        self.thresholds_data = None

    def initialize_threshold(self, code, start_time, end_time, trade_exchange, fields=[]):
        """
            Initialize a new Stop Loss order for one stock.

            Parameters
            ----------
            code : str
                The code of the stock to initialize the Stop Loss threshold for.

            start_time : Union[pd.Timestamp, str]
                Start of the slices used for fetching the data.

            end_time : Union[pd.Timestamp, str]
                End of the slices used for fetching the data.

            trade_exchange : Exchange()
                Instance of qlib.contrib.backtest.Exchange -> Exchange()
                Used to avoid fetching error, if stock has no data for that period.

            fields : List[Text]
                You can use this field to select only some of the threshold logics.
        """

        if trade_exchange.is_stock_tradable(code, start_time, end_time):
            # --- Load necessary market data --- #
            close_price_slice = self.market_data.loc[(slice(start_time, end_time), code), 'CLOSE']
            # close_price_slice = close_price_slice.loc[~close_price_slice.isna().astype(bool)]
            close_price = close_price_slice.iloc[-1] if len(close_price_slice) > 0 else np.inf

            # --- Load thresholds and set up the Stop Loss --- #
            thresholds_slice = self.thresholds_data.loc[(slice(start_time, end_time), code), :]
            # thresholds_slice = thresholds_slice.loc[~thresholds_slice.isna().all(axis=1).astype(bool)]
            if len(thresholds_slice) == 0:
                stop_loss_price = 0
            else:
                thresholds = thresholds_slice.iloc[-1:]
                # Filter fields if needed
                thresholds = thresholds[fields] if len(fields) > 0 else thresholds
                # Orders cannot be above -> current price / latest price / close price
                thresholds.where(thresholds < close_price, np.nan, inplace=True)
                # Select max threshold
                stop_loss_price = thresholds.max(axis=1).values[0]

            # Save in stop_loss_info
            self.stop_loss[code] = stop_loss_price

    def update_thresholds(self, start_time, end_time, trade_exchange, fields=[], down_trailing=False):
        """
            Update currently active thresholds with new data.

            Parameters
            ----------
            start_time : Union[pd.Timestamp, str]
                Start of the slices used for fetching the data.

            end_time : Union[pd.Timestamp, str]
                End of the slices used for fetching the data.

            trade_exchange : Exchange()
                Instance of qlib.contrib.backtest.Exchange -> Exchange()
                Used to avoid fetching error, if stock has no data for that period.

            fields : List[Text]
                You can use this field to select only some of the threshold logics.

            down_trailing : Bool
                True to follow a trailing stop loss strategy on price decreases. False to not.
        """

        for code in self.stop_loss.keys():
            if not trade_exchange.is_stock_tradable(code, start_time, end_time):
                continue
            # --- Load necessary market data --- #
            close_price_slice = self.market_data.loc[(slice(start_time, end_time), code), 'CLOSE']
            # close_price_slice = close_price_slice.loc[~close_price_slice.isna().astype(bool)]
            close_price = close_price_slice.iloc[-1] if len(close_price_slice) > 0 else np.inf

            # --- Load new stop loss price (threshold) --- #
            thresholds_slice = self.thresholds_data.loc[(slice(start_time, end_time), code), :]
            # thresholds_slice = thresholds_slice.loc[~thresholds_slice.isna().all(axis=1).astype(bool)]
            if len(thresholds_slice) == 0:
                stop_loss_price = 0
            else:
                thresholds = thresholds_slice.iloc[-1:]
                # Filter fields if needed
                thresholds = thresholds[fields] if len(fields) > 0 else thresholds
                # Orders cannot be above -> current price / latest price / close price
                thresholds.where(thresholds < close_price, np.nan, inplace=True)
                # Select max threshold
                stop_loss_price = thresholds.max(axis=1).values[0]

            # --- Load previous stop loss price (threshold) --- #
            prev_stop_loss_price = self.stop_loss[code]

            # ------------ Update threshold if appropiate ------------ #
            if down_trailing or (stop_loss_price > prev_stop_loss_price):
                self.stop_loss[code] = stop_loss_price  # Save in stop_loss

    def check_broken_thresholds(self, start_time, end_time, trade_exchange, trade_position, soft_thresholds=False):
        """
            Checks for Stop Loss threshold breakthrough for the codes of held stocks
            during date, and sells the stock for the Stop Loss threshold price, since it
            should have been sold by that price automatically by the broker.
            There might still be some diferences between the Stop Loss threshold price set and
            the actual price on which the stock is sold on practice.

            None of this applies however if 'soft_thresholds' is set to True. In that case
            the function will return a list with the codes for the stocks with a close price
            lower than the stop_loss set.

            Parameters
            ----------
            start_time : Union[pd.Timestamp, str]
                Start of the slices used for fetching the data.

            end_time : Union[pd.Timestamp, str]
                End of the slices used for fetching the data.

            trade_exchange : Exchange()
                Instance of qlib.contrib.backtest.Exchange -> Exchange()
                Used to avoid fetching error, if stock has no data for that period.

            trade_position : Position()
                Instance of qlib.contrib.backtest.Position -> Position()

            soft_thresholds: Bool
                Wether to use soft stop_loss or not.
        """

        if soft_thresholds:
            # Sell orders
            sell_order_list = []

            # Load currently held stock list
            held_stock_list = trade_position.get_stock_list()

            # Loop through currently held stock list
            for code in held_stock_list:
                if not trade_exchange.is_stock_tradable(code, start_time, end_time):
                    continue
                elif code in self.stop_loss.keys():
                    # --- Load last price (CLOSE) --- #
                    close_price_slice = self.market_data.loc[(slice(start_time, end_time), code), 'CLOSE']
                    # close_price_slice = close_price_slice.loc[~close_price_slice.isna().astype(bool)]
                    close_price = close_price_slice.iloc[-1] if len(close_price_slice) > 0 else np.inf

                    # --- Load current Stop_Loss threshold --- #
                    stop_loss_price = self.stop_loss[code]

                    # ------------ Check for break ------------ #
                    if stop_loss_price > close_price:
                        sell_order_list.append(code)

            return sell_order_list

        else:  # Hard thresholds
            # Load currently held stock list
            held_stock_list = trade_position.get_stock_list()

            # Loop through currently held stock list
            for code in held_stock_list:
                if not trade_exchange.is_stock_tradable(code, start_time, end_time):
                    continue
                elif code in self.stop_loss.keys():
                    # --- Load last valid open price --- #
                    open_price_slice = self.market_data.loc[(slice(start_time, end_time), code), 'OPEN']
                    # open_price_slice = open_price_slice.loc[~open_price_slice.isna().astype(bool)]
                    open_price = open_price_slice.iloc[-1] if len(open_price_slice) > 0 else np.inf

                    # --- Load last valid low price --- #
                    low_price_slice = self.market_data.loc[(slice(start_time, end_time), code), 'LOW']
                    # low_price_slice = low_price_slice.loc[~low_price_slice.isna().astype(bool)]
                    low_price = low_price_slice.iloc[-1] if len(low_price_slice) > 0 else np.inf

                    # --- Load current Stop_Loss threshold -- #
                    stop_loss_price = self.stop_loss[code]

                    # ------------ Execute sell ------------ #
                    if stop_loss_price >= low_price:
                        # Calculate trade_val, trade_cost and trade_price
                        trade_amount = trade_position.get_stock_amount(code)  # n_stocks held
                        if stop_loss_price >= open_price:
                            trade_val = trade_amount * open_price
                            trade_price = open_price
                        else:
                            trade_val = trade_amount * stop_loss_price
                            trade_price = stop_loss_price
                        trade_cost = max(trade_val * trade_exchange.close_cost, trade_exchange.min_cost)

                        # Sell Stock
                        trade_position._sell_stock(code, trade_val, trade_cost, trade_price)

                        # Delete stop-loss threshold
                        del self.stop_loss[code]

    # ---------------------------------------------------------------------------------------------

    def get_theorical_threshold(self, code, start_time, end_time, fields=[]):
        """
            Returns what the Stop Loss threshold would be for code and date if it was set that time.
            This is build in a way that will use the last valid (non NA) data available until Timestamp == end_time.
            As such, it makes possible to get a valid Stop Loss even on a period between start_time and end_time
            where there was no trading for the stock.

            Parameters
            ----------
            code : str
                The code of the stock to get the Stop Loss threshold for.

            start_time : Union[pd.Timestamp, str]
                Start of the slices used for fetching the data.

            end_time : Union[pd.Timestamp, str]
                End of the slices used for fetching the data.

            fields : List[Text]
                You can use this field to select only some of the threshold logics.
        """

        # --- Load necessary market data --- #
        close_price_slice = self.market_data.loc[(slice(start_time, end_time), code), 'CLOSE']
        # close_price_slice = close_price_slice.loc[~close_price_slice.isna().astype(bool)]
        close_price = close_price_slice.iloc[-1] if len(close_price_slice) > 0 else np.inf

        # --- Load thresholds and set up the Stop Loss --- #
        thresholds_slice = self.thresholds_data.loc[(slice(start_time, end_time), code), :]
        # thresholds_slice = thresholds_slice.loc[~thresholds_slice.isna().all(axis=1).astype(bool)]
        if len(thresholds_slice) == 0:
            stop_loss_price = 0
        else:
            thresholds = thresholds_slice.iloc[-1:]
            # Filter fields if needed
            thresholds = thresholds[fields] if len(fields) > 0 else thresholds
            # Orders cannot be above -> current price / latest price / close price
            thresholds.where(thresholds < close_price, np.nan, inplace=True)
            # Select max threshold
            stop_loss_price = thresholds.max(axis=1).values[0]

        return stop_loss_price

    # ---------------------------------------------------------------------------------------------

    def delete_all_thresholds(self):
        self.stop_loss = {}

    def delete_threshold(self, code):
        if code in self.stop_loss.keys():
            del self.stop_loss[code]

    def set_threshold(self, code, price):
        self.stop_loss[code] = price

    def get_threshold(self, code):
        if code in self.stop_loss.keys():
            return self.stop_loss[code]
        else:
            return None

    def get_thresholds(self):
        return pd.DataFrame.from_dict(self.stop_loss, orient='index')

    # ---------------------------------------------------------------------------------------------

    def save_info(self, path='StopLoss_info.json'):
        temp_stop_loss = self.stop_loss  # Avoid modifiying main stop_loss dict
        for key in temp_stop_loss:
            temp_stop_loss[key] = float(temp_stop_loss[key])

        json_file = open(path, 'w')
        json.dump(temp_stop_loss, json_file, indent=4)
        json_file.close()

    def load_info(self, path='StopLoss_info.json'):
        self.stop_loss = {}  # Empty main stop_loss dict

        json_file = open(path)
        self.stop_loss = json.load(json_file)
        json_file.close()

        for key in self.stop_loss:
            self.stop_loss[key] = float(self.stop_loss[key])


class StopLossLogics():
    def __init__(
        self
    ):
        pass

    def atr_stoploss(self, diff=1.5, of='$close', r=14):
        return """
            {of} - {diff} * Mean(
                Greater(
                    $high-$low,
                    Greater(
                        Abs($high-Ref($close, 1)),
                        Abs($low-Ref($close, 1))
                    )
                ),
                {r}
            )
        """.format(diff=diff, of=of, r=r)
    ######################################################

    #############################
    # # # Stop Loss samples # # #
    #############################

    normal_atr = """
        $close - 1.5 * Mean(
            Greater(
                $high-$low,
                Greater(
                    Abs($high-Ref($close, 1)),
                    Abs($low-Ref($close, 1))
                )
            ),
            14
        )
    """

    high_atr = """
        $high - 2 * Mean(
            Greater(
                $high-$low,
                Greater(
                    Abs($high-Ref($close, 1)),
                    Abs($low-Ref($close, 1))
                )
            ),
            20
        )
    """

    low_atr = """
        $low - 1.5 * Mean(
            Greater(
                $high-$low,
                Greater(
                    Abs($high-Ref($close, 1)),
                    Abs($low-Ref($close, 1))
                )
            ),
            20
        )
    """

    bollinger_band = """((Mean($close, 20) - 2 * Std($close, 20)))"""
