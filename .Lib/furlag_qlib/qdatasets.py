from .indicators import CommonIndicators


ci = CommonIndicators()


#######################################################################################################################
#  region ------------------------------------------- FEATURES --------------------------------------------------------

def dataset_features(index_features=False):
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- Basic Features -----------------------------------------------
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
    # region ------------------------------- Rolling Features (Mean based) ----------------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    
    #######
    # EMA #
    #######

    windows = [
        5, 8, 12, 26,
        50, 100, 200
    ]
    # Price vs EMA
    fields += ["$close/EMA($close, %d)" % d for d in windows]
    names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(EMA_%d(close))" % (d) for d in windows]
    # EMA Variation Acceleration
    fields += ["""(
        (EMA($close, %d)/EMA(Ref($close, 1), %d) - 1)
         - (EMA(Ref($close, 1), %d)/EMA(Ref($close, 2), %d) - 1)
    )""" % (d, d, d, d) for d in windows]
    names += ["Change_acceleration(EMA_%d(close))" % (d) for d in windows]


    # EMA 5 / EMA 8
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1)"]
    names += ["EMA_5(close)/EMA_8(close)"]
    
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1)"]
    names += ["Change(EMA_5(close)/EMA_8(close))"]

    fields += ["""(
               ((EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1))
               - ((EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1) - (EMA(Ref($close, 2), 5)/EMA(Ref($close, 2), 8) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(close)/EMA_8(close))"]

    # EMA 12 / EMA 26
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1)"]
    names += ["EMA_12(close)/EMA_26(close)"]
    
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1)"]
    names += ["Change(EMA_12(close)/EMA_26(close))"]

    fields += ["""(
                ((EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1))
                - ((EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1) - (EMA(Ref($close, 2), 12)/EMA(Ref($close, 2), 26) - 1))
            )"""]
    names += ["Change_acceleration(EMA_12(close)/EMA_26(close))"]

    # EMA 26 / EMA 50
    fields += ["(EMA($close, 26)/EMA($close, 50) - 1)"]
    names += ["EMA_26(close)/EMA_50(close)"]

    fields += ["(EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1)"]
    names += ["Change(EMA_26(close)/EMA_50(close))"]

    fields += ["""(
               ((EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1))
               - ((EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1) - (EMA(Ref($close, 2), 26)/EMA(Ref($close, 2), 50) - 1))
            )"""]
    names += ["Change_acceleration(EMA_26(close)/EMA_50(close))"]

    # EMA 50 / EMA 200
    fields += ["(EMA($close, 50)/EMA($close, 200) - 1)"]
    names += ["EMA_50(close)/EMA_200(close)"]

    fields += ["(EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1)"]
    names += ["Change(EMA_50(close)/EMA_200(close))"]

    fields += ["""(
               ((EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1))
               - ((EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1) - (EMA(Ref($close, 2), 50)/EMA(Ref($close, 2), 200) - 1))
            )"""]
    names += ["Change_acceleration(EMA_50(close)/EMA_200(close))"]


    #######
    # SMA #
    #######

    windows = [
        5, 10, 20, 30,
        50, 100, 200
    ]
    # Price vs Mean
    # fields += ["$close/Mean($close, %d)" % d for d in windows]
    # names += ["close/Mean_%d(close)" % d for d in windows]
    # Mean Variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(Mean_%d(close))" % (d) for d in windows]
    # Mean Variation Acceleration
    fields += ["""(
        (Mean($close, %d)/Mean(Ref($close, 1), %d) - 1)
         - (Mean(Ref($close, 1), %d)/Mean(Ref($close, 2), %d) - 1)
    )""" % (d, d, d, d) for d in windows]
    names += ["Change_acceleration(Mean_%d(close))" % (d) for d in windows]


    # Mean 5 / Mean 10
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1)"]
    names += ["Mean_5(close)/Mean_10(close)"]
    
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1) - (Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1)"]
    names += ["Change(Mean_5(close)/Mean_10(close))"]

    fields += ["""(
               ((Mean($close, 5)/Mean($close, 10) - 1) - (Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1))
               - ((Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1) - (Mean(Ref($close, 2), 5)/Mean(Ref($close, 2), 10) - 1))
            )"""]
    names += ["Change_acceleration(Mean_5(close)/Mean_10(close))"]

    # Mean 10 / Mean 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]
    
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1)"]
    names += ["Change(Mean_10(close)/Mean_20(close))"]

    fields += ["""(
                ((Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1))
                - ((Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1) - (Mean(Ref($close, 2), 10)/Mean(Ref($close, 2), 20) - 1))
            )"""]
    names += ["Change_acceleration(Mean_10(close)/Mean_20(close))"]

    # Mean 20 / Mean 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]

    fields += ["(Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1)"]
    names += ["Change(Mean_20(close)/Mean_50(close))"]

    fields += ["""(
               ((Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1))
               - ((Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1) - (Mean(Ref($close, 2), 20)/Mean(Ref($close, 2), 50) - 1))
            )"""]
    names += ["Change_acceleration(Mean_20(close)/Mean_50(close))"]

    # Mean 50 / Mean 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    fields += ["(Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1)"]
    names += ["Change(Mean_50(close)/Mean_200(close))"]

    fields += ["""(
               ((Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1))
               - ((Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1) - (Mean(Ref($close, 2), 50)/Mean(Ref($close, 2), 200) - 1))
            )"""]
    names += ["Change_acceleration(Mean_50(close)/Mean_200(close))"]


    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # EMA HIGH 5 / EMA CLOSE 5
    fields += ["(EMA($high, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(high)/EMA_5(close)"]

    fields += ["(EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["Change(EMA_5(high)/EMA_5(close))"]

    fields += ["""(
               ((EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1))
               - ((EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($high, 2), 5)/EMA(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(high)/EMA_5(close))"]

    # EMA LOW 5 / EMA CLOSE 5
    fields += ["(EMA($low, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(low)/EMA_5(close)"]

    fields += ["(EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["Change(EMA_5(low)/EMA_5(close))"]

    fields += ["""(
               ((EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1))
               - ((EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($low, 2), 5)/EMA(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(low)/EMA_5(close))"]

    # EMA OPEN 5 / EMA CLOSE(1) 5
    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["EMA_5(open)/EMA_5(close(1))"]

    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1)"]
    names += ["Change(EMA_5(open)/EMA_5(close(1)))"]

    fields += ["""(
               ((EMA($open, 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1))
               - ((EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1) - (EMA(Ref($open, 2), 5)/EMA(Ref($close, 3), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(open)/EMA_5(close(1)))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ Rolling Features (Statistical Significance) ---------------------------------
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
    # region ------------------------------- Rolling Features (Miscellaneous) -------------------------------------
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
    
    # endregion

    ###############################################################################################################
    # region ---------------------------------------- Indicators --------------------------------------------------
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [
        "{}".format(ci.MACD()),
        "{0} - {1}".format(ci.MACD(), ci.MACD(d=1))
    ]
    names += ["MACD", "acceleration_MACD"]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [
        ci.Bollinger_Band(r=20),
        "({0} / {1} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20), ci.Bollinger_Band(d=2, r=20))
    ]
    names += [
        "BollingerBand(20)",
        "change_BollingerBand(20)",
        "change_acceleration_BollingerBand(20)"
    ]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 14
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=14)),
        "{0} / Mean({0}, 3) - 1".format(ci.Stochastic_Oscillator(r=14))
    ]
    names += [
        "Stochastic_Oscillator(14)",
        "Stochastic_Oscillator(14)_signal(3)"
    ]

    # SO 8
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=8)),
        "{0} / Mean({0}, 5) - 1".format(ci.Stochastic_Oscillator(r=8))
    ]
    names += [
        "Stochastic_Oscillator(8)",
        "Stochastic_Oscillator(8)_signal(5)"
    ]
    
    ####################################################
    # # # Relative Strenght Index (RSI) Oscillator # # #
    ####################################################
    fields += [ci.RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        ci.Aroon_Up(r=14),
        ci.Aroon_Down(r=14),
        ci.Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        ci.Aroon_Up(r=25),
        ci.Aroon_Down(r=25),
        ci.Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    #############################################
    # # # Comodity Channel (CCI) Oscillator # # #
    #############################################

    # CCI 14
    fields += [ci.CCI(r=14)]
    names += ["CCI_14"]
    # CCI 21
    fields += [ci.CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [ci.CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    # fields += [ci.Positive_DI()]
    # names += ["Positive_DI"]

    # fields += [ci.Negative_DI()]
    # names += ["Negative_DI"]

    # fields += ["(%s - %s)" % (ci.Positive_DI(), ci.Negative_DI())]
    # names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [
        ci.ADX(r=14),
        "({0} / {1} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14), ci.ADX(d=2, r=14))
    ]
    names += [
        "ADX",
        "change_ADX",
        "change_acceleration_ADX"
    ]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [ci.CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ci.ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        ci.Bulls_Power(),
        ci.Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [ci.Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ###############
    # # # OBV # # #
    ###############
    windows = [10, 20]

    # fields += ["{s}/Mean({s}, {d})".format(s=ci.OBV(), d=d) for d in windows]
    # names += ["OBV/Mean%d(OBV)" % (d) for d in windows]

    fields += ["(Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1)".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change(Mean%d(OBV))" % (d) for d in windows]

    fields += ["""(
        (Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1) - (Mean(Ref({s}, 1), {d})/Mean(Ref({s}, 2), {d}) - 1)
    )""".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change_acceleration(Mean%d(OBV))" % (d) for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- Volume based Features ---------------------------------------------
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

    windows = [50, 100, 200]
    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, %d)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["WVMA%d" % d for d in windows]

    windows = [5, 10, 20, 50, 100]
    fields += [
        """
        If(Or(Or($close == 0, $volume == 0), Or(Ref($close,1) == 0, Ref($volume,1) == 0)),
        0, Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), %d))
        """
        % d for d in windows
    ]
    names += ["CORDV%d" % d for d in windows]

    windows = [5]  # 10, 20, 50, 100, 200
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
    # region ---------------------------------- Market Index Features ---------------------------------------------
    ###############################################################################################################

    if index_features:
    
        #######
        # SMA #
        #######
        windows = [
            5, 10, 20, 30,
            50, 100, 200
        ]

        # SMA variation
        fields += ["Mean($close_idx, %d)/Mean(Ref($close_idx, 1), %d)" % (d, d) for d in windows]
        names += ["Change_Mean_%d(close_idx)" % (d) for d in windows]

        # Mean 5 / Mean 10
        fields += ["(Mean($close_idx, 5)/Mean($close_idx, 10) - 1)"]
        names += ["Mean_5(close_idx)/Mean_10(close_idx)"]

        # Mean 10 / Mean 20
        fields += ["(Mean($close_idx, 10)/Mean($close_idx, 20) - 1)"]
        names += ["Mean_10(close_idx)/Mean_20(close_idx)"]

        # Mean 20 / Mean 50
        fields += ["(Mean($close_idx, 20)/Mean($close_idx, 50) - 1)"]
        names += ["Mean_20(close_idx)/Mean_50(close_idx)"]

        # Mean 50 / Mean 200
        fields += ["(Mean($close_idx, 50)/Mean($close_idx, 200) - 1)"]
        names += ["Mean_50(close_idx)/Mean_200(close_idx)"]

    # endregion

    return fields, names


# ---------------------------------------------------------------------------------------------------------------------


def dataset_features_ts(index_features=False):
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- Basic Features -----------------------------------------------
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
    # region ------------------------------- Rolling Features (Mean based) ----------------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    
    #######
    # EMA #
    #######

    windows = [
        5, 8, 12, 26,
        50, 100, 200
    ]
    # Price vs EMA
    fields += ["$close/EMA($close, %d)" % d for d in windows]
    names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(EMA_%d(close))" % (d) for d in windows]
    # EMA Variation Acceleration
    fields += ["""(
        (EMA($close, %d)/EMA(Ref($close, 1), %d) - 1)
         - (EMA(Ref($close, 1), %d)/EMA(Ref($close, 2), %d) - 1)
    )""" % (d, d, d, d) for d in windows]
    names += ["Change_acceleration(EMA_%d(close))" % (d) for d in windows]


    # EMA 5 / EMA 8
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1)"]
    names += ["EMA_5(close)/EMA_8(close)"]
    
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1)"]
    names += ["Change(EMA_5(close)/EMA_8(close))"]

    fields += ["""(
               ((EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1))
               - ((EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1) - (EMA(Ref($close, 2), 5)/EMA(Ref($close, 2), 8) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(close)/EMA_8(close))"]

    # EMA 12 / EMA 26
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1)"]
    names += ["EMA_12(close)/EMA_26(close)"]
    
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1)"]
    names += ["Change(EMA_12(close)/EMA_26(close))"]

    fields += ["""(
                ((EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1))
                - ((EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1) - (EMA(Ref($close, 2), 12)/EMA(Ref($close, 2), 26) - 1))
            )"""]
    names += ["Change_acceleration(EMA_12(close)/EMA_26(close))"]

    # EMA 26 / EMA 50
    fields += ["(EMA($close, 26)/EMA($close, 50) - 1)"]
    names += ["EMA_26(close)/EMA_50(close)"]

    fields += ["(EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1)"]
    names += ["Change(EMA_26(close)/EMA_50(close))"]

    fields += ["""(
               ((EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1))
               - ((EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1) - (EMA(Ref($close, 2), 26)/EMA(Ref($close, 2), 50) - 1))
            )"""]
    names += ["Change_acceleration(EMA_26(close)/EMA_50(close))"]

    # EMA 50 / EMA 200
    fields += ["(EMA($close, 50)/EMA($close, 200) - 1)"]
    names += ["EMA_50(close)/EMA_200(close)"]

    fields += ["(EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1)"]
    names += ["Change(EMA_50(close)/EMA_200(close))"]

    fields += ["""(
               ((EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1))
               - ((EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1) - (EMA(Ref($close, 2), 50)/EMA(Ref($close, 2), 200) - 1))
            )"""]
    names += ["Change_acceleration(EMA_50(close)/EMA_200(close))"]


    #######
    # SMA #
    #######

    windows = [
        5, 10, 20, 30,
        50, 100, 200
    ]
    # Price vs Mean
    fields += ["$close/Mean($close, %d)" % d for d in windows]
    names += ["close/Mean_%d(close)" % d for d in windows]
    # Mean Variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(Mean_%d(close))" % (d) for d in windows]
    # Mean Variation Acceleration
    fields += ["""(
        (Mean($close, %d)/Mean(Ref($close, 1), %d) - 1)
         - (Mean(Ref($close, 1), %d)/Mean(Ref($close, 2), %d) - 1)
    )""" % (d, d, d, d) for d in windows]
    names += ["Change_acceleration(Mean_%d(close))" % (d) for d in windows]


    # Mean 5 / Mean 10
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1)"]
    names += ["Mean_5(close)/Mean_10(close)"]
    
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1) - (Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1)"]
    names += ["Change(Mean_5(close)/Mean_10(close))"]

    fields += ["""(
               ((Mean($close, 5)/Mean($close, 10) - 1) - (Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1))
               - ((Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1) - (Mean(Ref($close, 2), 5)/Mean(Ref($close, 2), 10) - 1))
            )"""]
    names += ["Change_acceleration(Mean_5(close)/Mean_10(close))"]

    # Mean 10 / Mean 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]
    
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1)"]
    names += ["Change(Mean_10(close)/Mean_20(close))"]

    fields += ["""(
                ((Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1))
                - ((Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1) - (Mean(Ref($close, 2), 10)/Mean(Ref($close, 2), 20) - 1))
            )"""]
    names += ["Change_acceleration(Mean_10(close)/Mean_20(close))"]

    # Mean 20 / Mean 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]

    fields += ["(Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1)"]
    names += ["Change(Mean_20(close)/Mean_50(close))"]

    fields += ["""(
               ((Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1))
               - ((Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1) - (Mean(Ref($close, 2), 20)/Mean(Ref($close, 2), 50) - 1))
            )"""]
    names += ["Change_acceleration(Mean_20(close)/Mean_50(close))"]

    # Mean 50 / Mean 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    fields += ["(Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1)"]
    names += ["Change(Mean_50(close)/Mean_200(close))"]

    fields += ["""(
               ((Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1))
               - ((Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1) - (Mean(Ref($close, 2), 50)/Mean(Ref($close, 2), 200) - 1))
            )"""]
    names += ["Change_acceleration(Mean_50(close)/Mean_200(close))"]


    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # EMA HIGH 5 / EMA CLOSE 5
    fields += ["(EMA($high, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(high)/EMA_5(close)"]

    fields += ["(EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["Change(EMA_5(high)/EMA_5(close))"]

    fields += ["""(
               ((EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1))
               - ((EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($high, 2), 5)/EMA(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(high)/EMA_5(close))"]

    # EMA LOW 5 / EMA CLOSE 5
    fields += ["(EMA($low, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(low)/EMA_5(close)"]

    fields += ["(EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["Change(EMA_5(low)/EMA_5(close))"]

    fields += ["""(
               ((EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1))
               - ((EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($low, 2), 5)/EMA(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(low)/EMA_5(close))"]

    # EMA OPEN 5 / EMA CLOSE(1) 5
    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["EMA_5(open)/EMA_5(close(1))"]

    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1)"]
    names += ["Change(EMA_5(open)/EMA_5(close(1)))"]

    fields += ["""(
               ((EMA($open, 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1))
               - ((EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1) - (EMA(Ref($open, 2), 5)/EMA(Ref($close, 3), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(open)/EMA_5(close(1)))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ Rolling Features (Statistical Significance) ---------------------------------
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
    # region ------------------------------- Rolling Features (Miscellaneous) -------------------------------------
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
    
    # endregion

    ###############################################################################################################
    # region ---------------------------------------- Indicators --------------------------------------------------
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [
        "{}".format(ci.MACD()),
        "{0} - {1}".format(ci.MACD(), ci.MACD(d=1))
    ]
    names += ["MACD", "acceleration_MACD"]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [
        ci.Bollinger_Band(r=20),
        "({0} / {1} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20), ci.Bollinger_Band(d=2, r=20))
    ]
    names += [
        "BollingerBand(20)",
        "change_BollingerBand(20)",
        "change_acceleration_BollingerBand(20)"
    ]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 14
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=14)),
        "{0} / Mean({0}, 3) - 1".format(ci.Stochastic_Oscillator(r=14))
    ]
    names += [
        "Stochastic_Oscillator(14)",
        "Stochastic_Oscillator(14)_signal(3)"
    ]

    # SO 8
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=8)),
        "{0} / Mean({0}, 5) - 1".format(ci.Stochastic_Oscillator(r=8))
    ]
    names += [
        "Stochastic_Oscillator(8)",
        "Stochastic_Oscillator(8)_signal(5)"
    ]
    
    ####################################################
    # # # Relative Strenght Index (RSI) Oscillator # # #
    ####################################################
    fields += [ci.RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        ci.Aroon_Up(r=14),
        ci.Aroon_Down(r=14),
        ci.Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        ci.Aroon_Up(r=25),
        ci.Aroon_Down(r=25),
        ci.Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    #############################################
    # # # Comodity Channel (CCI) Oscillator # # #
    #############################################

    # CCI 14
    fields += [ci.CCI(r=14)]
    names += ["CCI_14"]
    # CCI 21
    fields += [ci.CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [ci.CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    # fields += [ci.Positive_DI()]
    # names += ["Positive_DI"]

    # fields += [ci.Negative_DI()]
    # names += ["Negative_DI"]

    # fields += ["(%s - %s)" % (ci.Positive_DI(), ci.Negative_DI())]
    # names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [
        ci.ADX(r=14),
        "({0} / {1} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14), ci.ADX(d=2, r=14))
    ]
    names += [
        "ADX",
        "change_ADX",
        "change_acceleration_ADX"
    ]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [ci.CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ci.ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        ci.Bulls_Power(),
        ci.Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [ci.Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ###############
    # # # OBV # # #
    ###############
    windows = [10, 20]

    # fields += ["{s}/Mean({s}, {d})".format(s=ci.OBV(), d=d) for d in windows]
    # names += ["OBV/Mean%d(OBV)" % (d) for d in windows]

    fields += ["(Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1)".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change(Mean%d(OBV))" % (d) for d in windows]

    fields += ["""(
        (Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1) - (Mean(Ref({s}, 1), {d})/Mean(Ref({s}, 2), {d}) - 1)
    )""".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change_acceleration(Mean%d(OBV))" % (d) for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- Volume based Features ---------------------------------------------
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

    windows = [50, 100, 200]
    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, %d)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, %d)+1e-12)"
        % (d, d)
        for d in windows
    ]
    names += ["WVMA%d" % d for d in windows]

    windows = [10, 20, 50, 100]
    fields += [
        """
        If(Or(Or($close == 0, $volume == 0), Or(Ref($close,1) == 0, Ref($volume,1) == 0)),
        0, Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), %d))
        """
        % d for d in windows
    ]
    names += ["CORDV%d" % d for d in windows]

    windows = [5]  # 10, 20, 50, 100, 200
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
    # region ---------------------------------- Market Index Features ---------------------------------------------
    ###############################################################################################################

    if index_features:
    
        #######
        # SMA #
        #######
        windows = [
            5, 10, 20, 30,
            50, 100, 200
        ]

        # SMA variation
        fields += ["Mean($close_idx, %d)/Mean(Ref($close_idx, 1), %d)" % (d, d) for d in windows]
        names += ["Change_Mean_%d(close_idx)" % (d) for d in windows]

        # Mean 5 / Mean 10
        fields += ["(Mean($close_idx, 5)/Mean($close_idx, 10) - 1)"]
        names += ["Mean_5(close_idx)/Mean_10(close_idx)"]

        # Mean 10 / Mean 20
        fields += ["(Mean($close_idx, 10)/Mean($close_idx, 20) - 1)"]
        names += ["Mean_10(close_idx)/Mean_20(close_idx)"]

        # Mean 20 / Mean 50
        fields += ["(Mean($close_idx, 20)/Mean($close_idx, 50) - 1)"]
        names += ["Mean_20(close_idx)/Mean_50(close_idx)"]

        # Mean 50 / Mean 200
        fields += ["(Mean($close_idx, 50)/Mean($close_idx, 200) - 1)"]
        names += ["Mean_50(close_idx)/Mean_200(close_idx)"]

    # endregion
    
    return fields, names


# ---------------------------------------------------------------------------------------------------------------------


def dataset_features_ts_100_v1(index_features=False):
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- Basic Features -----------------------------------------------
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
    # region ------------------------------- Rolling Features (Mean based) ----------------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    
    #######
    # EMA #
    #######

    windows = [
        5, 8, 12, 26,
        50, 100, 200
    ]
    # Price vs EMA
    # fields += ["$close/EMA($close, %d)" % d for d in windows]
    # names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(EMA_%d(close))" % (d) for d in windows]
    # EMA Variation Acceleration
    fields += ["""(
        (EMA($close, %d)/EMA(Ref($close, 1), %d) - 1)
         - (EMA(Ref($close, 1), %d)/EMA(Ref($close, 2), %d) - 1)
    )""" % (d, d, d, d) for d in windows]
    names += ["Change_acceleration(EMA_%d(close))" % (d) for d in windows]


    # EMA 5 / EMA 8
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1)"]
    names += ["EMA_5(close)/EMA_8(close)"]
    
    fields += ["(EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1)"]
    names += ["Change(EMA_5(close)/EMA_8(close))"]

    fields += ["""(
               ((EMA($close, 5)/EMA($close, 8) - 1) - (EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1))
               - ((EMA(Ref($close, 1), 5)/EMA(Ref($close, 1), 8) - 1) - (EMA(Ref($close, 2), 5)/EMA(Ref($close, 2), 8) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(close)/EMA_8(close))"]

    # EMA 12 / EMA 26
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1)"]
    names += ["EMA_12(close)/EMA_26(close)"]
    
    fields += ["(EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1)"]
    names += ["Change(EMA_12(close)/EMA_26(close))"]

    fields += ["""(
                ((EMA($close, 12)/EMA($close, 26) - 1) - (EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1))
                - ((EMA(Ref($close, 1), 12)/EMA(Ref($close, 1), 26) - 1) - (EMA(Ref($close, 2), 12)/EMA(Ref($close, 2), 26) - 1))
            )"""]
    names += ["Change_acceleration(EMA_12(close)/EMA_26(close))"]

    # EMA 26 / EMA 50
    fields += ["(EMA($close, 26)/EMA($close, 50) - 1)"]
    names += ["EMA_26(close)/EMA_50(close)"]

    fields += ["(EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1)"]
    names += ["Change(EMA_26(close)/EMA_50(close))"]

    fields += ["""(
               ((EMA($close, 26)/EMA($close, 50) - 1) - (EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1))
               - ((EMA(Ref($close, 1), 26)/EMA(Ref($close, 1), 50) - 1) - (EMA(Ref($close, 2), 26)/EMA(Ref($close, 2), 50) - 1))
            )"""]
    names += ["Change_acceleration(EMA_26(close)/EMA_50(close))"]

    # EMA 50 / EMA 200
    fields += ["(EMA($close, 50)/EMA($close, 200) - 1)"]
    names += ["EMA_50(close)/EMA_200(close)"]

    fields += ["(EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1)"]
    names += ["Change(EMA_50(close)/EMA_200(close))"]

    fields += ["""(
               ((EMA($close, 50)/EMA($close, 200) - 1) - (EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1))
               - ((EMA(Ref($close, 1), 50)/EMA(Ref($close, 1), 200) - 1) - (EMA(Ref($close, 2), 50)/EMA(Ref($close, 2), 200) - 1))
            )"""]
    names += ["Change_acceleration(EMA_50(close)/EMA_200(close))"]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # EMA HIGH 5 / EMA CLOSE 5
    fields += ["(EMA($high, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(high)/EMA_5(close)"]

    fields += ["(EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["Change(EMA_5(high)/EMA_5(close))"]

    fields += ["""(
               ((EMA($high, 5)/EMA($close, 5) - 1) - (EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1))
               - ((EMA(Ref($high, 1), 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($high, 2), 5)/EMA(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(high)/EMA_5(close))"]

    # EMA LOW 5 / EMA CLOSE 5
    fields += ["(EMA($low, 5)/EMA($close, 5) - 1)"]
    names += ["EMA_5(low)/EMA_5(close)"]

    fields += ["(EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["Change(EMA_5(low)/EMA_5(close))"]

    fields += ["""(
               ((EMA($low, 5)/EMA($close, 5) - 1) - (EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1))
               - ((EMA(Ref($low, 1), 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($low, 2), 5)/EMA(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(low)/EMA_5(close))"]

    # EMA OPEN 5 / EMA CLOSE(1) 5
    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1)"]
    names += ["EMA_5(open)/EMA_5(close(1))"]

    fields += ["(EMA($open, 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1)"]
    names += ["Change(EMA_5(open)/EMA_5(close(1)))"]

    fields += ["""(
               ((EMA($open, 5)/EMA(Ref($close, 1), 5) - 1) - (EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1))
               - ((EMA(Ref($open, 1), 5)/EMA(Ref($close, 2), 5) - 1) - (EMA(Ref($open, 2), 5)/EMA(Ref($close, 3), 5) - 1))
            )"""]
    names += ["Change_acceleration(EMA_5(open)/EMA_5(close(1)))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ Rolling Features (Statistical Significance) ---------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    # STANDARD DEVIATION
    windows = [20]
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ------------------------------- Rolling Features (Miscellaneous) -------------------------------------
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
    
    # endregion

    ###############################################################################################################
    # region ---------------------------------------- Indicators --------------------------------------------------
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [
        "{}".format(ci.MACD()),
        "{0} - {1}".format(ci.MACD(), ci.MACD(d=1))
    ]
    names += ["MACD", "acceleration_MACD"]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [
        ci.Bollinger_Band(r=20),
        "({0} / {1} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20), ci.Bollinger_Band(d=2, r=20))
    ]
    names += [
        "BollingerBand(20)",
        "change_BollingerBand(20)",
        "change_acceleration_BollingerBand(20)"
    ]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 14
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=14)),
        "{0} / Mean({0}, 3) - 1".format(ci.Stochastic_Oscillator(r=14))
    ]
    names += [
        "Stochastic_Oscillator(14)",
        "Stochastic_Oscillator(14)_signal(3)"
    ]

    # SO 8
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=8)),
        "{0} / Mean({0}, 5) - 1".format(ci.Stochastic_Oscillator(r=8))
    ]
    names += [
        "Stochastic_Oscillator(8)",
        "Stochastic_Oscillator(8)_signal(5)"
    ]
    
    ####################################################
    # # # Relative Strenght Index (RSI) Oscillator # # #
    ####################################################
    fields += [ci.RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        ci.Aroon_Up(r=14),
        ci.Aroon_Down(r=14),
        ci.Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        ci.Aroon_Up(r=25),
        ci.Aroon_Down(r=25),
        ci.Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    #############################################
    # # # Comodity Channel (CCI) Oscillator # # #
    #############################################

    # CCI 14
    fields += [ci.CCI(r=14)]
    names += ["CCI_14"]
    # CCI 21
    fields += [ci.CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [ci.CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    # fields += [ci.Positive_DI()]
    # names += ["Positive_DI"]

    # fields += [ci.Negative_DI()]
    # names += ["Negative_DI"]

    # fields += ["(%s - %s)" % (ci.Positive_DI(), ci.Negative_DI())]
    # names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [
        ci.ADX(r=14),
        "({0} / {1} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14), ci.ADX(d=2, r=14))
    ]
    names += [
        "ADX",
        "change_ADX",
        "change_acceleration_ADX"
    ]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [ci.CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ci.ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        ci.Bulls_Power(),
        ci.Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [ci.Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ###############
    # # # OBV # # #
    ###############
    windows = [10, 20]

    # fields += ["{s}/Mean({s}, {d})".format(s=ci.OBV(), d=d) for d in windows]
    # names += ["OBV/Mean%d(OBV)" % (d) for d in windows]

    fields += ["(Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1)".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change(Mean%d(OBV))" % (d) for d in windows]

    fields += ["""(
        (Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1) - (Mean(Ref({s}, 1), {d})/Mean(Ref({s}, 2), {d}) - 1)
    )""".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change_acceleration(Mean%d(OBV))" % (d) for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- Market Index Features ---------------------------------------------
    ###############################################################################################################

    if index_features:
    
        #######
        # EMA #
        #######
        windows = [
            5, 8, 12, 26,
            50, 100, 200
        ]

        # EMA variation
        fields += ["EMA($close_idx, %d)/EMA(Ref($close_idx, 1), %d)" % (d, d) for d in windows]
        names += ["Change_EMA_%d(close_idx)" % (d) for d in windows]

        # EMA 5 / EMA 8
        fields += ["(EMA($close_idx, 5)/EMA($close_idx, 8) - 1)"]
        names += ["EMA_5(close_idx)/EMA_8(close_idx)"]

        # EMA 12 / EMA 26
        fields += ["(EMA($close_idx, 12)/EMA($close_idx, 26) - 1)"]
        names += ["EMA_12(close_idx)/EMA_26(close_idx)"]

        # EMA 26 / EMA 50
        fields += ["(EMA($close_idx, 26)/EMA($close_idx, 50) - 1)"]
        names += ["EMA_26(close_idx)/EMA_50(close_idx)"]

        # EMA 50 / EMA 200
        fields += ["(EMA($close_idx, 50)/EMA($close_idx, 200) - 1)"]
        names += ["EMA_50(close_idx)/EMA_200(close_idx)"]

    # endregion
    
    return fields, names


def dataset_features_ts_100_v2(index_features=False):
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- Basic Features -----------------------------------------------
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
    # region ------------------------------- Rolling Features (Mean based) ----------------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    
    #######
    # SMA #
    #######

    windows = [
        5, 10, 20, 30,
        50, 100, 200
    ]
    # Price vs Mean
    # fields += ["$close/Mean($close, %d)" % d for d in windows]
    # names += ["close/Mean_%d(close)" % d for d in windows]
    # Mean Variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(Mean_%d(close))" % (d) for d in windows]
    # Mean Variation Acceleration
    fields += ["""(
        (Mean($close, %d)/Mean(Ref($close, 1), %d) - 1)
         - (Mean(Ref($close, 1), %d)/Mean(Ref($close, 2), %d) - 1)
    )""" % (d, d, d, d) for d in windows]
    names += ["Change_acceleration(Mean_%d(close))" % (d) for d in windows]


    # Mean 5 / Mean 10
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1)"]
    names += ["Mean_5(close)/Mean_10(close)"]
    
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1) - (Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1)"]
    names += ["Change(Mean_5(close)/Mean_10(close))"]

    fields += ["""(
               ((Mean($close, 5)/Mean($close, 10) - 1) - (Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1))
               - ((Mean(Ref($close, 1), 5)/Mean(Ref($close, 1), 10) - 1) - (Mean(Ref($close, 2), 5)/Mean(Ref($close, 2), 10) - 1))
            )"""]
    names += ["Change_acceleration(Mean_5(close)/Mean_10(close))"]

    # Mean 10 / Mean 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]
    
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1)"]
    names += ["Change(Mean_10(close)/Mean_20(close))"]

    fields += ["""(
                ((Mean($close, 10)/Mean($close, 20) - 1) - (Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1))
                - ((Mean(Ref($close, 1), 10)/Mean(Ref($close, 1), 20) - 1) - (Mean(Ref($close, 2), 10)/Mean(Ref($close, 2), 20) - 1))
            )"""]
    names += ["Change_acceleration(Mean_10(close)/Mean_20(close))"]

    # Mean 20 / Mean 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]

    fields += ["(Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1)"]
    names += ["Change(Mean_20(close)/Mean_50(close))"]

    fields += ["""(
               ((Mean($close, 20)/Mean($close, 50) - 1) - (Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1))
               - ((Mean(Ref($close, 1), 20)/Mean(Ref($close, 1), 50) - 1) - (Mean(Ref($close, 2), 20)/Mean(Ref($close, 2), 50) - 1))
            )"""]
    names += ["Change_acceleration(Mean_20(close)/Mean_50(close))"]

    # Mean 50 / Mean 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    fields += ["(Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1)"]
    names += ["Change(Mean_50(close)/Mean_200(close))"]

    fields += ["""(
               ((Mean($close, 50)/Mean($close, 200) - 1) - (Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1))
               - ((Mean(Ref($close, 1), 50)/Mean(Ref($close, 1), 200) - 1) - (Mean(Ref($close, 2), 50)/Mean(Ref($close, 2), 200) - 1))
            )"""]
    names += ["Change_acceleration(Mean_50(close)/Mean_200(close))"]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # Mean HIGH 5 / Mean CLOSE 5
    fields += ["(Mean($high, 5)/Mean($close, 5) - 1)"]
    names += ["Mean_5(high)/Mean_5(close)"]

    fields += ["(Mean($high, 5)/Mean($close, 5) - 1) - (Mean(Ref($high, 1), 5)/Mean(Ref($close, 1), 5) - 1)"]
    names += ["Change(Mean_5(high)/Mean_5(close))"]

    fields += ["""(
               ((Mean($high, 5)/Mean($close, 5) - 1) - (Mean(Ref($high, 1), 5)/Mean(Ref($close, 1), 5) - 1))
               - ((Mean(Ref($high, 1), 5)/Mean(Ref($close, 1), 5) - 1) - (Mean(Ref($high, 2), 5)/Mean(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(Mean_5(high)/Mean_5(close))"]

    # Mean LOW 5 / Mean CLOSE 5
    fields += ["(Mean($low, 5)/Mean($close, 5) - 1)"]
    names += ["Mean_5(low)/Mean_5(close)"]

    fields += ["(Mean($low, 5)/Mean($close, 5) - 1) - (Mean(Ref($low, 1), 5)/Mean(Ref($close, 1), 5) - 1)"]
    names += ["Change(Mean_5(low)/Mean_5(close))"]

    fields += ["""(
               ((Mean($low, 5)/Mean($close, 5) - 1) - (Mean(Ref($low, 1), 5)/Mean(Ref($close, 1), 5) - 1))
               - ((Mean(Ref($low, 1), 5)/Mean(Ref($close, 1), 5) - 1) - (Mean(Ref($low, 2), 5)/Mean(Ref($close, 2), 5) - 1))
            )"""]
    names += ["Change_acceleration(Mean_5(low)/Mean_5(close))"]

    # Mean OPEN 5 / Mean CLOSE(1) 5
    fields += ["(Mean($open, 5)/Mean(Ref($close, 1), 5) - 1)"]
    names += ["Mean_5(open)/Mean_5(close(1))"]

    fields += ["(Mean($open, 5)/Mean(Ref($close, 1), 5) - 1) - (Mean(Ref($open, 1), 5)/Mean(Ref($close, 2), 5) - 1)"]
    names += ["Change(Mean_5(open)/Mean_5(close(1)))"]

    fields += ["""(
               ((Mean($open, 5)/Mean(Ref($close, 1), 5) - 1) - (Mean(Ref($open, 1), 5)/Mean(Ref($close, 2), 5) - 1))
               - ((Mean(Ref($open, 1), 5)/Mean(Ref($close, 2), 5) - 1) - (Mean(Ref($open, 2), 5)/Mean(Ref($close, 3), 5) - 1))
            )"""]
    names += ["Change_acceleration(Mean_5(open)/Mean_5(close(1)))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ Rolling Features (Statistical Significance) ---------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    # STANDARD DEVIATION
    windows = [20]
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ------------------------------- Rolling Features (Miscellaneous) -------------------------------------
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
    
    # endregion

    ###############################################################################################################
    # region ---------------------------------------- Indicators --------------------------------------------------
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += [
        "{}".format(ci.MACD()),
        "{0} - {1}".format(ci.MACD(), ci.MACD(d=1))
    ]
    names += ["MACD", "acceleration_MACD"]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [
        ci.Bollinger_Band(r=20),
        "({0} / {1} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.Bollinger_Band(r=20), ci.Bollinger_Band(d=1, r=20), ci.Bollinger_Band(d=2, r=20))
    ]
    names += [
        "BollingerBand(20)",
        "change_BollingerBand(20)",
        "change_acceleration_BollingerBand(20)"
    ]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 14
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=14)),
        "{0} / Mean({0}, 3) - 1".format(ci.Stochastic_Oscillator(r=14))
    ]
    names += [
        "Stochastic_Oscillator(14)",
        "Stochastic_Oscillator(14)_signal(3)"
    ]

    # SO 8
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=8)),
        "{0} / Mean({0}, 5) - 1".format(ci.Stochastic_Oscillator(r=8))
    ]
    names += [
        "Stochastic_Oscillator(8)",
        "Stochastic_Oscillator(8)_signal(5)"
    ]
    
    ####################################################
    # # # Relative Strenght Index (RSI) Oscillator # # #
    ####################################################
    fields += [ci.RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        ci.Aroon_Up(r=14),
        ci.Aroon_Down(r=14),
        ci.Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        ci.Aroon_Up(r=25),
        ci.Aroon_Down(r=25),
        ci.Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    #############################################
    # # # Comodity Channel (CCI) Oscillator # # #
    #############################################

    # CCI 14
    fields += [ci.CCI(r=14)]
    names += ["CCI_14"]
    # CCI 21
    fields += [ci.CCI(r=21)]
    names += ["CCI_21"]
    # CCI 50
    fields += [ci.CCI(r=50)]
    names += ["CCI_50"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    # fields += [ci.Positive_DI()]
    # names += ["Positive_DI"]

    # fields += [ci.Negative_DI()]
    # names += ["Negative_DI"]

    # fields += ["(%s - %s)" % (ci.Positive_DI(), ci.Negative_DI())]
    # names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [
        ci.ADX(r=14),
        "({0} / {1} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14)),
        "({0} / {1} - 1) - ({1} / {2} - 1)".format(ci.ADX(r=14), ci.ADX(d=1, r=14), ci.ADX(d=2, r=14))
    ]
    names += [
        "ADX",
        "change_ADX",
        "change_acceleration_ADX"
    ]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [ci.CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ci.ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        ci.Bulls_Power(),
        ci.Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [ci.Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ###############
    # # # OBV # # #
    ###############
    windows = [10, 20]

    # fields += ["{s}/Mean({s}, {d})".format(s=ci.OBV(), d=d) for d in windows]
    # names += ["OBV/Mean%d(OBV)" % (d) for d in windows]

    fields += ["(Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1)".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change(Mean%d(OBV))" % (d) for d in windows]

    fields += ["""(
        (Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1) - (Mean(Ref({s}, 1), {d})/Mean(Ref({s}, 2), {d}) - 1)
    )""".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change_acceleration(Mean%d(OBV))" % (d) for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------- Market Index Features ---------------------------------------------
    ###############################################################################################################

    if index_features:
    
        #######
        # SMA #
        #######
        windows = [
            5, 10, 20, 30,
            50, 100, 200
        ]

        # SMA variation
        fields += ["Mean($close_idx, %d)/Mean(Ref($close_idx, 1), %d)" % (d, d) for d in windows]
        names += ["Change_Mean_%d(close_idx)" % (d) for d in windows]

        # Mean 5 / Mean 10
        fields += ["(Mean($close_idx, 5)/Mean($close_idx, 10) - 1)"]
        names += ["Mean_5(close_idx)/Mean_10(close_idx)"]

        # Mean 10 / Mean 20
        fields += ["(Mean($close_idx, 10)/Mean($close_idx, 20) - 1)"]
        names += ["Mean_10(close_idx)/Mean_20(close_idx)"]

        # Mean 20 / Mean 50
        fields += ["(Mean($close_idx, 20)/Mean($close_idx, 50) - 1)"]
        names += ["Mean_20(close_idx)/Mean_50(close_idx)"]

        # Mean 50 / Mean 200
        fields += ["(Mean($close_idx, 50)/Mean($close_idx, 200) - 1)"]
        names += ["Mean_50(close_idx)/Mean_200(close_idx)"]

    # endregion

    return fields, names


# ---------------------------------------------------------------------------------------------------------------------


def dataset_features_ts_50_v1():
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- Basic Features -----------------------------------------------
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
    # region ------------------------------- Rolling Features (Mean based) ----------------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    
    #######
    # EMA #
    #######

    windows = [
        5, 8, 12, 26,
        50, 100, 200
    ]
    # Price vs EMA
    # fields += ["$close/EMA($close, %d)" % d for d in windows]
    # names += ["close/EMA_%d(close)" % d for d in windows]
    # EMA Variation
    fields += ["EMA($close, %d)/EMA(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(EMA_%d(close))" % (d) for d in windows]
    

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
    # region ------------------------ Rolling Features (Statistical Significance) ---------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    # STANDARD DEVIATION
    windows = [20]
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------------- Indicators --------------------------------------------------
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += ["{}".format(ci.MACD())]
    names += ["MACD"]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [ci.Bollinger_Band(r=20)]
    names += ["BollingerBand(20)"]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 14
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=14)),
        "{0} / Mean({0}, 3) - 1".format(ci.Stochastic_Oscillator(r=14))
    ]
    names += [
        "Stochastic_Oscillator(14)",
        "Stochastic_Oscillator(14)_signal(3)"
    ]
    
    ####################################################
    # # # Relative Strenght Index (RSI) Oscillator # # #
    ####################################################
    fields += [ci.RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        ci.Aroon_Up(r=14),
        ci.Aroon_Down(r=14),
        ci.Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        ci.Aroon_Up(r=25),
        ci.Aroon_Down(r=25),
        ci.Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    #############################################
    # # # Comodity Channel (CCI) Oscillator # # #
    #############################################

    # CCI 20
    fields += [ci.CCI(r=20)]
    names += ["CCI_20"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    # fields += [ci.Positive_DI()]
    # names += ["Positive_DI"]

    # fields += [ci.Negative_DI()]
    # names += ["Negative_DI"]

    fields += ["(%s - %s)" % (ci.Positive_DI(), ci.Negative_DI())]
    names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [ci.ADX(r=14)]
    names += ["ADX"]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [ci.CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ci.ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        ci.Bulls_Power(),
        ci.Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [ci.Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ###############
    # # # OBV # # #
    ###############
    windows = [15]

    # fields += ["{s}/Mean({s}, {d})".format(s=ci.OBV(), d=d) for d in windows]
    # names += ["OBV/Mean%d(OBV)" % (d) for d in windows]

    fields += ["(Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1)".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change(Mean%d(OBV))" % (d) for d in windows]

    # endregion

    return fields, names


def dataset_features_ts_50_v2():
    fields = []
    names = []

    ###############################################################################################################
    # region --------------------------------------- Basic Features -----------------------------------------------
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
    # region ------------------------------- Rolling Features (Mean based) ----------------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################
    
    #######
    # SMA #
    #######

    windows = [
        5, 10, 20, 30,
        50, 100, 200
    ]
    # Price vs Mean
    # fields += ["$close/Mean($close, %d)" % d for d in windows]
    # names += ["close/Mean_%d(close)" % d for d in windows]
    # Mean Variation
    fields += ["Mean($close, %d)/Mean(Ref($close, 1), %d) - 1" % (d, d) for d in windows]
    names += ["Change(Mean_%d(close))" % (d) for d in windows]


    # Mean 5 / Mean 10
    fields += ["(Mean($close, 5)/Mean($close, 10) - 1)"]
    names += ["Mean_5(close)/Mean_10(close)"]

    # Mean 10 / Mean 20
    fields += ["(Mean($close, 10)/Mean($close, 20) - 1)"]
    names += ["Mean_10(close)/Mean_20(close)"]

    # Mean 20 / Mean 50
    fields += ["(Mean($close, 20)/Mean($close, 50) - 1)"]
    names += ["Mean_20(close)/Mean_50(close)"]

    # Mean 50 / Mean 200
    fields += ["(Mean($close, 50)/Mean($close, 200) - 1)"]
    names += ["Mean_50(close)/Mean_200(close)"]

    #########################
    # # # MISCELLANEOUS # # #
    #########################
    # Mean HIGH 5 / Mean CLOSE 5
    fields += ["(Mean($high, 5)/Mean($close, 5) - 1)"]
    names += ["Mean_5(high)/Mean_5(close)"]

    # Mean LOW 5 / Mean CLOSE 5
    fields += ["(Mean($low, 5)/Mean($close, 5) - 1)"]
    names += ["Mean_5(low)/Mean_5(close)"]

    # Mean OPEN 5 / Mean CLOSE(1) 5
    fields += ["(Mean($open, 5)/Mean(Ref($close, 1), 5) - 1)"]
    names += ["Mean_5(open)/Mean_5(close(1))"]

    # endregion

    ###############################################################################################################
    # region ------------------------ Rolling Features (Statistical Significance) ---------------------------------
    ###############################################################################################################

    #################
    # # # CLOSE # # #
    #################

    # STANDARD DEVIATION
    windows = [20]
    fields += ["Std($close, %d)/$close" % d for d in windows]
    names += ["STD_%d(close)/close" % d for d in windows]

    # endregion

    ###############################################################################################################
    # region ---------------------------------------- Indicators --------------------------------------------------
    ###############################################################################################################

    ################
    # # # MACD # # #
    ################
    fields += ["{}".format(ci.MACD())]
    names += ["MACD"]

    ###########################
    # # # Bollinger Bands # # #
    ###########################
    fields += [ci.Bollinger_Band(r=20)]
    names += ["BollingerBand(20)"]

    #################################
    # # # Stochastic Oscillator # # #
    #################################

    # SO 14
    fields += [
        "{0}".format(ci.Stochastic_Oscillator(r=14)),
        "{0} / Mean({0}, 3) - 1".format(ci.Stochastic_Oscillator(r=14))
    ]
    names += [
        "Stochastic_Oscillator(14)",
        "Stochastic_Oscillator(14)_signal(3)"
    ]
    
    ####################################################
    # # # Relative Strenght Index (RSI) Oscillator # # #
    ####################################################
    fields += [ci.RSI(r=14)]
    names += ["RSI"]

    ############################
    # # # Aroon Oscillator # # #
    ############################

    # Aroon 14
    fields += [
        ci.Aroon_Up(r=14),
        ci.Aroon_Down(r=14),
        ci.Aroon_Oscillator(r=14)
    ]
    names += [
        "Aroon_Up(14)",
        "Aroon_Down(14)",
        "Aroon_Oscillator(14)"
    ]
    # Aroon 25
    fields += [
        ci.Aroon_Up(r=25),
        ci.Aroon_Down(r=25),
        ci.Aroon_Oscillator(r=25)
    ]
    names += [
        "Aroon_Up(25)",
        "Aroon_Down(25)",
        "Aroon_Oscillator(25)"
    ]

    #############################################
    # # # Comodity Channel (CCI) Oscillator # # #
    #############################################

    # CCI 20
    fields += [ci.CCI(r=20)]
    names += ["CCI_20"]

    ##################################
    # # # Directional Indicators # # #
    ##################################
    # fields += [ci.Positive_DI()]
    # names += ["Positive_DI"]

    # fields += [ci.Negative_DI()]
    # names += ["Negative_DI"]

    fields += ["(%s - %s)" % (ci.Positive_DI(), ci.Negative_DI())]
    names += ["Positive_DI-Negative_DI"]

    ###########################################
    # # # Average Directional Index (ADX) # # #
    ###########################################
    # ADX 14
    fields += [ci.ADX(r=14)]
    names += ["ADX"]

    ###################################
    # # # Choppy Indicator (CHOP) # # #
    ###################################
    fields += [ci.CHOP(r=14)]
    names += ["CHOP"]

    ####################################
    # # # Average True Range (ATR) # # #
    ####################################
    fields += [ci.ATR() + " / EMA($close, 14)"]
    names += ["ATR / EMA_14(close)"]

    ###################################
    # # # Bull's and Bear's Power # # #
    ###################################
    fields += [
        ci.Bulls_Power(),
        ci.Bears_Power()
    ]
    names += [
        "Bulls_Power",
        "Bears_Power"
    ]

    ############################
    # # # Money Flow Index # # #
    ############################
    fields += [ci.Money_Flow_Index()]
    names += ["Money_Flow_Index"]

    ###############
    # # # OBV # # #
    ###############
    windows = [15]

    # fields += ["{s}/Mean({s}, {d})".format(s=ci.OBV(), d=d) for d in windows]
    # names += ["OBV/Mean%d(OBV)" % (d) for d in windows]

    fields += ["(Mean({s}, {d})/Mean(Ref({s}, 1), {d}) - 1)".format(s=ci.OBV(), d=d) for d in windows]
    names += ["Change(Mean%d(OBV))" % (d) for d in windows]

    # endregion

    return fields, names

#  endregion
