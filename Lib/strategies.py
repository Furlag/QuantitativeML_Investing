#  region --------------------------------------------- Imports --------------------------------------------------------
from .stop_loss import StopLoss

import copy
# import math

import pandas as pd

from qlib.strategy.base import BaseStrategy
from qlib.backtest.decision import Order, OrderDir, TradeDecisionWO

from qlib.backtest.signal import Signal, create_signal_from

from qlib.data.dataset.loader import QlibDataLoader
from qlib.data.dataset.handler import DataHandler

#  endregion


#######################################################################################################################
#  region ------------------------------------------ Strategies -------------------------------------------------------

class BasicStrategy(BaseStrategy):
    def __init__(
        self,

        signal,

        investment_percentage=0.10,

        buy_threshold=0,
        sell_threshold=0
    ):
        self.signal: Signal = create_signal_from(signal)

        self.investment_percentage = investment_percentage

        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def get_account_risk_degree(self, start_time, end_time):
        """get_risk_degree
        Return the proportion of your total value you will used in investment.
        Dynamically risk_degree will result in Market timing.
        """
        account_risk_degree = 0.90
        return account_risk_degree

    def generate_trade_decision(self, execute_result=None):

        sell_order_list = []
        buy_order_list = []

        ################################################################################################################

        # Init
        trade_step = self.trade_calendar.get_trade_step()
        pred_start_time, pred_end_time = self.trade_calendar.get_step_time(trade_step, shift=1)
        trade_start_time, trade_end_time = self.trade_calendar.get_step_time(trade_step)
        pred_score = self.signal.get_signal(start_time=pred_start_time, end_time=pred_end_time)

        if isinstance(pred_score, pd.DataFrame):
            pred_score = pred_score.iloc[:, 0]
        if pred_score is None:
            return TradeDecisionWO([], self)

        # --------------------------------------------------------------------------------------------------------------

        current_temp = copy.deepcopy(self.trade_position)  # Create a copy of current Position()
        cash = current_temp.get_cash()  # Load current cash
        held_stock_list = current_temp.get_stock_list()  # Load currently held stocks

        ################################################################################################################

        ############################################################################
        # # # IDENTIFY CURRENTLY HELD STOCKS AND SELL THOSE WITH A SELL SIGNAL # # #
        ############################################################################
        held_stock_scores = pred_score.reindex(held_stock_list)
        sell_signals = held_stock_scores[held_stock_scores < self.sell_threshold]

        for code in sell_signals.index:  # Sell order
            sell_amount = current_temp.get_stock_amount(code=code)  # Amount of held stock
            sell_order = Order(
                stock_id=code,
                amount=sell_amount,
                start_time=trade_start_time,
                end_time=trade_end_time,
                direction=Order.SELL,  # 0 for sell, 1 for buy
                factor=self.trade_exchange.get_factor(
                    stock_id=code, start_time=trade_start_time, end_time=trade_end_time
                ),
            )

            if self.trade_exchange.check_order(sell_order):  # is order executable
                sell_order_list.append(sell_order)

                # Execute order
                # trade_val, trade_cost, trade_price = self.trade_exchange.deal_order(
                #   sell_order, position=current_temp
                # )
                # cash += trade_val - trade_cost  # update cash

        ################################################################################################################

        ########################################################################
        # # # IDENTIFY BUY SIGNALS FOR UNHELD STOCKS AND BUY THE BEST ONES # # #
        ########################################################################
        unheld_stock_scores = pred_score[~pred_score.index.isin(held_stock_scores.index)]
        buy_signals = unheld_stock_scores[unheld_stock_scores > self.buy_threshold]
        top_buy_signals = buy_signals.sort_values(ascending=False)

        available_cash = cash * self.get_account_risk_degree(start_time=pred_start_time, end_time=pred_start_time)
        account_value = current_temp.calculate_value()

        for code in top_buy_signals.index:  # Buy order
            if not self.trade_exchange.is_stock_tradable(
                stock_id=code, start_time=trade_start_time, end_time=trade_end_time
            ):
                continue

            # Calculate the number of stocks to buy and cash spend
            buy_price = self.trade_exchange.get_deal_price(
                stock_id=code, start_time=trade_start_time, end_time=trade_end_time, direction=OrderDir.BUY
            )

            cash_spend = account_value * self.investment_percentage
            buy_amount = cash_spend / buy_price

            if available_cash >= cash_spend and cash_spend > 0:
                factor = self.trade_exchange.get_factor(
                    stock_id=code, start_time=trade_start_time, end_time=trade_end_time
                )
                buy_amount = self.trade_exchange.round_amount_by_trade_unit(buy_amount, factor)

                buy_order = Order(
                    stock_id=code,
                    amount=buy_amount,
                    start_time=trade_start_time,
                    end_time=trade_end_time,
                    direction=Order.BUY,  # 1 for buy
                    factor=factor,
                )
                buy_order_list.append(buy_order)

                # Update cash
                available_cash -= cash_spend

        ################################################################################################################

        # Save position
        # current.save_position('Position.xls', trade_date)

        return TradeDecisionWO(sell_order_list + buy_order_list, self)


class KellyCriterionStrategy(BaseStrategy):
    def __init__(
        self,

        signal,

        buy_threshold=0,
        sell_threshold=0,

        investment_risk_degree=0.01,

        stop_loss_logics=["""
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
        """],
        hard_stop_loss=False,
        soft_stop_loss=False,
        trailing_stop_loss=False,

        max_invest=None,
        min_invest=None,

        fractional_shares=False,

        stock_validation=False,
        stock_validation_logics=["""
            Sum(
                If(
                    EMA(
                        ($volume * ($high + $low + $close + $open)/4),
                        80
                    ) > 3000000,
                    1,
                    0
                ),
                80
            ) > 65
        """],

        instruments=None,
        start_time=None,
        end_time=None,
    ):
        """
            TODO
        """
        if hard_stop_loss and soft_stop_loss:  # hard_stop_loss takes priority
            soft_stop_loss = False

        ####################
        # # # __init__ # # #
        ####################
        self.signal: Signal = create_signal_from(signal)

        # Buy and Sell Thresholds
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

        # Investment Risk Degree
        self.investment_risk_degree = investment_risk_degree

        # StopLoss
        self.stop_loss = StopLoss(instruments=instruments, start_time=start_time, end_time=end_time,
                                  threshold_logics=stop_loss_logics)
        self.hard_stop_loss = hard_stop_loss
        self.soft_stop_loss = soft_stop_loss
        self.trailing_stop_loss = trailing_stop_loss

        # Investment amount
        self.max_invest = max_invest
        self.min_invest = min_invest

        # Fractional Shares
        self.fractional_shares = fractional_shares

        # Stock validation
        self.stock_validation = stock_validation
        if self.stock_validation:
            # STOCK VALIDATION DATA
            print("Stock validation data initializing...")
            self.stock_validation_dh = DataHandler(
                instruments=instruments,
                start_time=start_time,
                end_time=end_time,
                data_loader=QlibDataLoader(
                    config={"data": (['$volume'], ["VOLUME"])},
                    filter_pipe=[
                        {
                            "class": "ExpressionDFilter",
                            "module_path": "qlib.data.filter",
                            "kwargs": {"rule_expression": stock_validation_logics, "keep": True}
                        }
                    ]
                )
            )
            self.stock_validation_index = self.stock_validation_dh.fetch(selector=slice(start_time, end_time)).index

    def config(self, instruments=None, start_time=None, end_time=None):
        """
            Used to change the configuration for DataHandler's.
            This method will be used when loading pickled object.
        """

        # STOPLOSS CLASS DATA
        self.stop_loss.config(instruments=instruments, start_time=start_time, end_time=end_time)

        # STOCK VALIDATION DATA
        if self.stock_validation:
            self.stock_validation_dh.config(instruments=instruments, start_time=start_time, end_time=end_time)

    def setup_data(self):
        """
            Need to call this every time an instance of this Class is loaded from disk.
            DataHandlers must run .setup_data() to work properly.
        """

        # STOPLOSS CLASS DATA
        self.stop_loss.setup_data()

        # STOCK VALIDATION DATA
        if self.stock_validation:
            print("Stock Validation data setting up...")
            self.stock_validation_dh.setup_data()
            self.stock_validation_index = self.stock_validation_dh.fetch(selector=slice(None, None)).index

    def clean_memory(self):
        """
            Used to save memory if you are going to save the class and you plan
            on loading it again with different data.
        """

        # STOPLOSS CLASS DATA
        self.stop_loss.clean_memory()

        # STOCK VALIDATION DATA
        if self.stock_validation:
            self.stock_validation_index = None

    def validate_stock(self, code, date):
        """
            Check if stock (code) meets the given criteria in stock_validation_logics for given date.
            Can be used to check if liquidity meets the preferences of the user.
        """
        if self.stock_validation:
            pass  # TODO
        else:
            return True

    def get_account_risk_degree(self, start_time, end_time):
        """ get_risk_degree
            Return the proportion of your total value you will used in investment.
            Dynamically risk_degree will result in Market timing.
        """
        acct_risk_degree = 0.90
        return acct_risk_degree

    def buy__calculations(
        self,
        code,
        trade_start_time, trade_end_time,
        pred_start_time, pred_end_time,
        available_cash, account_value
    ):

        # Load last traded price (CLOSE)
        close_price = self.trade_exchange.get_close(code, pred_start_time, pred_end_time)

        #######################################################################################################
        # DETERMINE cash_spend
        # (It's estimated, since we dont know what the the real buy price will be, we use last price)

        theorical_threshold = self.stop_loss.get_theorical_threshold(code, pred_start_time, pred_end_time)

        max_per_stock_cash_loss = close_price - theorical_threshold
        max_account_value_loss = account_value * self.investment_risk_degree

        cash_spend = (max_account_value_loss / max_per_stock_cash_loss) * close_price

        #######################################################################################################
        # AJUST CASH SPEND

        # max_investment
        if self.max_invest is None:
            pass
        elif self.max_invest <= 0:
            raise NotImplementedError
        elif (self.max_invest < 1 and (cash_spend > account_value * self.max_invest)):
            cash_spend = account_value * self.max_invest
        elif (self.max_invest > 1 and cash_spend > self.max_invest):
            cash_spend = self.max_invest

        # Ajust based on available_cash
        if cash_spend > available_cash:
            cash_spend = available_cash

        # min_investment
        if self.min_invest is None:
            pass
        elif self.min_invest <= 0:
            raise NotImplementedError
        elif (self.min_invest < 1 and (cash_spend < account_value * self.min_invest)):
            cash_spend = account_value * self.min_invest
        elif (self.min_invest > 1 and cash_spend < self.min_invest):
            cash_spend = self.min_invest

        #######################################################################################################
        # DETERMINE buy_amount

        if self.fractional_shares:  # Fractional shares
            buy_amount = cash_spend / close_price
            buy_amount = buy_amount // 0.01 / 100

        else:  # Normal
            buy_amount = cash_spend // close_price

        #######################################################################################################

        # factor = self.trade_exchange.get_factor(
        #     stock_id=code, start_time=trade_start_time, end_time=trade_end_time
        # )
        # buy_amount = self.trade_exchange.round_amount_by_trade_unit(buy_amount, factor)

        return buy_amount, cash_spend

    def generate_trade_decision(self, execute_result=None):

        sell_order_list = []
        buy_order_list = []

        ################################################################################################################

        # Init
        trade_step = self.trade_calendar.get_trade_step()
        trade_start_time, trade_end_time = self.trade_calendar.get_step_time(trade_step)
        pred_start_time, pred_end_time = self.trade_calendar.get_step_time(trade_step, shift=1)

        pred_score = self.signal.get_signal(start_time=pred_start_time, end_time=pred_end_time)

        if isinstance(pred_score, pd.DataFrame):
            pred_score = pred_score.iloc[:, 0]
        if pred_score is None:
            # print("pred_score is None!")
            return TradeDecisionWO([], self)

        # --------------------------------------------------------------------------------------------------------------

        # StopLoss -> Update trade_position acording to hard_stop_loss triggering on trading session.
        if self.hard_stop_loss:
            self.stop_loss.check_broken_thresholds(
                start_time=pred_start_time, end_time=pred_end_time,
                trade_exchange=self.trade_exchange, trade_position=self.trade_position)

        # --------------------------------------------------------------------------------------------------------------

        cash = self.trade_position.get_cash()  # Load current cash
        held_stock_list = self.trade_position.get_stock_list()  # Load currently held stocks

        ################################################################################################################

        ############################################################################
        # # # IDENTIFY CURRENTLY HELD STOCKS AND SELL THOSE WITH A SELL SIGNAL # # #
        ############################################################################
        held_stock_scores = pred_score.reindex(held_stock_list)
        sell_signals = held_stock_scores[held_stock_scores < self.sell_threshold]

        # --------------------------------------------------------------------------------------------------------------

        # StopLoss -> Append soft_stop_loss sell signals. hard_stop_loss takes priority.
        if self.soft_stop_loss:
            sl_signals = self.stop_loss.check_broken_thresholds(
                start_time=pred_start_time, end_time=pred_end_time,
                trade_exchange=self.trade_exchange, trade_position=self.trade_position,
                soft_thresholds=True
            )
            sell_signals = sell_signals.append(held_stock_scores.loc[sl_signals])
            sell_signals = sell_signals[~sell_signals.index.duplicated(keep='first')]

        # --------------------------------------------------------------------------------------------------------------

        # Update sell order list
        for code in sell_signals.index:  # Sell order
            sell_amount = self.trade_position.get_stock_amount(code=code)  # Amount of held stock
            sell_order = Order(
                stock_id=code,
                amount=sell_amount,
                start_time=trade_start_time,
                end_time=trade_end_time,
                direction=Order.SELL,  # 0 for sell, 1 for buy
                factor=self.trade_exchange.get_factor(
                    stock_id=code, start_time=trade_start_time, end_time=trade_end_time
                ),
            )

            if self.trade_exchange.check_order(sell_order):  # is order executable
                sell_order_list.append(sell_order)

                # StopLoss -> delete stop loss thresholds
                if self.hard_stop_loss or self.soft_stop_loss:
                    self.stop_loss.delete_threshold(code)

        ################################################################################################################

        # StopLoss -> Update remaining stop loss orders
        if (self.hard_stop_loss or self.soft_stop_loss) and self.trailing_stop_loss:
            self.stop_loss.update_thresholds(
                start_time=pred_start_time, end_time=pred_end_time, trade_exchange=self.trade_exchange
            )

        ################################################################################################################

        ########################################################################
        # # # IDENTIFY BUY SIGNALS FOR UNHELD STOCKS AND BUY THE BEST ONES # # #
        ########################################################################
        unheld_stock_scores = pred_score[~pred_score.index.isin(held_stock_scores.index)]
        buy_signals = unheld_stock_scores[unheld_stock_scores > self.buy_threshold]
        buy_signals = buy_signals.sort_values(ascending=False)

        # Calculate cash available for transactions
        available_cash = cash * self.get_account_risk_degree(start_time=pred_start_time, end_time=pred_end_time)

        # Calculate account value
        account_value = self.trade_position.calculate_value()

        # --------------------------------------------------------------------------------------------------------------

        # Update buy order list
        for code in buy_signals.index:  # Buy order
            if available_cash == 0:
                break
            # if not self.trade_exchange.is_stock_tradable(code, trade_start_time, trade_end_time):
            #     continue
            if not self.trade_exchange.is_stock_tradable(code, pred_start_time, pred_end_time):
                continue

            # Calculate the number of stocks to buy and cash spend
            buy_amount, cash_spend = self.buy__calculations(
                code,
                trade_start_time, trade_end_time,
                pred_start_time, pred_end_time,
                available_cash, account_value
            )

            if available_cash >= cash_spend and buy_amount > 0:
                buy_order = Order(
                    stock_id=code,
                    amount=buy_amount,
                    start_time=trade_start_time,
                    end_time=trade_end_time,
                    direction=Order.BUY,  # 1 for buy
                    factor=self.trade_exchange.get_factor(
                        stock_id=code, start_time=trade_start_time, end_time=trade_end_time
                    ),
                )
                buy_order_list.append(buy_order)

                # StopLoss -> Initialize stop loss threshold
                if self.hard_stop_loss or self.soft_stop_loss:
                    self.stop_loss.initialize_threshold(
                        code=code, start_time=pred_start_time, end_time=pred_end_time,
                        trade_exchange=self.trade_exchange
                    )

                # Update cash
                available_cash -= cash_spend

            else:  # Exit loop to speed up backtest
                break

        ################################################################################################################

        return TradeDecisionWO(sell_order_list + buy_order_list, self)

    def save_stop_loss(self, path):
        self.stop_loss.save_info(path='StopLoss_info.json')

    def load_stop_loss(self, path):
        self.stop_loss.load_info(path='StopLoss_info.json')

    def get_stop_loss_df(self):
        return self.stop_loss.get_thresholds()

# endregion
