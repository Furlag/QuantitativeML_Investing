''' This makes it so flake8 ignores all errors:  # flake8: noqa'''
# flake8: noqa

#######################################################################################################################
#  region --------------------------------------- Common Indicators ---------------------------------------------------

# Rate of Change Oscillator
def ROC(d=0, r=14):
    if d == 0:
        field = "($close / Ref($close, {r}))".format(r=r)
    else:
        field = "(Ref($close, {d}) / Ref($close, {dr}))".format(d=d, dr=d+r)
    return field


# Moving Average Convergence Divergence
def MACD(d=0):
    if d == 0:
        field = """(
            (EMA($close, 12) - EMA($close, 26))
            / EMA((EMA($close, 12) - EMA($close, 26)), 9)
        )"""
    else:
        field = """(
            (EMA(Ref($close, {d}), 12) - EMA(Ref($close, {d}), 26))
            / EMA((EMA(Ref($close, {d}), 12) - EMA(Ref($close, {d}), 26)), 9)
        )""".format(d=d)
    return field


# Stochastic Oscillator
def Stochastic_Oscillator(d=0, r=14):
    if d == 0:
        field = """(
            100
            * ($close - Min($low, {r}))
            / (Max($high, {r}) - Min($low, {r}))
        )""".format(r=r)
    else:
        field = """(
            100
            * (Ref($close, {d}) - Min(Ref($low, {d}), {r}))
            / (Max(Ref($high, {d}), {r}) - Min(Ref($low, {d}), {r}))
        )""".format(r=r, d=d)
    return field


# Williams Percent Range (Oscillator)
def Williams_Percent_Range(d=0, r=14):
    if d == 0:
        field = """(
            100
            * (Max($high, {r}) - $close)
            / (Max($high, {r}) - Min($low, {r}))
        )""".format(r=r)
    else:
        field = """(
            100
            * (Max(Ref($high, {d}), {r}) - Ref($close, {d}))
            / (Max(Ref($high, {d}), {r}) - Min(Ref($low, {d}), {r}))
        )""".format(r=r, d=d)
    return field


# Relative Strenght Indicator (Oscillator)
def RSI(d=0, r=14):
    if d == 0:
        field = """(
            100 - 100 /
            (
                1 + EMA($close > Ref($close, 1), {r})
                / EMA($close < Ref($close, 1), {r})
            )
        )""".format(r=r)
    else:
        field = """(
            100 - 100 /
            (
                1 + EMA(Ref($close, {d}) > Ref($close, {d1}), {r})
                / EMA(Ref($close, {d}) < Ref($close, {d1}), {r})
            )
        )""".format(r=r, d=d, d1=d+1)
    return field


# Aroon Oscillator
def Aroon_Up(d=0, r=25):
    if d == 0:
        field = "(100 * ({r} - IdxMax($high, {r})) / {r})".format(r=r)
    else:
        field = "(100 * ({r} - IdxMax(Ref($high, {d}), {r})) / {r})".format(r=r, d=d)
    return field


def Aroon_Down(d=0, r=25):
    if d == 0:
        field = "(100 * ({r} - IdxMin($low, {r})) / {r})".format(r=r)
    else:
        field = "(100 * ({r} - IdxMin(Ref($low, {d}), {r})) / {r})".format(r=r, d=d)
    return field


def Aroon_Oscillator(d=0, r=25):
    A_up = Aroon_Up(d=d, r=r)
    A_down = Aroon_Down(d=d, r=r)

    field = "(" + A_up + " - " + A_down + ")"
    return field


# Commodity Channel Indicator (Oscillator)
def CCI(d=0, r=20):
    if d == 0:
        field = """(
            (
                (($close + $high + $low) / 3)
                - Mean(($close + $high + $low) / 3, {r})
            )
            / (0.015 * Std(($close + $high + $low) / 3, {r}))
        )""".format(r=r)
    else:
        field = """(
            (
                ((Ref($close, {d}) + Ref($high, {d}) + Ref($low, {d})) / 3)
                - Mean((Ref($close, {d}) + Ref($high, {d}) + Ref($low, {d})) / 3, {r})
            )
            / (0.015 * Std((Ref($close, {d}) + Ref($high, {d}) + Ref($low, {d})) / 3, {r}))
        )""".format(r=r, d=d)
    return field


# Bollinger Bands
def Bollinger_Band(d=0, r=20, m=2, adapt=True):
    if adapt:  # Adapted for machine learning
        if d == 0:
            field = "({m} * Std($close, {r})) / (Mean($close, {r}))".format(r=r, m=m)
        else:
            field = "({m} * Std(Ref($close, {d}), {r}) / Mean(Ref($close, {d}), {r}))".format(r=r, d=d, m=m)
        return field
    else:  # Original indicator
        if d == 0:
            field = "({m} * Std($close, {r})) + (Mean($close, {r}))".format(r=r, m=m)
        else:
            field = "({m} * Std(Ref($close, {d}), {r}) + Mean(Ref($close, {d}), {r}))".format(r=r, d=d, m=m)
        return field


# Ichimoku Cloud
def Ichimoku_Cloud__tenkan_sen(d=0):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        return "(Mean($high, 9) + Mean($low, 9) / 2)"
    else:
        return "(Mean(Ref($high, %d), 9) + Mean(Ref($low, %d), 9) / 2)" % (d, d)


def Ichimoku_Cloud__kijun_sen(d=0):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        return "(Mean($high, 26) + Mean($low, 26) / 2)"
    else:
        return "(Mean(Ref($high, %d), 26) + Mean(Ref($low, %d), 26) / 2)" % (d, d)


def Ichimoku_Cloud__senkou_span_A(d=0):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        return """(
            (
                (Mean($high, 9) + Mean($low, 9) / 2)
                + (Mean($high, 26) + Mean($low, 26) / 2)
            ) / 2
        )"""
    else:
        return """(
            (
                (Mean(Ref($high, %d), 9) + Mean(Ref($low, %d), 9) / 2)
                + (Mean(Ref($high, %d), 26) + Mean(Ref($low, %d), 26) / 2)
            ) / 2
        )""" % (d, d, d, d),


def Ichimoku_Cloud__senkou_span_B(d=0):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        return "(Mean($high, 52) + Mean($low, 52) / 2)"
    else:
        return "(Mean(Ref($high, %d), 52) + Mean(Ref($low, %d), 52) / 2)" % (d, d)


def Ichimoku_Cloud__chikou_span(d=0):  # WARNING: Adapt for ML, don't use alone
    return "Ref($close, %d)" % (26+d)


# Directional Indicators
def Positive_DI(d=0, r=14):
    if d == 0:
        field = """(
            If(
                Mean(
                    Greater(
                        $high - $low,
                        Greater(
                            Abs($high - Ref($close, 1)),
                            Abs($low - Ref($close, 1))
                        )
                    ),
                    {r}
                ) == 0,
                0,
                100 * Div(
                    EMA(
                        If(
                            And($high - Ref($high, 1) > $low - Ref($low, 1), $high - Ref($high, 1) > 0),
                            $high - Ref($high, 1),
                            0
                        ),
                        {r}
                    ),
                    Mean(
                        Greater($high - $low,
                            Greater(
                                Abs($high - Ref($close, 1)),
                                Abs($low - Ref($close, 1))
                            )
                        ),
                        {r}
                    )
                )
            )
        )""".format(r=r)
    else:
        field = """(
            If(
                Mean(
                    Greater(
                        Ref($high, %d) - Ref($low, %d),
                        Greater(
                            Abs(Ref($high, %d) - Ref($close, %d)),
                            Abs(Ref($low, %d) - Ref($close, %d))
                        )
                    ),
                    %d
                ) == 0,
                0,
                100 * Div(
                    EMA(
                        If(
                            And(Ref($high, %d) - Ref($high, %d) > Ref($low, %d) - Ref($low, %d), Ref($high, %d) - Ref($high, %d) > 0),
                            Ref($high, %d) - Ref($high, %d),
                            0
                        ),
                        %d
                    ),
                    Mean(
                        Greater(
                            Ref($high, %d) - Ref($low, %d),
                            Greater(
                                Abs(Ref($high, %d)-Ref($close, %d)),
                                Abs(Ref($low, %d)-Ref($close, %d))
                            )
                        ),
                        %d
                    )
                )
            )
        )""" % (d, d, d, d+1, d, d+1, r, d, d+1, d, d+1, d, d+1, d, d+1, r, d, d, d, d+1, d, d+1, r)
    return field


def Negative_DI(d=0, r=14):
    if d == 0:
        field = """(
            If(
                Mean(
                    Greater(
                        $high-$low,
                        Greater(
                            Abs($high-Ref($close, 1)),
                            Abs($low-Ref($close, 1))
                        )
                    ),
                    {r}
                ) == 0,
                0,
                100 * Div(
                    EMA(
                        If(
                            And($low-Ref($low, 1) > $high-Ref($high, 1), $low-Ref($low, 1) > 0),
                            $low-Ref($low, 1),
                            0
                        ),
                        {r}
                    ),
                    Mean(
                        Greater(
                            $high-$low,
                            Greater(
                                Abs($high-Ref($close, 1)),
                                Abs($low-Ref($close, 1))
                            )
                        ),
                        {r}
                    )
                )
            )
        )""".format(r=r)
    else:
        field = """(
            If(
                Mean(
                    Greater(
                        Ref($high, %d)-Ref($low, %d),
                        Greater(
                            Abs(Ref($high, %d)-Ref($close, %d)),
                            Abs(Ref($low, %d)-Ref($close, %d))
                        )
                    ),
                    %d
                ) == 0,
                0,
                100 * Div(
                    EMA(
                        If(
                            And(Ref($low, %d)-Ref($low, %d) > Ref($high, %d)-Ref($high, %d), Ref($low, %d)-Ref($low, %d) > 0),
                            Ref($low, %d)-Ref($low, %d),
                            0
                        ),
                        %d
                    ),
                    Mean(
                        Greater(
                            Ref($high, %d) - Ref($low, %d),
                            Greater(
                                Abs(Ref($high, %d)-Ref($close, %d)),
                                Abs(Ref($low, %d)-Ref($close, %d))
                            )
                        ),
                        %d
                    )
                )
            )
        )""" % (d, d, d, d+1, d, d+1, r, d, d+1, d, d+1, d, d+1, d, d+1, r, d, d, d, d+1, d, d+1, r)
    return field


def ADX(d=0, r=14):
    p_DI = Positive_DI(d=d, r=r)
    n_DI = Negative_DI(d=d, r=r)

    field = "(100 * EMA(Abs(Div(Sub(" + p_DI + ", " + n_DI + "), Add(" + p_DI + ", " + n_DI + "))), {r}))".format(r=r)
    return field


def ATR(d=0, r=14):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        field = """(
            Mean(
                Greater(
                    $high - $low,
                    Greater(
                        Abs($high - Ref($close, 1)),
                        Abs($low - Ref($close, 1))
                    )
                ),
                {r}
            )
        )""".format(r=r)
    else:
        field = """(
            Mean(
                Greater(
                    Ref($high, {d}) - Ref($low, {d}),
                    Greater(
                        Abs(Ref($high, {d}) - Ref($close, {d1})),
                        Abs(Ref($low, {d}) - Ref($close, {d1})))
                    ),
                {r}
            )
        )""".format(r=r, d=d, d1=d+1)
    return field


def CHOP(d=0, r=14):
    if d == 0:
        field = """(
            100
            * Log(Sum({A_T_R}, {r}) / (Max($high, {r}) - Min($low, {r})))
            / Log($close-$close + {r})
        )""".format(A_T_R=ATR(d=d, r=1), r=r)
    else:
        field = """(
            100
            * Log(Sum({A_T_R}, {r}) / (Max(Ref($high, {d}), {r}) - Min(Ref($low, {d}), {r})))
            / Log($close-$close + {r})
        )""".format(A_T_R=ATR(d=d, r=1), r=r, d=d)
    return field


def Bulls_Power(d=0, r=14, adapt=True):
    if adapt:  # Adapted for machine learning
        if d == 0:
            field = """($high / EMA($close, {r}))""".format(r=r)
        else:
            field = """(Ref($high, {d}) / EMA(Ref($close, {d}), {r}))""".format(r=r, d=d)
        return field
    else:  # Original indicator
        if d == 0:
            field = """($high - EMA($close, {r}))""".format(r=r)
        else:
            field = """(Ref($high, {d}) - EMA(Ref($close, {d}), {r}))""".format(r=r, d=d)
        return field


def Bears_Power(d=0, r=14, adapt=True):
    if adapt:  # Adapted for machine learning
        if d == 0:
            field = """($low / EMA($close, {r}))""".format(r=r)
        else:
            field = """(Ref($low, {d}) / EMA(Ref($close, {d}), {r}))""".format(r=r, d=d)
        return field
    else:  # Original indicator
        if d == 0:
            field = """($low - EMA($close, {r}))""".format(r=r)
        else:
            field = """(Ref($low, {d}) - EMA(Ref($close, {d}), {r}))""".format(r=r, d=d)
        return field


def Money_Flow_Index(d=0, r=14):
    if d == 0:
        field = """(
            100 - 100 /
            (1 +
                Sum(
                    If(
                        ($high + $low + $close)/3 > (Ref($high, 1) + Ref($low, 1) + Ref($close, 1))/3,
                        ($high + $low + $close)/3 * $volume,
                        0
                    ),
                    {r}
                )
                / Sum(
                    If(
                        ($high + $low + $close)/3  < (Ref($high, 1) + Ref($low, 1) + Ref($close, 1))/3,
                        ($high + $low + $close)/3 * $volume,
                        0
                    ),
                    {r}
                )
            )
        )""".format(r=r)
    else:
        field = """(
            100 - 100 /
            (1 +
                Sum(
                    If(
                        (Ref($high, {d}) + Ref($low, {d}) + Ref($close, {d}))/3 > (Ref($high, {d1}) + Ref($low, {d1}) + Ref($close, {d1}))/3,
                        (Ref($high, {d}) + Ref($low, {d}) + Ref($close, {d}))/3 * Ref($volume, {d}),
                        0
                    ),
                    {r}
                )
                / Sum(
                    If(
                        (Ref($high, {d}) + Ref($low, {d}) + Ref($close, {d}))/3 < (Ref($high, {d1}) + Ref($low, {d1}) + Ref($close, {d1}))/3,
                        (Ref($high, {d}) + Ref($low, {d}) + Ref($close, {d}))/3 * Ref($volume, {d}),
                        0
                    ),
                    {r}
                )
            )
        )""".format(r=r, d=d, d1=d+1)
    return field


def OBV(d=0):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        field = """(
            Sum(
                If(
                    $close == Ref($close, 1),
                    0,
                    If(
                        $close > Ref($close, 1),
                        $volume,
                        0 - $volume
                    )
                ),
                0
            )
        )"""
    else:
        field = """(
            Sum(
                If(
                    Ref($close, {d}) == Ref($close, {d1}),
                    0,
                    If(
                        Ref($close, {d}) > Ref($close, {d1}),
                        Ref($volume, {d}),
                        0 - Ref($volume, {d})
                    )
                ),
                0
            )
        )""".format(d=d, d1=d+1)
    return field


def AD_Line(d=0):  # WARNING: Adapt for ML, don't use alone
    if d == 0:
        field = """(
            Sum(
                (
                    (($close - $low) - ($high - $close))
                    / ($high - $low) * $volume
                ),
                0
            )
        )"""
    else:
        field = """(
            Sum(
                (
                    ((Ref($close, {d}) - Ref($low, {d})) - (Ref($high, {d}) - Ref($close, {d})))
                    / (Ref($high, {d}) - Ref($low, {d})) * Ref($volume, {d})
                ),
                0
            )
        )""".format(d=d)
    return field

#  endregion

#######################################################################################################################
#######################################################################################################################
#  region -------------------------------------------- Features -------------------------------------------------------


def dataset_features_ts_185():
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- BASIC FEATURES -------------------------------------- ########
    ###############################################################################################################

    #######################
    # # # CURRENT DAY # # #
    #######################
    fields += [
        "$high/$close",
        "$low/$close",
        "$open/$close",

        "$high/$low",
    ]
    names += [
        "HIGH/CLOSE",
        "LOW/CLOSE",
        "OPEN/CLOSE",

        "HIGH/LOW",
    ]

    # Hardcoded kbar features
    fields += [
        "($high-$low)/$close",
        "($close-$open)/($high-$low+1e-12)",
        "($high-Greater($open, $close))/$close",
        "($high-Greater($open, $close))/($high-$low+1e-12)",
        "(Less($open, $close)-$low)/$close",
        "(Less($open, $close)-$low)/($high-$low+1e-12)",
        "(2*$close-$high-$low)/$close",
        "(2*$close-$high-$low)/($high-$low+1e-12)",
    ]
    names += [
        "KLEN",
        "KMID2",
        "KUP",
        "KUP2",
        "KLOW",
        "KLOW2",
        "KSFT",
        "KSFT2",
    ]

    #######################################
    # # # CURRENT DAY vs PREVIOUS DAY # # #
    #######################################
    fields += [
        "$close/Ref($close, 1)",

        "$open/Ref($close, 1)",

        "$open/Ref($open, 1)"
    ]
    names += [
        "CLOSE/CLOSE(1)",

        "OPEN/CLOSE(1)",

        "OPEN/OPEN(1)"
    ]

    ###############################
    # # # HEIKIN-ASHI CANDLES # # #
    ###############################
    # fields += [
    #     "(((0.25 * ($open + $high + $low + $close)) / (0.5 * (Ref($open, 1) + Ref($close, 1)))) - 1)"
    # ]
    # names += [
    #     "HEIKIN ASHI CANDLE"
    # ]

    # endregion

    ###############################################################################################################
    # region ------------------------------- ROLLING FEATURES (Mean based) ------------------------------- ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    #######
    # EMA #
    #######
    windows = [5, 8, 12, 26, 50, 100, 200]

    # Price vs EMA
    fields += ["$close/EMA($close, %d)" % d for d in windows]
    names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_EMA_%d(close))" % (d) for d in windows]

    # EMA 5 / EMA 8
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1)"]
    names += ["EMA_5(close)/EMA_8(close)"]
    # EMA 12 / EMA 26
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1)"]
    names += ["EMA_12(close)/EMA_26(close)"]
    # EMA 26 / EMA 50
    fields += ["(EMA($close, 26)/EMA($close, 50) - 1)"]
    names += ["EMA_26(close)/EMA_50(close)"]
    # EMA 50 / EMA 200
    fields += ["(EMA($close, 50)/EMA($close, 200) - 1)"]
    names += ["EMA_50(close)/EMA_200(close)"]

    #######
    # SMA #
    #######
    windows = [5, 10, 30, 50, 100, 200]

    # Price vs SMA
    fields += ["$close/Mean($close, %d)" % d for d in windows]
    names += ["close/Mean_%d(close)" % d for d in windows]
    # SMA variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_Mean_%d(close)" % (d) for d in windows]

    # SMA 10 / SMA 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]
    # SMA 10 / SMA 30
    fields += ["(Mean($close, 10)/Mean($close, 30) - 1)"]
    names += ["Mean_10(close)/Mean_30(close)"]
    # SMA 20 / SMA 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]
    # SMA 50 / SMA 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    ################
    # # # OPEN # # #
    ################

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # EMA HIGH 5 / EMA CLOSE 5
    fields += ["(EMA($high, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(high)/EMA_5(close)"]

    # EMA LOW 5 / EMA CLOSE 5
    fields += ["(EMA($low, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(low)/EMA_5(close)"]

    # EMA OPEN 5 / EMA CLOSE(1) 5
    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["EMA_5(open)/EMA_5(close(1))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ ROLLING FEATURES (Statistical Significance) ------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    # STANDARD DEVIATION
    windows = [10, 20, 50]
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # BETA
    windows = [30, 60, 90]
    fields += ["Slope($close, %d)/$close" % d for d in windows]
    names += ["BETA_%d(close)/close" % d for d in windows]
    # RESIDUALS
    windows = [30, 60, 90]
    fields += ["Resi($close, %d)/$close" % d for d in windows]
    names += ["RESI_%d(close)/close" % d for d in windows]

    # QUANTILES
    windows = [25, 50, 75]
    fields += ["Quantile($close, %d, 0.8)/$close" % d for d in windows]
    names += ["QTLU_%d(close)/close" % d for d in windows]
    fields += ["Quantile($close, %d, 0.2)/$close" % d for d in windows]
    names += ["QTLD_%d(close)/close" % d for d in windows]

    # RANK
    windows = [10, 50, 200]
    fields += ["Rank($close, %d)" % d for d in windows]
    names += ["RANK_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################
    windows = [10, 20, 50]
    fields += ["Std($open, %d)/$open" % d for d in windows]
    names += ["STD_%d(open)/open" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [50]
    fields += ["Corr($close, $open, %d)" % d for d in windows]
    names += ["CORR_%d(close/open)" % d for d in windows]

    ################################################
    # # # RSQR -> Explained variance of target # # #
    ################################################
    # windows = []
    # fields += ["Rsquare($close, %d)" % d for d in windows]
    # names += ["RSQR_%d(close)" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ----------------------------- ROLLING FEATURES (Miscellaneous) ------------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    windows = [20, 50, 100, 200]

    fields += ["Mean($close>Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTP_%d(close)" % d for d in windows]

    fields += ["Mean($close<Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTN_%d(close)" % d for d in windows]

    fields += ["Mean($close>Ref($close, 1), %d)-Mean($close<Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["CNTD_%d(close)" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Sum(Greater($close-Ref($close, 1), 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
        for d in windows
    ]
    names += ["SUMP_%d(close)" % d for d in windows]

    # fields += [
    #     "Sum(Greater(Ref($close, 1)-$close, 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
    #     for d in windows
    # ]
    # names += ["SUMN_%d(close)" % d for d in windows]

    # fields += [
    #     "(Sum(Greater($close-Ref($close, 1), 0), %d)-Sum(Greater(Ref($close, 1)-$close, 0), %d))"
    #     "/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d, d)
    #     for d in windows
    # ]
    # names += ["SUMD_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################

    # endregion

    ###############################################################################################################
    # region --------------------------------- MAX & MIN BASED FEATURES ---------------------------------- ########
    ###############################################################################################################

    # Note to self: Should do something to get a more precise look at Resistances and Supports

    windows = [10, 20, 50, 100, 200]
    fields += ["Max($high, %d)/$close" % d for d in windows]
    names += ["MAX%d" % d for d in windows]

    fields += ["Min($low, %d)/$close" % d for d in windows]
    names += ["MIN%d" % d for d in windows]

    fields += ["Max($high, %d)/Min($low, %d)" % (d, d) for d in windows]
    names += ["MAX/MIN%d" % d for d in windows]

    windows = [10, 20, 50, 100, 200]
    fields += ["(Max($high, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MAXvsMEAN/CLOSE%d" % d for d in windows]

    fields += ["(Min($low, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MINvsMEAN/CLOSE%d" % d for d in windows]

    windows = [20, 50, 100, 200]
    fields += ["IdxMax($high, %d)/%d" % (d, d) for d in windows]
    names += ["IMAX%d" % d for d in windows]

    fields += ["IdxMin($low, %d)/%d" % (d, d) for d in windows]
    names += ["IMIN%d" % d for d in windows]

    fields += ["(IdxMax($high, %d)-IdxMin($low, %d))/%d" % (d, d, d) for d in windows]
    names += ["IMAX/IMIN%d" % d for d in windows]

    #########################################
    # # # SUPPORT AND RESISTANCE LEVELS # # #
    #########################################
    support = """
        If(
            And(
                And(
                    $low < Ref($low, 1),
                    And(
                        Ref($low, 1) < Ref($low, 2),
                        Ref($low, 2) < Ref($low, 3)
                    )
                ),
                And(
                    $low < Ref($low, -1),
                    And(
                        Ref($low, -1) < Ref($low, -2),
                        Ref($low, -2) < Ref($low, -3)
                    )
                )
            ),
            $low,
            0
        )
    """
    resistance = """
        If(
            And(
                And(
                    $high > Ref($high, 1),
                    And(
                        Ref($high, 1) > Ref($high, 2),
                        Ref($ligh, 2) > Ref($high, 3)
                    )
                ),
                And(
                    $high > Ref($high, -1),
                    And(
                        Ref($high, -1) > Ref($high, -2),
                        Ref($high, -2) > Ref($high, -3)
                    )
                )
            ),
            $high,
            0
        )
    """

    # endregion

    ###############################################################################################################
    # region ---------------------------------------- INDICATORS ----------------------------------------- ########
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [MACD()]
    names += ["MACD"]

    ##########################
    # # # Ichimoku Cloud # # #
    ##########################
    fields += [
                Ichimoku_Cloud__tenkan_sen() + " / " + Ichimoku_Cloud__kijun_sen(),
                Ichimoku_Cloud__tenkan_sen() + " / $close",
                Ichimoku_Cloud__kijun_sen() + " / $close",

                Ichimoku_Cloud__senkou_span_A() + " / $close",
                Ichimoku_Cloud__senkou_span_B() + " / $close",

                Ichimoku_Cloud__chikou_span() + " / $close"
            ]
    names += [
            "tenkan_sen / kijun_sen",
            "tenkan_sen / close",
            "kijun_sen / close",

            "senkou_span_A / close",
            "senkou_span_B / close",

            "chikou_span / close"
            ]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [Bollinger_Band(r=20)]
    names += ["Bollinger Band"]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 7
    fields += [
        Stochastic_Oscillator(r=7),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=7), Stochastic_Oscillator(r=7))
    ]
    names += [
        "fast_Stochastic_Oscillator(7)",
        "fast_Stochastic_Oscillator(7)-slow_Stochastic_Oscillator(7)"
    ]
    # SO 14
    fields += [
        Stochastic_Oscillator(r=14),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=14), Stochastic_Oscillator(r=14))
    ]
    names += [
        "fast_Stochastic_Oscillator(14)",
        "fast_Stochastic_Oscillator(14)-slow_Stochastic_Oscillator(14)"
    ]
    # SO 21
    fields += [
        Stochastic_Oscillator(r=21),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=21), Stochastic_Oscillator(r=21))
    ]
    names += [
        "fast_Stochastic_Oscillator(21)",
        "fast_Stochastic_Oscillator(21)-slow_Stochastic_Oscillator(21)"
    ]

    #########################################
    # # # Relative Strenght Index (RSI) # # #
    #########################################
    fields += [RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        Aroon_Up(r=14),
        Aroon_Down(r=14),
        Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        Aroon_Up(r=25),
        Aroon_Down(r=25),
        Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    ##################################
    # # # Comodity Channel (CCI) # # #
    ##################################

    # CCI 14
    fields += [CCI(r=14)]
    names += ["CCI_14"]
    # CCI 20
    fields += [CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    fields += [Positive_DI()]
    names += ["Positive_DI"]

    fields += [Negative_DI()]
    names += ["Negative_DI"]

    fields += ["(%s - %s)" % (Positive_DI(), Negative_DI())]
    names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [ADX(r=14)]
    names += ["ADX"]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ATR() + " / $close"]
    names += ["ATR / close"]

    fields += [ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        Bulls_Power(),
        Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    # OBV
    fields += [OBV() + " / " + OBV(d=1)]
    names += ["OBV / OBV(1)"]

    # Accumulation/Distribution Line
    fields += [AD_Line() + " / " + AD_Line(d=1)]
    names += ["AD_Line / AD_Line(1)"]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- VOLUME BASED FEATURES ------------------------------------ ########
    ###############################################################################################################

    ############################
    # # # VOLUME VARIATION # # #
    ############################
    fields += ["If(Ref($volume, 1) == 0, 0, $volume/(Ref($volume, 1)))"]
    names += ["VOLUME/VOLUME(1)"]

    ######################
    # # # MEAN BASED # # #
    ######################
    windows = [50]
    fields += ["If($volume == 0, 0, $volume/Mean($volume, %d))" % d for d in windows]
    names += ["VMA%d" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [20]
    fields += ["Std($volume, %d)/($volume+1e-12)" % d for d in windows]
    names += ["VSTD%d" % d for d in windows]

    windows = [20]
    fields += ["Corr($close, Log($volume+1), %d)" % d for d in windows]
    names += ["CORRV%d" % d for d in windows]

    windows = [20, 50, 100, 200]
    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, %d)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["WVMA%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        """
        If(Or(Or($close == 0, $volume == 0), Or(Ref($close,1) == 0, Ref($volume,1) == 0)),
        0, Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), %d))
        """
        % d for d in windows
    ]
    names += ["CORDV%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Sum(Greater($volume-Ref($volume, 1), 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["VSUMP%d" % d for d in windows]

    # fields += [
    #     "Sum(Greater(Ref($volume, 1)-$volume, 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
    #     % (d, d)
    #     for d in windows
    # ]
    # names += ["VSUMN%d" % d for d in windows]

    # fields += [
    #     "(Sum(Greater($volume-Ref($volume, 1), 0), %d)-Sum(Greater(Ref($volume, 1)-$volume, 0), %d))"
    #     "/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)" % (d, d, d)
    #     for d in windows
    # ]
    # names += ["VSUMD%d" % d for d in windows]

    # endregion

    # -------------------------------------------------------------------------------------------------------------

    return fields, names


def dataset_features_ts_210():
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- BASIC FEATURES -------------------------------------- ########
    ###############################################################################################################

    #######################
    # # # CURRENT DAY # # #
    #######################
    fields += [
        "$high/$close",
        "$low/$close",
        "$open/$close",

        "$high/$low",
    ]
    names += [
        "HIGH/CLOSE",
        "LOW/CLOSE",
        "OPEN/CLOSE",

        "HIGH/LOW",
    ]

    # Hardcoded kbar features
    fields += [
        "($high-$low)/$close",
        "($close-$open)/($high-$low+1e-12)",
        "($high-Greater($open, $close))/$close",
        "($high-Greater($open, $close))/($high-$low+1e-12)",
        "(Less($open, $close)-$low)/$close",
        "(Less($open, $close)-$low)/($high-$low+1e-12)",
        "(2*$close-$high-$low)/$close",
        "(2*$close-$high-$low)/($high-$low+1e-12)",
    ]
    names += [
        "KLEN",
        "KMID2",
        "KUP",
        "KUP2",
        "KLOW",
        "KLOW2",
        "KSFT",
        "KSFT2",
    ]

    #######################################
    # # # CURRENT DAY vs PREVIOUS DAY # # #
    #######################################
    fields += [
        "$close/Ref($close, 1)",

        "$open/Ref($close, 1)",

        "$open/Ref($open, 1)"
    ]
    names += [
        "CLOSE/CLOSE(1)",

        "OPEN/CLOSE(1)",

        "OPEN/OPEN(1)"
    ]

    ###############################
    # # # HEIKIN-ASHI CANDLES # # #
    ###############################
    # fields += [
    #     "(((0.25 * ($open + $high + $low + $close)) / (0.5 * (Ref($open, 1) + Ref($close, 1)))) - 1)"
    # ]
    # names += [
    #     "HEIKIN ASHI CANDLE"
    # ]

    # endregion

    ###############################################################################################################
    # region ------------------------------- ROLLING FEATURES (Mean based) ------------------------------- ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    #######
    # EMA #
    #######
    windows = [5, 8, 12, 26, 50, 100, 200]

    # Price vs EMA
    fields += ["$close/EMA($close, %d)" % d for d in windows]
    names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_EMA_%d(close))" % (d) for d in windows]

    # EMA 5 / EMA 8
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1)"]
    names += ["EMA_5(close)/EMA_8(close)"]
    # EMA 12 / EMA 26
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1)"]
    names += ["EMA_12(close)/EMA_26(close)"]
    # EMA 26 / EMA 50
    fields += ["(EMA($close, 26)/EMA($close, 50) - 1)"]
    names += ["EMA_26(close)/EMA_50(close)"]
    # EMA 50 / EMA 200
    fields += ["(EMA($close, 50)/EMA($close, 200) - 1)"]
    names += ["EMA_50(close)/EMA_200(close)"]

    #######
    # SMA #
    #######
    windows = [5, 10, 30, 50, 100, 200]

    # Price vs SMA
    fields += ["$close/Mean($close, %d)" % d for d in windows]
    names += ["close/Mean_%d(close)" % d for d in windows]
    # SMA variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_Mean_%d(close)" % (d) for d in windows]

    # SMA 5 / SMA 10
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1)"]
    names += ["Mean_5(close)/Mean_10(close)"]
    # SMA 10 / SMA 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]
    # SMA 10 / SMA 30
    fields += ["(Mean($close, 10)/Mean($close, 30) - 1)"]
    names += ["Mean_10(close)/Mean_30(close)"]
    # SMA 20 / SMA 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]
    # SMA 50 / SMA 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    ################
    # # # OPEN # # #
    ################

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # EMA HIGH 5 / EMA CLOSE 5
    fields += ["(EMA($high, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(high)/EMA_5(close)"]

    # EMA LOW 5 / EMA CLOSE 5
    fields += ["(EMA($low, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(low)/EMA_5(close)"]

    # EMA OPEN 5 / EMA CLOSE(1) 5
    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["EMA_5(open)/EMA_5(close(1))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ ROLLING FEATURES (Statistical Significance) ------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    # STANDARD DEVIATION
    windows = [10, 20, 50]
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # BETA
    windows = [30, 60, 90]
    fields += ["Slope($close, %d)/$close" % d for d in windows]
    names += ["BETA_%d(close)/close" % d for d in windows]
    # RESIDUALS
    windows = [30, 60, 90]
    fields += ["Resi($close, %d)/$close" % d for d in windows]
    names += ["RESI_%d(close)/close" % d for d in windows]

    # QUANTILES
    windows = [25, 50, 75]
    fields += ["Quantile($close, %d, 0.8)/$close" % d for d in windows]
    names += ["QTLU_%d(close)/close" % d for d in windows]
    fields += ["Quantile($close, %d, 0.2)/$close" % d for d in windows]
    names += ["QTLD_%d(close)/close" % d for d in windows]

    # RANK
    windows = [10, 50, 200]
    fields += ["Rank($close, %d)" % d for d in windows]
    names += ["RANK_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################
    windows = [10, 20, 50]
    fields += ["Std($open, %d)/$open" % d for d in windows]
    names += ["STD_%d(open)/open" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [10, 20, 50]
    fields += ["Corr($open, Ref($close, 1), %d)" % d for d in windows]
    names += ["CORR_%d(open/close(1))" % d for d in windows]

    ################################################
    # # # RSQR -> Explained variance of target # # #
    ################################################
    # windows = []
    # fields += ["Rsquare($close, %d)" % d for d in windows]
    # names += ["RSQR_%d(close)" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ----------------------------- ROLLING FEATURES (Miscellaneous) ------------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    windows = [20, 50, 100, 200]

    fields += ["Mean($close>Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTP_%d(close)" % d for d in windows]

    fields += ["Mean($close<Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTN_%d(close)" % d for d in windows]

    fields += ["Mean($close>Ref($close, 1), %d)-Mean($close<Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["CNTD_%d(close)" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Sum(Greater($close-Ref($close, 1), 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
        for d in windows
    ]
    names += ["SUMP_%d(close)" % d for d in windows]

    # fields += [
    #     "Sum(Greater(Ref($close, 1)-$close, 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
    #     for d in windows
    # ]
    # names += ["SUMN_%d(close)" % d for d in windows]

    # fields += [
    #     "(Sum(Greater($close-Ref($close, 1), 0), %d)-Sum(Greater(Ref($close, 1)-$close, 0), %d))"
    #     "/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d, d)
    #     for d in windows
    # ]
    # names += ["SUMD_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################

    # endregion

    ###############################################################################################################
    # region --------------------------------- MAX & MIN BASED FEATURES ---------------------------------- ########
    ###############################################################################################################

    # Note to self: Should do something to get a more precise look at Resistances and Supports

    windows = [10, 20, 50, 100, 200]
    fields += ["Max($high, %d)/$close" % d for d in windows]
    names += ["MAX%d" % d for d in windows]

    fields += ["Min($low, %d)/$close" % d for d in windows]
    names += ["MIN%d" % d for d in windows]

    fields += ["Max($high, %d)/Min($low, %d)" % (d, d) for d in windows]
    names += ["MAX/MIN%d" % d for d in windows]

    windows = [10, 20, 50, 100, 200]
    fields += ["(Max($high, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MAXvsMEAN/CLOSE%d" % d for d in windows]

    fields += ["(Min($low, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MINvsMEAN/CLOSE%d" % d for d in windows]

    windows = [20, 50, 100, 200]
    fields += ["IdxMax($high, %d)/%d" % (d, d) for d in windows]
    names += ["IMAX%d" % d for d in windows]

    fields += ["IdxMin($low, %d)/%d" % (d, d) for d in windows]
    names += ["IMIN%d" % d for d in windows]

    fields += ["(IdxMax($high, %d)-IdxMin($low, %d))/%d" % (d, d, d) for d in windows]
    names += ["IMAX/IMIN%d" % d for d in windows]

    #########################################
    # # # SUPPORT AND RESISTANCE LEVELS # # #
    #########################################
    support = """
        If(
            And(
                And(
                    $low < Ref($low, 1),
                    And(
                        Ref($low, 1) < Ref($low, 2),
                        Ref($low, 2) < Ref($low, 3)
                    )
                ),
                And(
                    $low < Ref($low, -1),
                    And(
                        Ref($low, -1) < Ref($low, -2),
                        Ref($low, -2) < Ref($low, -3)
                    )
                )
            ),
            $low,
            0
        )
    """
    resistance = """
        If(
            And(
                And(
                    $high > Ref($high, 1),
                    And(
                        Ref($high, 1) > Ref($high, 2),
                        Ref($ligh, 2) > Ref($high, 3)
                    )
                ),
                And(
                    $high > Ref($high, -1),
                    And(
                        Ref($high, -1) > Ref($high, -2),
                        Ref($high, -2) > Ref($high, -3)
                    )
                )
            ),
            $high,
            0
        )
    """

    # endregion

    ###############################################################################################################
    # region ---------------------------------------- INDICATORS ----------------------------------------- ########
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [MACD()]
    names += ["MACD"]

    ##########################
    # # # Ichimoku Cloud # # #
    ##########################
    fields += [
                Ichimoku_Cloud__tenkan_sen() + " / " + Ichimoku_Cloud__kijun_sen(),
                Ichimoku_Cloud__tenkan_sen() + " / $close",
                Ichimoku_Cloud__kijun_sen() + " / $close",

                Ichimoku_Cloud__senkou_span_A() + " / $close",
                Ichimoku_Cloud__senkou_span_B() + " / $close",

                Ichimoku_Cloud__chikou_span() + " / $close"
            ]
    names += [
            "tenkan_sen / kijun_sen",
            "tenkan_sen / close",
            "kijun_sen / close",

            "senkou_span_A / close",
            "senkou_span_B / close",

            "chikou_span / close"
            ]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [Bollinger_Band(r=20)]
    names += ["Bollinger Band"]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 7
    fields += [
        Stochastic_Oscillator(r=7),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=7), Stochastic_Oscillator(r=7))
    ]
    names += [
        "fast_Stochastic_Oscillator(7)",
        "fast_Stochastic_Oscillator(7)-slow_Stochastic_Oscillator(7)"
    ]
    # SO 14
    fields += [
        Stochastic_Oscillator(r=14),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=14), Stochastic_Oscillator(r=14))
    ]
    names += [
        "fast_Stochastic_Oscillator(14)",
        "fast_Stochastic_Oscillator(14)-slow_Stochastic_Oscillator(14)"
    ]
    # SO 21
    fields += [
        Stochastic_Oscillator(r=21),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=21), Stochastic_Oscillator(r=21))
    ]
    names += [
        "fast_Stochastic_Oscillator(21)",
        "fast_Stochastic_Oscillator(21)-slow_Stochastic_Oscillator(21)"
    ]

    #########################################
    # # # Relative Strenght Index (RSI) # # #
    #########################################
    fields += [RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        Aroon_Up(r=14),
        Aroon_Down(r=14),
        Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        Aroon_Up(r=25),
        Aroon_Down(r=25),
        Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    ##################################
    # # # Comodity Channel (CCI) # # #
    ##################################

    # CCI 14
    fields += [CCI(r=14)]
    names += ["CCI_14"]
    # CCI 20
    fields += [CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    fields += [Positive_DI()]
    names += ["Positive_DI"]

    fields += [Negative_DI()]
    names += ["Negative_DI"]

    fields += ["(%s - %s)" % (Positive_DI(), Negative_DI())]
    names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [ADX(r=14)]
    names += ["ADX"]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ATR() + " / $close"]
    names += ["ATR / close"]

    fields += [ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        Bulls_Power(),
        Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ##########################################
    # # # Accumulation/Distribution Line # # #
    ##########################################
    # Removed #

    ###############
    # # # OBV # # #
    ###############
    fields += ["If(%s > 0, 1, 0)" % (OBV())]
    names += ["OBV_sign"]

    windows = [5, 10, 30, 50, 100, 200]

    p_OBV = "{s}+Abs(Min({s}, 0))".format(s=OBV())  # Always positive OBV

    # SMA variation
    fields += ["Mean({s}, {d})/Mean(Ref({s}, 1), {d})".format(s=p_OBV, d=d) for d in windows]
    names += ["Change_Mean_%d(OBV)" % (d) for d in windows]

    # SMA 10 / SMA 20
    fields += ["(Mean({s}, 10)/Mean({s}, 20) - 1)".format(s=p_OBV)]
    names += ["Mean_10(OBV)/Mean_20(OBV)"]
    # SMA 10 / SMA 30
    fields += ["(Mean({s}, 10)/Mean({s}, 30) - 1)".format(s=p_OBV)]
    names += ["Mean_10(OBV)/Mean_30(OBV)"]
    # SMA 20 / SMA 50
    fields += ["(Mean({s}, 20)/Mean({s}, 50) - 1)".format(s=p_OBV)]
    names += ["Mean_20(OBV)/Mean_50(OBV)"]
    # SMA 50 / SMA 200
    fields += ["(Mean({s}, 50)/Mean({s}, 200) - 1)".format(s=p_OBV)]
    names += ["Mean_50(OBV)/Mean_200(OBV)"]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- VOLUME BASED FEATURES ------------------------------------ ########
    ###############################################################################################################

    ############################
    # # # VOLUME VARIATION # # #
    ############################
    fields += ["If(Ref($volume, 1) == 0, 0, $volume/(Ref($volume, 1)))"]
    names += ["VOLUME/VOLUME(1)"]

    ######################
    # # # MEAN BASED # # #
    ######################
    windows = [50]
    fields += ["If($volume == 0, 0, $volume/Mean($volume, %d))" % d for d in windows]
    names += ["VMA%d" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [20]
    fields += ["Std($volume, %d)/($volume+1e-12)" % d for d in windows]
    names += ["VSTD%d" % d for d in windows]

    windows = [20]
    fields += ["Corr($close, Log($volume+1), %d)" % d for d in windows]
    names += ["CORRV%d" % d for d in windows]

    windows = [20, 50, 100, 200]
    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, %d)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["WVMA%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        """
        If(Or(Or($close == 0, $volume == 0), Or(Ref($close,1) == 0, Ref($volume,1) == 0)),
        0, Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), %d))
        """
        % d for d in windows
    ]
    names += ["CORDV%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Sum(Greater($volume-Ref($volume, 1), 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["VSUMP%d" % d for d in windows]

    # fields += [
    #     "Sum(Greater(Ref($volume, 1)-$volume, 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
    #     % (d, d)
    #     for d in windows
    # ]
    # names += ["VSUMN%d" % d for d in windows]

    # fields += [
    #     "(Sum(Greater($volume-Ref($volume, 1), 0), %d)-Sum(Greater(Ref($volume, 1)-$volume, 0), %d))"
    #     "/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)" % (d, d, d)
    #     for d in windows
    # ]
    # names += ["VSUMD%d" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- MARKET INDEX FEATURES ------------------------------------ ########
    ###############################################################################################################
    
    ###############
    # CORRELATION #
    ###############
    windows = [5]
    fields += ["Corr($close, $close_idx, %d)" % d for d in windows]
    names += ["CORR_%d(close/close_idx)" % d for d in windows]

    #######################
    # # # CURRENT DAY # # #
    #######################
    fields += [
        "$high_idx/$close_idx",
        "$low_idx/$close_idx",
        "$open_idx/$close_idx",

        "$high_idx/$low_idx",
    ]
    names += [
        "HIGH_idx/CLOSE_idx",
        "LOW_idx/CLOSE_idx",
        "OPEN_idx/CLOSE_idx",

        "HIGH_idx/LOW_idx",
    ]

    #######################################
    # # # CURRENT DAY vs PREVIOUS DAY # # #
    #######################################
    fields += [
        "$close_idx/Ref($close_idx, 1)",
        "$open_idx/Ref($close_idx, 1)"
    ]
    names += [
        "CLOSE_idx/CLOSE_idx(1)",
        "OPEN_idx/CLOSE_idx(1)"
    ]
    
    #######
    # SMA #
    #######
    windows = [5, 10]

    # Price vs SMA
    fields += ["$close_idx/Mean($close_idx, %d)" % d for d in windows]
    names += ["close_idx/Mean_%d(close_idx)" % d for d in windows]
    # SMA variation
    fields += ["Mean($close_idx, %d)/Mean(Ref($close_idx, 1), %d)" % (d, d) for d in windows]
    names += ["Change_Mean_%d(close_idx)" % (d) for d in windows]

    # SMA 5 / SMA 10
    fields += ["(Mean($close_idx, 5)/Mean($close_idx, 10) - 1)"]
    names += ["Mean_5(close_idx)/Mean_10(close_idx)"]

    # endregion

    # -------------------------------------------------------------------------------------------------------------

    return fields, names


def dataset_features_ts_235():
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- BASIC FEATURES -------------------------------------- ########
    ###############################################################################################################

    #######################
    # # # CURRENT DAY # # #
    #######################
    fields += [
        "$high/$close",
        "$low/$close",
        "$open/$close",
    ]
    names += [
        "HIGH/CLOSE",
        "LOW/CLOSE",
        "OPEN/CLOSE",
    ]

    # Hardcoded kbar features
    fields += [
        "($high-$low)/$close",
        "($close-$open)/($high-$low+1e-12)",
        "($high-Greater($open, $close))/$close",
        "($high-Greater($open, $close))/($high-$low+1e-12)",
        "(Less($open, $close)-$low)/$close",
        "(Less($open, $close)-$low)/($high-$low+1e-12)",
        "(2*$close-$high-$low)/$close",
        "(2*$close-$high-$low)/($high-$low+1e-12)",
    ]
    names += [
        "KLEN",
        "KMID2",
        "KUP",
        "KUP2",
        "KLOW",
        "KLOW2",
        "KSFT",
        "KSFT2",
    ]

    #######################################
    # # # CURRENT DAY vs PREVIOUS DAY # # #
    #######################################
    fields += [
        "$close/Ref($close, 1)",

        "$open/Ref($close, 1)",

        "$open/Ref($open, 1)"
    ]
    names += [
        "CLOSE/CLOSE(1)",

        "OPEN/CLOSE(1)",

        "OPEN/OPEN(1)"
    ]

    ###############################
    # # # HEIKIN-ASHI CANDLES # # #
    ###############################
    # fields += [
    #     "(((0.25 * ($open + $high + $low + $close)) / (0.5 * (Ref($open, 1) + Ref($close, 1)))) - 1)"
    # ]
    # names += [
    #     "HEIKIN ASHI CANDLE"
    # ]

    # endregion

    ###############################################################################################################
    # region ------------------------------- ROLLING FEATURES (Mean based) ------------------------------- ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    #######
    # EMA #
    #######
    windows = [5, 8, 12, 26, 50, 100, 200]

    # Price vs EMA
    fields += ["$close/EMA($close, %d)" % d for d in windows]
    names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_EMA_%d(close))" % (d) for d in windows]

    # EMA 5 / EMA 8
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1)"]
    names += ["EMA_5(close)/EMA_8(close)"]
    # EMA 12 / EMA 26
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1)"]
    names += ["EMA_12(close)/EMA_26(close)"]
    # EMA 26 / EMA 50
    fields += ["(EMA($close, 26)/EMA($close, 50) - 1)"]
    names += ["EMA_26(close)/EMA_50(close)"]
    # EMA 50 / EMA 200
    fields += ["(EMA($close, 50)/EMA($close, 200) - 1)"]
    names += ["EMA_50(close)/EMA_200(close)"]

    #######
    # SMA #
    #######
    windows = [5, 10, 30, 50, 100, 200]

    # Price vs SMA
    fields += ["$close/Mean($close, %d)" % d for d in windows]
    names += ["close/Mean_%d(close)" % d for d in windows]
    # SMA variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_Mean_%d(close)" % (d) for d in windows]

    # SMA 10 / SMA 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]
    # SMA 10 / SMA 30
    fields += ["(Mean($close, 10)/Mean($close, 30) - 1)"]
    names += ["Mean_10(close)/Mean_30(close)"]
    # SMA 20 / SMA 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]
    # SMA 50 / SMA 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    ################
    # # # OPEN # # #
    ################

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # EMA HIGH 5 / EMA CLOSE 5
    fields += ["(EMA($high, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(high)/EMA_5(close)"]

    # EMA LOW 5 / EMA CLOSE 5
    fields += ["(EMA($low, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(low)/EMA_5(close)"]

    # EMA OPEN 5 / EMA CLOSE(1) 5
    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["EMA_5(open)/EMA_5(close(1))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ ROLLING FEATURES (Statistical Significance) ------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    windows = [5, 10, 20, 50, 100, 200]

    # STANDARD DEVIATION
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # BETA
    fields += ["Slope($close, %d)/$close" % d for d in windows]
    names += ["BETA_%d(close)/close" % d for d in windows]
    # RESIDUALS
    fields += ["Resi($close, %d)/$close" % d for d in windows]
    names += ["RESI_%d(close)/close" % d for d in windows]

    # QUANTILES
    fields += ["Quantile($close, %d, 0.8)/$close" % d for d in windows]
    names += ["QTLU_%d(close)/close" % d for d in windows]
    fields += ["Quantile($close, %d, 0.2)/$close" % d for d in windows]
    names += ["QTLD_%d(close)/close" % d for d in windows]

    # RANK
    fields += ["Rank($close, %d)" % d for d in windows]
    names += ["RANK_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################
    windows = [20, 50]
    fields += ["Std($open, %d)/$open" % d for d in windows]
    names += ["STD_%d(open)/open" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [50]
    fields += ["Corr($close, $open, %d)" % d for d in windows]
    names += ["CORR_%d(close/open)" % d for d in windows]

    ################################################
    # # # RSQR -> Explained variance of target # # #
    ################################################
    # windows = []
    # fields += ["Rsquare($close, %d)" % d for d in windows]
    # names += ["RSQR_%d(close)" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ----------------------------- ROLLING FEATURES (Miscellaneous) ------------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    windows = [5, 10, 20, 50, 100, 200]

    fields += ["Mean($close>Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTP_%d(close)" % d for d in windows]

    fields += ["Mean($close<Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTN_%d(close)" % d for d in windows]

    fields += ["Mean($close>Ref($close, 1), %d)-Mean($close<Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["CNTD_%d(close)" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Sum(Greater($close-Ref($close, 1), 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
        for d in windows
    ]
    names += ["SUMP_%d(close)" % d for d in windows]

    # fields += [
    #     "Sum(Greater(Ref($close, 1)-$close, 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
    #     for d in windows
    # ]
    # names += ["SUMN_%d(close)" % d for d in windows]

    # fields += [
    #     "(Sum(Greater($close-Ref($close, 1), 0), %d)-Sum(Greater(Ref($close, 1)-$close, 0), %d))"
    #     "/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d, d)
    #     for d in windows
    # ]
    # names += ["SUMD_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################

    # endregion

    ###############################################################################################################
    # region --------------------------------- MAX & MIN BASED FEATURES ---------------------------------- ########
    ###############################################################################################################

    # Note to self: Should do something to get a more precise look at Resistances and Supports

    windows = [5, 10, 20, 50, 100, 200]
    fields += ["Max($high, %d)/$close" % d for d in windows]
    names += ["MAX%d" % d for d in windows]

    fields += ["Min($low, %d)/$close" % d for d in windows]
    names += ["MIN%d" % d for d in windows]

    fields += ["Max($high, %d)/Min($low, %d)" % (d, d) for d in windows]
    names += ["MAX/MIN%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += ["(Max($high, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MAXvsMEAN/CLOSE%d" % d for d in windows]

    fields += ["(Min($low, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MINvsMEAN/CLOSE%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += ["IdxMax($high, %d)/%d" % (d, d) for d in windows]
    names += ["IMAX%d" % d for d in windows]

    fields += ["IdxMin($low, %d)/%d" % (d, d) for d in windows]
    names += ["IMIN%d" % d for d in windows]

    fields += ["(IdxMax($high, %d)-IdxMin($low, %d))/%d" % (d, d, d) for d in windows]
    names += ["IMAX/IMIN%d" % d for d in windows]

    #########################################
    # # # SUPPORT AND RESISTANCE LEVELS # # #
    #########################################
    support = """
        If(
            And(
                And(
                    $low < Ref($low, 1),
                    And(
                        Ref($low, 1) < Ref($low, 2),
                        Ref($low, 2) < Ref($low, 3)
                    )
                ),
                And(
                    $low < Ref($low, -1),
                    And(
                        Ref($low, -1) < Ref($low, -2),
                        Ref($low, -2) < Ref($low, -3)
                    )
                )
            ),
            $low,
            0
        )
    """
    resistance = """
        If(
            And(
                And(
                    $high > Ref($high, 1),
                    And(
                        Ref($high, 1) > Ref($high, 2),
                        Ref($ligh, 2) > Ref($high, 3)
                    )
                ),
                And(
                    $high > Ref($high, -1),
                    And(
                        Ref($high, -1) > Ref($high, -2),
                        Ref($high, -2) > Ref($high, -3)
                    )
                )
            ),
            $high,
            0
        )
    """

    # endregion

    ###############################################################################################################
    # region ---------------------------------------- INDICATORS ----------------------------------------- ########
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [MACD()]
    names += ["MACD"]

    ##########################
    # # # Ichimoku Cloud # # #
    ##########################
    fields += [
                Ichimoku_Cloud__tenkan_sen() + " / " + Ichimoku_Cloud__kijun_sen(),
                Ichimoku_Cloud__tenkan_sen() + " / $close",
                Ichimoku_Cloud__kijun_sen() + " / $close",

                Ichimoku_Cloud__senkou_span_A() + " / $close",
                Ichimoku_Cloud__senkou_span_B() + " / $close",

                Ichimoku_Cloud__chikou_span() + " / $close"
            ]
    names += [
            "tenkan_sen / kijun_sen",
            "tenkan_sen / close",
            "kijun_sen / close",

            "senkou_span_A / close",
            "senkou_span_B / close",

            "chikou_span / close"
            ]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [Bollinger_Band(r=20)]
    names += ["Bollinger Band"]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 7
    fields += [
        Stochastic_Oscillator(r=7),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=7), Stochastic_Oscillator(r=7))
    ]
    names += [
        "fast_Stochastic_Oscillator(7)",
        "fast_Stochastic_Oscillator(7)-slow_Stochastic_Oscillator(7)"
    ]
    # SO 14
    fields += [
        Stochastic_Oscillator(r=14),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=14), Stochastic_Oscillator(r=14))
    ]
    names += [
        "fast_Stochastic_Oscillator(14)",
        "fast_Stochastic_Oscillator(14)-slow_Stochastic_Oscillator(14)"
    ]
    # SO 21
    fields += [
        Stochastic_Oscillator(r=21),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=21), Stochastic_Oscillator(r=21))
    ]
    names += [
        "fast_Stochastic_Oscillator(21)",
        "fast_Stochastic_Oscillator(21)-slow_Stochastic_Oscillator(21)"
    ]

    #########################################
    # # # Relative Strenght Index (RSI) # # #
    #########################################
    fields += [RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        Aroon_Up(r=14),
        Aroon_Down(r=14),
        Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        Aroon_Up(r=25),
        Aroon_Down(r=25),
        Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    ##################################
    # # # Comodity Channel (CCI) # # #
    ##################################

    # CCI 14
    fields += [CCI(r=14)]
    names += ["CCI_14"]
    # CCI 20
    fields += [CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    fields += [Positive_DI()]
    names += ["Positive_DI"]

    fields += [Negative_DI()]
    names += ["Negative_DI"]

    fields += ["(%s - %s)" % (Positive_DI(), Negative_DI())]
    names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [ADX(r=14)]
    names += ["ADX"]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ATR() + " / $close"]
    names += ["ATR / close"]

    fields += [ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        Bulls_Power(),
        Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    # OBV
    fields += [OBV() + " / " + OBV(d=1)]
    names += ["OBV / OBV(1)"]

    # Accumulation/Distribution Line
    fields += [AD_Line() + " / " + AD_Line(d=1)]
    names += ["AD_Line / AD_Line"]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- VOLUME BASED FEATURES ------------------------------------ ########
    ###############################################################################################################

    ############################
    # # # VOLUME VARIATION # # #
    ############################
    fields += ["If(Ref($volume, 1) == 0, 0, $volume/(Ref($volume, 1)))"]
    names += ["VOLUME/VOLUME(1)"]

    ######################
    # # # MEAN BASED # # #
    ######################
    windows = [5, 10, 20, 50, 100, 200]
    fields += ["If($volume == 0, 0, $volume/Mean($volume, %d))" % d for d in windows]
    names += ["VMA%d" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [5, 10, 20, 50, 100, 200]
    fields += ["Std($volume, %d)/($volume+1e-12)" % d for d in windows]
    names += ["VSTD%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += ["Corr($close, Log($volume+1), %d)" % d for d in windows]
    names += ["CORRV%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, %d)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["WVMA%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        """
        If(Or(Or($close == 0, $volume == 0), Or(Ref($close,1) == 0, Ref($volume,1) == 0)),
        0, Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), %d))
        """
        % d for d in windows
    ]
    names += ["CORDV%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100, 200]
    fields += [
        "Sum(Greater($volume-Ref($volume, 1), 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["VSUMP%d" % d for d in windows]

    # fields += [
    #     "Sum(Greater(Ref($volume, 1)-$volume, 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
    #     % (d, d)
    #     for d in windows
    # ]
    # names += ["VSUMN%d" % d for d in windows]

    # fields += [
    #     "(Sum(Greater($volume-Ref($volume, 1), 0), %d)-Sum(Greater(Ref($volume, 1)-$volume, 0), %d))"
    #     "/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)" % (d, d, d)
    #     for d in windows
    # ]
    # names += ["VSUMD%d" % d for d in windows]

    # endregion

    # ------------------------------------------------------------------------------------------------------------------

    return fields, names


###############################################################################################################
###############################################################################################################
###############################################################################################################
###############################################################################################################


def dataset_features(deep_overview=True):
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- BASIC FEATURES -------------------------------------- ########
    ###############################################################################################################

    #######################
    # # # CURRENT DAY # # #
    #######################
    for d in range(0, 3):
        if d == 0:
            fields += [
            "$high/$close",
            "$low/$close",
            "$open/$close"
            ]
            names += [
                    "HIGH/CLOSE",
                    "LOW/CLOSE",
                    "OPEN/CLOSE",
                    ]
        else:
            fields += [
                    "Ref($high, %d)/Ref($close, %d)" % (d, d),
                    "Ref($low, %d)/Ref($close, %d)" % (d, d),
                    "Ref($open, %d)/Ref($close, %d)" % (d, d),
                    ]
            names += [
                    "HIGH(%d)/CLOSE(%d)" % (d, d),
                    "LOW(%d)/CLOSE(%d)" % (d, d),
                    "OPEN(%d)/CLOSE(%d)" % (d, d)
                    ]

    for d in range(0, 3):  # Hardcoded kbar features
        if d == 0:
            fields += [
                    "($high-$low)/$close",
                    "($close-$open)/($high-$low+1e-12)",
                    "($high-Greater($open, $close))/$close",
                    "($high-Greater($open, $close))/($high-$low+1e-12)",
                    "(Less($open, $close)-$low)/$close",
                    "(Less($open, $close)-$low)/($high-$low+1e-12)",
                    "(2*$close-$high-$low)/$close",
                    "(2*$close-$high-$low)/($high-$low+1e-12)",
                    ]
            names += [
                    "KLEN",
                    "KMID2",
                    "KUP",
                    "KUP2",
                    "KLOW",
                    "KLOW2",
                    "KSFT",
                    "KSFT2",
                    ]
        else:
            fields += [
                    "(Ref($high, %d)-Ref($low, %d))/Ref($close, %d)" % (d, d, d),
                    "(Ref($close, %d)-Ref($open, %d))/(Ref($high, %d)-Ref($low, %d)+1e-12)" % (d, d, d, d),
                    "(Ref($high, %d)-Greater(Ref($open, %d), Ref($close, %d)))/Ref($close, %d)" % (d, d, d, d),
                    "(Ref($high, %d)-Greater(Ref($open, %d), Ref($close, %d)))/(Ref($high, %d)-Ref($low, %d)+1e-12)" % (d, d, d, d, d),
                    "(Less(Ref($open, %d), Ref($close, %d))-Ref($low, %d))/Ref($close, %d)" % (d, d, d, d),
                    "(Less(Ref($open, %d), Ref($close, %d))-Ref($low, %d))/(Ref($high, %d)-Ref($low, %d)+1e-12)" % (d, d, d, d, d),
                    "(2*Ref($close, %d)-Ref($high, %d)-Ref($low, %d))/Ref($close, %d)" % (d, d, d, d),
                    "(2*Ref($close, %d)-Ref($high, %d)-Ref($low, %d))/(Ref($high, %d)-Ref($low, %d)+1e-12)" % (d, d, d, d, d),
                    ]
            names += [
                    "KLEN(%d)" % (d),
                    "KMID2(%d)" % (d),
                    "KUP(%d)" % (d),
                    "KUP2(%d)" % (d),
                    "KLOW(%d)" % (d),
                    "KLOW2(%d)" % (d),
                    "KSFT(%d)" % (d),
                    "KSFT2(%d)" % (d),
                    ]

    #######################################
    # # # CURRENT DAY vs PREVIOUS DAY # # #
    #######################################
    for d in range(0, 3):
        if d == 0:
            fields += [
                    "Ref($close, 1)/$close",

                    "Ref($open, 1)/$open",

                    "Ref($close, 1)/$open",
                    ]
            names += [
                    "CLOSE(1)/CLOSE"

                    "OPEN(1)/OPEN",

                    "CLOSE(1)/OPEN",
                    ]
        else:
            fields += [
                    "Ref($close, %d)/Ref($close, %d)" % (d+1, d),

                    "Ref($open, %d)/Ref($open, %d)" % (d+1, d),

                    "Ref($close, %d)/Ref($open, %d)" % (d+1, d),
                    ]
            names += [
                    "CLOSE(%d)/CLOSE(%d)" % (d+1, d),

                    "OPEN(%d)/OPEN(%d)" % (d+1, d),

                    "CLOSE(%d)/OPEN(%d)" % (d+1, d),
                    ]

    # endregion

    ###############################################################################################################
    # region ------------------------------- ROLLING FEATURES (Mean based) ------------------------------- ########
    ###############################################################################################################


    def mean_vs_mean_features(
        expr1="EMA", var1="close", r1=12,
        expr2="EMA", var2="close", r2=26,
        n_diff_periods=1,
        mean_diff_periods=[3, 5, 8]
    ):
        # Feature components
        def Above_diff(d=0):
            if d == 0:
                Above_diff = """If(({expr1}(${var1}, {r1})/{expr2}(${var2}, {r2}) - 1) > 0,
                    ({expr1}(${var1}, {r1})/{expr2}(${var2}, {r2}) - 1),
                    0)""".format(expr1=expr1, var1=var1, r1=r1, expr2=expr2, var2=var2, r2=r2)
            else:
                Above_diff = """If(({expr1}(Ref(${var1},{d}), {r1})/{expr2}(Ref(${var2},{d}), {r2}) - 1) > 0,
                    ({expr1}(Ref(${var1},{d}), {r1})/{expr2}(Ref(${var2},{d}), {r2}) - 1),
                    0)""".format(expr1=expr1, var1=var1, r1=r1, expr2=expr2, var2=var2, r2=r2, d=d)
            return Above_diff


        def Below_diff(d=0):
            if d == 0:
                Below_diff = """If(({expr1}(${var1}, {r1})/{expr2}(${var2}, {r2}) - 1) < 0,
                    ({expr1}(${var1}, {r1})/{expr2}(${var2}, {r2}) - 1),
                    0)""".format(expr1=expr1, var1=var1, r1=r1, expr2=expr2, var2=var2, r2=r2)
            else:
                Below_diff = """If(({expr1}(Ref(${var1},{d}), {r1})/{expr2}(Ref(${var2},{d}), {r2}) - 1) < 0,
                    ({expr1}(Ref(${var1},{d}), {r1})/{expr2}(Ref(${var2},{d}), {r2}) - 1),
                    0)""".format(expr1=expr1, var1=var1, r1=r1, expr2=expr2, var2=var2, r2=r2, d=d)
            return Below_diff
        

        # Names components
        Above_diff_nm = "Above_diff({expr1}_{r1}({var1})/{expr2}_{r2}({var2}))".format(
            expr1=expr1, var1=var1, r1=r1, expr2=expr2, var2=var2, r2=r2)

        Below_diff_nm = "Below_diff({expr1}_{r1}({var1})/{expr2}_{r2}({var2}))".format(
            expr1=expr1, var1=var1, r1=r1, expr2=expr2, var2=var2, r2=r2)

        ###############################################################################################

        new_fields = []
        new_names = []

        # Difference between means
        new_fields += [
            Above_diff(0),
            Below_diff(0)
        ]
        new_names += [
            Above_diff_nm,
            Below_diff_nm
        ]

        # Difference between means increase/decrease from previous period
        for n in range(0, n_diff_periods):
            new_fields += [
                "%s - %s" % (Above_diff(n), Above_diff(n+1)),
                "%s - %s" % (Below_diff(n), Below_diff(n+1))
            ]
            new_names += [
                "DiffChange_%d(%s)" % (n, Above_diff_nm),
                "DiffChange_%d(%s)" % (n, Below_diff_nm)
            ]
        # Mean Difference increase/decrease from previous period
        for n in mean_diff_periods:
            new_fields += [
                "Mean(%s - %s, %d)" % (Above_diff(0), Above_diff(1), n),
                "Mean(%s - %s, %d)" % (Below_diff(0), Below_diff(1), n),
            ]
            new_names += [
                "Mean_%d(DiffChange(%s))" % (n, Above_diff_nm),
                "Mean_%d(DiffChange(%s))" % (n, Below_diff_nm)
            ]

        # Difference increase/decrease from previous period vs itself in previous period
        for n in range(0, n_diff_periods):
            new_fields += [
                """If(Or(
                         And({expr0}-{expr1} > 0, {expr1}-{expr2} > 0),
                         And({expr0}-{expr1} < 0, {expr1}-{expr2} < 0)
                         ),
                      ({expr0}-{expr1}) - ({expr1}-{expr1}),
                      0)""".format(expr0=Above_diff(n), expr1=Above_diff(n+1), expr2=Above_diff(n+2)),
                """If(Or(
                         And({expr0}-{expr1} > 0, {expr1}-{expr2} > 0),
                         And({expr0}-{expr1} < 0, {expr1}-{expr2} < 0)
                         ),
                      ({expr0}-{expr1}) - ({expr1}-{expr1}),
                      0)""".format(expr0=Below_diff(n), expr1=Below_diff(n+1), expr2=Below_diff(n+2)),
            ]
            new_names += [
                "DiffChangeAcceleration_%d(%s)" % (n, Above_diff_nm),
                "DiffChangeAcceleration_%d(%s)" % (n, Below_diff_nm)
            ]
        # Mean Difference increase/decrease from previous period vs itself in previous period
        for n in mean_diff_periods:
            new_fields += [
                """Mean(If(Or(
                              And({expr0}-{expr1} > 0, {expr1}-{expr2} > 0),
                              And({expr0}-{expr1} < 0, {expr1}-{expr2} < 0)
                              ),
                           ({expr0}-{expr1}) - ({expr1}-{expr1}),
                           0), {n})""".format(expr0=Above_diff(n), expr1=Above_diff(n+1), expr2=Above_diff(n+2), n=n),
                """Mean(If(Or(
                              And({expr0}-{expr1} > 0, {expr1}-{expr2} > 0),
                              And({expr0}-{expr1} < 0, {expr1}-{expr2} < 0)
                              ),
                           ({expr0}-{expr1}) - ({expr1}-{expr1}),
                           0), {n})""".format(expr0=Below_diff(n), expr1=Below_diff(n+1), expr2=Below_diff(n+2), n=n)
            ]
            new_names += [
                "Mean_%d(DiffChangeAcceleration(%s))" % (n, Above_diff_nm),
                "Mean_%d(DiffChangeAcceleration(%s))" % (n, Below_diff_nm)
            ]

        return new_fields, new_names
        
    
    #################
    # # # CLOSE # # #
    #################

    #######
    # EMA #
    #######
    windows = [5, 8, 12, 26, 50, 100, 200]
    
    # Price vs EMA
    fields += ["$close/EMA($close, %d)" % d for d in windows]
    names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Change
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_EMA_%d(close))" % (d) for d in windows]
    # Mean(EMA Change)
    fields += ["Mean(EMA($close, %d)/EMA(Ref($close, 1), %d), 5)" % (d, d) for d in windows]
    names += ["Mean_5(Change_EMA_%d(close)))" % (d) for d in windows]

    if not deep_overview:
        # EMA 5 / EMA 8
        fields += [
            "(EMA($close, 5)/EMA($close, 8) - 1)",
            "(EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1)",
            "Mean((EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1), 5)"
        ]
        names += [
            "EMA_5(close)/EMA_8(close)",
            "Change(EMA_5(close)/EMA_8(close))",
            "Mean_5(Change(EMA_5(close)/EMA_8(close)))"
        ]
        # EMA 12 / EMA 26
        fields += [
            "(EMA($close, 12)/EMA($close, 26) - 1)",
            "(EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1)",
            "Mean((EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1), 5)"
        ]
        names += [
            "EMA_12(close)/EMA_26(close)",
            "Change(EMA_12(close)/EMA_26(close))",
            "Mean_5(Change(EMA_12(close)/EMA_26(close)))"
        ]
        # EMA 26 / EMA 50
        fields += [
            "(EMA($close, 26)/EMA($close, 50) - 1)",
            "(EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1)",
            "Mean((EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1), 5)"
        ]
        names += [
            "EMA_26(close)/EMA_50(close)",
            "Change(EMA_26(close)/EMA_50(close))",
            "Mean_5(Change(EMA_26(close)/EMA_50(close)))"
        ]
        # EMA 50 / EMA 200
        fields += [
            "(EMA($close, 50)/EMA($close, 200) - 1)",
            "(EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1)",
            "Mean((EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1), 5)"
        ]
        names += [
            "EMA_50(close)/EMA_200(close)",
            "Change(EMA_50(close)/EMA_200(close))",
            "Mean_5(Change(EMA_50(close)/EMA_200(close)))"
        ]
    else:
        # EMA 5 / EMA 8
        new_fields, new_names = mean_vs_mean_features(
            expr1="EMA", var1="close", r1=5,
            expr2="EMA", var2="close", r2=8
        )
        fields += new_fields
        names += new_names
        # EMA 12 / EMA 26
        new_fields, new_names = mean_vs_mean_features(
            expr1="EMA", var1="close", r1=12,
            expr2="EMA", var2="close", r2=26
        )
        fields += new_fields
        names += new_names
        # EMA 26 / EMA 50
        new_fields, new_names = mean_vs_mean_features(
            expr1="EMA", var1="close", r1=26,
            expr2="EMA", var2="close", r2=50
        )
        fields += new_fields
        names += new_names
        # EMA 50 / EMA 200
        new_fields, new_names = mean_vs_mean_features(
            expr1="EMA", var1="close", r1=50,
            expr2="EMA", var2="close", r2=200
        )
        fields += new_fields
        names += new_names

    #######
    # SMA #
    #######
    windows = [5, 10, 20, 30, 50, 100, 200]

    # Price vs SMA
    fields += ["$close/Mean($close, %d)" % d for d in windows]
    names += ["close/Mean_%d(close)" % d for d in windows]
    # SMA variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["Change_Mean_%d(close)" % (d) for d in windows]
    # Mean(SMA variation)
    fields += ["Mean(Mean($close, %d)/Mean(Ref($close, 1), %d), 5)" % (d, d) for d in windows]
    names += ["Mean_5(Change_Mean_%d(close))" % (d) for d in windows]

    if deep_overview:
        # SMA 10 / SMA 20
        fields += [
            "(Mean($close, 10)/Mean($close, 20) - 1)",
            "(Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1)",

        ]
        names += [
            "Mean_10(close)/Mean_20(close)",
            "Change(Mean_10(close)/Mean_20(close))"
        ]
        # SMA 10 / SMA 30
        fields += [
            "(Mean($close, 10)/Mean($close, 30) - 1)",
            "(Mean($close, 10)/Mean($close, 30) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 30) - 1)"
        ]
        names += [
            "Mean_10(close)/Mean_30(close)",
            "Change(Mean_10(close)/Mean_30(close))"
        ]
        # SMA 20 / SMA 50
        fields += [
            "(Mean($close, 20)/Mean($close, 50) - 1)",
            "(Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1)"
        ]
        names += [
            "Mean_20(close)/Mean_50(close)",
            "Change(Mean_20(close)/Mean_50(close))"
        ]
        # SMA 50 / SMA 200
        fields += [
            "(Mean($close, 50)/Mean($close, 200) - 1)",
            "(Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1)"
        ]
        names += [
            "Mean_50(close)/Mean_200(close)",
            "Change(Mean_50(close)/Mean_200(close))"
        ]
    else:
        # SMA 10 / SMA 20
        new_fields, new_names = mean_vs_mean_features(
            expr1="Mean", var1="close", r1=10,
            expr2="Mean", var2="close", r2=20
        )
        fields += new_fields
        names += new_names
        # SMA 10 / SMA 30
        new_fields, new_names = mean_vs_mean_features(
            expr1="Mean", var1="close", r1=10,
            expr2="Mean", var2="close", r2=30
        )
        fields += new_fields
        names += new_names
        # SMA 20 / SMA 50
        new_fields, new_names = mean_vs_mean_features(
            expr1="Mean", var1="close", r1=20,
            expr2="Mean", var2="close", r2=50
        )
        fields += new_fields
        names += new_names
        # SMA 50 / SMA 200
        new_fields, new_names = mean_vs_mean_features(
            expr1="Mean", var1="close", r1=50,
            expr2="Mean", var2="close", r2=200
        )
        fields += new_fields
        names += new_names

    ################
    # # # OPEN # # #
    ################

    #########################
    # # # MISCELLANEOUS # # #
    #########################

    # EMA HIGH 5 / EMA CLOSE 5
    fields += [
        "(EMA($high, 5)/EMA($close, 5) - 1)",
        "(EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1)",
        "Mean((EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1), 5)"            
    ]
    names += [
        "EMA_5(high)/EMA_5(close)",
        "Change(EMA_5(high)/EMA_5(close))",
        "Mean_5(Change(EMA_5(high)/EMA_5(close)))"
    ]
    # EMA LOW 5 / EMA CLOSE 5
    fields += [
        "(EMA($low, 5)/EMA($close, 5) - 1)",
        "(EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1)",
        "Mean((EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1), 5)"
    ]
    names += [
        "EMA_5(low)/EMA_5(close)",
        "Change(EMA_5(low)/EMA_5(close))",
        "Mean_5(Change(EMA_5(low)/EMA_5(close)))"
    ]

    # endregion

    ###############################################################################################################
    # region ------------------------ ROLLING FEATURES (Statistical Significance) ------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    windows = [5, 10, 20, 50, 100, 200]

    # STANDARD DEVIATION
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]
    # RESIDUALS
    fields += ["Resi($close, %d)/$close" % d for d in windows]
    names += ["RESI_%d(close)/close" % d for d in windows]
    # QUANTILES
    fields += ["Quantile($close, %d, 0.8)/$close" % d for d in windows]
    names += ["QTLU_%d(close)/close" % d for d in windows]
    fields += ["Quantile($close, %d, 0.2)/$close" % d for d in windows]
    names += ["QTLD_%d(close)/close" % d for d in windows]
    # RSQR
    fields += ["Rsquare($close, %d)/$close" % d for d in windows]
    names += ["RSQR_%d(close)/close" % d for d in windows]
    # BETA
    fields += ["Slope($close, %d)" % d for d in windows]
    names += ["BETA_%d(close)" % d for d in windows]
    # RANK
    fields += ["Rank($close, %d)" % d for d in windows]
    names += ["RANK_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################

    #########################
    # # # MISCELLANEOUS # # #
    #########################
        
    # endregion

    ###############################################################################################################
    # region ----------------------------- ROLLING FEATURES (Miscellaneous) ------------------------------ ########
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    windows = [5, 10, 20, 50, 100, 200]

    fields += ["Mean($close>Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTP_%d(close)" % d for d in windows]

    fields += ["Mean($close<Ref($close, 1), %d)" % d for d in windows]
    names += ["CNTN_%d(close)" % d for d in windows]

    fields += ["Mean($close>Ref($close, 1), %d)-Mean($close<Ref($close, 1), %d)" % (d, d) for d in windows]
    names += ["CNTD_%d(close)" % d for d in windows]

    fields += [
        "Sum(Greater($close-Ref($close, 1), 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
        for d in windows
    ]
    names += ["SUMP_%d(close)" % d for d in windows]

    fields += [
        "Sum(Greater(Ref($close, 1)-$close, 0), %d)/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d)
        for d in windows
    ]
    names += ["SUMN_%d(close)" % d for d in windows]

    fields += [
        "(Sum(Greater($close-Ref($close, 1), 0), %d)-Sum(Greater(Ref($close, 1)-$close, 0), %d))"
        "/(Sum(Abs($close-Ref($close, 1)), %d)+1e-12)" % (d, d, d)
        for d in windows
    ]
    names += ["SUMD_%d(close)" % d for d in windows]

    ################
    # # # OPEN # # #
    ################

    # endregion

    ###############################################################################################################
    # region --------------------------------- MAX & MIN BASED FEATURES ---------------------------------- ########
    ###############################################################################################################

    # Note to self: Should do something to get a more precise look at Resistances and Supports

    windows = [5, 10, 20, 50, 100, 200]

    fields += ["Max($high, %d)/$close" % d for d in windows]
    names += ["MAX%d" % d for d in windows]

    fields += ["Min($low, %d)/$close" % d for d in windows]
    names += ["MIN%d" % d for d in windows]

    fields += ["Max($high, %d)/Min($low, %d)" % (d, d) for d in windows]
    names += ["MAX/MIN%d" % d for d in windows]


    fields += ["(Max($high, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MAXvsMEAN/CLOSE%d" % d for d in windows]

    fields += ["(Min($low, %d)-Mean($close, %d))/$close" % (d, d) for d in windows]
    names += ["MINvsMEAN/CLOSE%d" % d for d in windows]

 
    fields += ["IdxMax($high, %d)/%d" % (d, d) for d in windows]
    names += ["IMAX%d" % d for d in windows]

    fields += ["IdxMin($low, %d)/%d" % (d, d) for d in windows]
    names += ["IMIN%d" % d for d in windows]

    fields += ["(IdxMax($high, %d)-IdxMin($low, %d))/%d" % (d, d, d) for d in windows]
    names += ["IMAX/IMIN%d" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------------- INDICATORS ----------------------------------------- ########
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [
        MACD(),
        "%s - %s" % (MACD(), MACD(1)),
        "Mean(%s - %s, 5)" % (MACD(), MACD(1))
    ]
    names += [
        "MACD",
        "MACD-MACD(1)",
        "Mean_5(MACD-MACD(1))",
    ]

    ##########################
    # # # Ichimoku Cloud # # #
    ##########################
    fields += [
                Ichimoku_Cloud__tenkan_sen() + " / " + Ichimoku_Cloud__kijun_sen(),
                Ichimoku_Cloud__tenkan_sen() + " / $close",
                Ichimoku_Cloud__kijun_sen() + " / $close",

                Ichimoku_Cloud__senkou_span_A() + " / $close",
                Ichimoku_Cloud__senkou_span_B() + " / $close",

                Ichimoku_Cloud__chikou_span() + " / $close"
            ]
    names += [
            "tenkan_sen / kijun_sen",
            "tenkan_sen / close",
            "kijun_sen / close",

            "senkou_span_A / close",
            "senkou_span_B / close",

            "chikou_span / close"
            ]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 7
    fields += [
        Stochastic_Oscillator(r=7),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=7), Stochastic_Oscillator(r=7))
    ]
    names += [
        "fast_Stochastic_Oscillator(7)",
        "fast_Stochastic_Oscillator(7)-slow_Stochastic_Oscillator(7)"
    ]
    # SO 14
    fields += [
        Stochastic_Oscillator(r=14),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=14), Stochastic_Oscillator(r=14))
    ]
    names += [
        "fast_Stochastic_Oscillator(14)",
        "fast_Stochastic_Oscillator(14)-slow_Stochastic_Oscillator(14)"
    ]
    # SO 21
    fields += [
        Stochastic_Oscillator(r=21),
        "%s - Mean(%s, 3)" % (Stochastic_Oscillator(r=21), Stochastic_Oscillator(r=21))
    ]
    names += [
        "fast_Stochastic_Oscillator(21)",
        "fast_Stochastic_Oscillator(21)-slow_Stochastic_Oscillator(21)"
    ]

    #########################################
    # # # Relative Strenght Index (RSI) # # #
    #########################################
    fields += [RSI()]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        Aroon_Up(r=14),
        Aroon_Down(r=14),
        Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        Aroon_Up(r=25),
        Aroon_Down(r=25),
        Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    ##################################
    # # # Comodity Channel (CCI) # # #
    ##################################

    # CCI 14
    fields += [CCI(r=14)]
    names += ["CCI_14"]
    # CCI 20
    fields += [CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    fields += [Positive_DI()]
    names += ["Positive_DI"]

    fields += [Negative_DI()]
    names += ["Negative_DI"]

    fields += ["(%s - %s)" % (Positive_DI(), Negative_DI())]
    names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [ADX()]
    names += ["ADX"]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [CHOP()]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ATR() + " / $close"]
    names += ["ATR / close"]

    fields += [ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        Bulls_Power(),
        Bears_Power(),
        Bulls_Power() + " / " + Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power",
        "Bulls_Power / Bears_Power"
    ]
    
    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- VOLUME BASED FEATURES ------------------------------------ ########
    ###############################################################################################################

    ############################
    # # # VOLUME VARIATION # # #
    ############################
    for d in range(0, 5):
        if d == 0:
            fields += ["If(Ref($volume, 1) == 0, 0, $volume/(Ref($volume, 1)))"]
            names += ["VOLUME/VOLUME(1)"]
        else:
            fields += ["If(Ref($volume, %d) == 0, 0, Ref($volume, %d)/Ref($volume, %d))" % (d+1, d, d+1)]
            names += ["VOLUME(%d)/VOLUME(%d)" % (d, d+1)]

    windows = [5, 10, 20, 50, 100, 200]
    fields += ["Mean(If(Ref($volume, 1) == 0, 0, $volume/(Ref($volume, 1))), %d)" % d for d in windows]
    names += ["Mean_%d(VOLUME/VOLUME(1))" % d for d in windows]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    windows = [5, 10, 20, 50, 100, 200]

    fields += ["Mean($volume, %d)/($volume+1e-12)" % d for d in windows]
    names += ["VMA%d" % d for d in windows]

    fields += ["Std($volume, %d)/($volume+1e-12)" % d for d in windows]
    names += ["VSTD%d" % d for d in windows]

    fields += ["Corr($close, Log($volume+1), %d)" % d for d in windows]
    names += ["CORR%d" % d for d in windows]

    fields += [
        """
        If(Or(Or($close == 0, $volume == 0), Or(Ref($close,1) == 0, Ref($volume,1) == 0)), 
        0, Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), %d))
        """
        % d for d in windows
    ]
    names += ["CORD%d" % d for d in windows]

    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, %d)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["WVMA%d" % d for d in windows]

    fields += [
        "Sum(Greater($volume-Ref($volume, 1), 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["VSUMP%d" % d for d in windows]

    fields += [
        "Sum(Greater(Ref($volume, 1)-$volume, 0), %d)/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["VSUMN%d" % d for d in windows]

    fields += [
        "(Sum(Greater($volume-Ref($volume, 1), 0), %d)-Sum(Greater(Ref($volume, 1)-$volume, 0), %d))"
        "/(Sum(Abs($volume-Ref($volume, 1)), %d)+1e-12)" % (d, d, d)
        for d in windows
    ]
    names += ["VSUMD%d" % d for d in windows]

    # endregion

    # ------------------------------------------------------------------------------------------------------------------

    return fields, names

#  endregion
