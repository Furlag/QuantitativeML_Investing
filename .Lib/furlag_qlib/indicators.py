
class CommonIndicators():

    # Rate of Change Oscillator
    def ROC(self, d=0, r=14):
        if d == 0:
            field = "($close / Ref($close, {r}))".format(r=r)
        else:
            field = "(Ref($close, {d}) / Ref($close, {dr}))".format(d=d, dr=d+r)
        return field


    # Moving Average Convergence Divergence
    def MACD(self, d=0, adapt=True):
        if adapt:
            if d == 0:
                field = """(
                    (EMA($close, 12) / EMA($close, 26))
                    - EMA((EMA($close, 12) / EMA($close, 26)), 9)
                )"""
            else:
                field = """(
                    (EMA(Ref($close, {d}), 12) / EMA(Ref($close, {d}), 26))
                    - EMA((EMA(Ref($close, {d}), 12) / EMA(Ref($close, {d}), 26)), 9)
                )""".format(d=d)
        else:
            if d == 0:
                field = """(
                    (EMA($close, 12) - EMA($close, 26))
                    - EMA((EMA($close, 12) - EMA($close, 26)), 9)
                )"""
            else:
                field = """(
                    (EMA(Ref($close, {d}), 12) - EMA(Ref($close, {d}), 26))
                    - EMA((EMA(Ref($close, {d}), 12) - EMA(Ref($close, {d}), 26)), 9)
                )""".format(d=d)
        return field


    # Stochastic Oscillator
    def Stochastic_Oscillator(self, d=0, r=14):
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
    def Williams_Percent_Range(self, d=0, r=14):
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
    def RSI(self, d=0, r=14):
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
    def Aroon_Up(self, d=0, r=25):
        if d == 0:
            field = "(100 * ({r} - IdxMax($high, {r})) / {r})".format(r=r)
        else:
            field = "(100 * ({r} - IdxMax(Ref($high, {d}), {r})) / {r})".format(r=r, d=d)
        return field


    def Aroon_Down(self, d=0, r=25):
        if d == 0:
            field = "(100 * ({r} - IdxMin($low, {r})) / {r})".format(r=r)
        else:
            field = "(100 * ({r} - IdxMin(Ref($low, {d}), {r})) / {r})".format(r=r, d=d)
        return field


    def Aroon_Oscillator(self, d=0, r=25):
        A_up = self.Aroon_Up(d=d, r=r)
        A_down = self.Aroon_Down(d=d, r=r)

        field = "(" + A_up + " - " + A_down + ")"
        return field


    # Commodity Channel Indicator (Oscillator)
    def CCI(self, d=0, r=20):
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
    def Bollinger_Band(self, d=0, r=20, m=2, adapt=True):
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
    def Ichimoku_Cloud__tenkan_sen(self, d=0):  # WARNING: Adapt for ML, don't use alone
        if d == 0:
            return "(Mean($high, 9) + Mean($low, 9) / 2)"
        else:
            return "(Mean(Ref($high, %d), 9) + Mean(Ref($low, %d), 9) / 2)" % (d, d)


    def Ichimoku_Cloud__kijun_sen(self, d=0):  # WARNING: Adapt for ML, don't use alone
        if d == 0:
            return "(Mean($high, 26) + Mean($low, 26) / 2)"
        else:
            return "(Mean(Ref($high, %d), 26) + Mean(Ref($low, %d), 26) / 2)" % (d, d)


    def Ichimoku_Cloud__senkou_span_A(self, d=0):  # WARNING: Adapt for ML, don't use alone
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


    def Ichimoku_Cloud__senkou_span_B(self, d=0):  # WARNING: Adapt for ML, don't use alone
        if d == 0:
            return "(Mean($high, 52) + Mean($low, 52) / 2)"
        else:
            return "(Mean(Ref($high, %d), 52) + Mean(Ref($low, %d), 52) / 2)" % (d, d)


    def Ichimoku_Cloud__chikou_span(self, d=0):  # WARNING: Adapt for ML, don't use alone
        return "Ref($close, %d)" % (26+d)


    # Directional Indicators
    def Positive_DI(self, d=0, r=14):
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
                            Ref($high, {d}) - Ref($low, {d}),
                            Greater(
                                Abs(Ref($high, {d}) - Ref($close, {d1})),
                                Abs(Ref($low, {d}) - Ref($close, {d1}))
                            )
                        ),
                        {r}
                    ) == 0,
                    0,
                    100 * Div(
                        EMA(
                            If(
                                And(Ref($high, {d}) - Ref($high, {d1}) > Ref($low, {d}) - Ref($low, {d1}), Ref($high, {d}) - Ref($high, {d1}) > 0),
                                Ref($high, {d}) - Ref($high, {d1}),
                                0
                            ),
                            {r}
                        ),
                        Mean(
                            Greater(
                                Ref($high, {d}) - Ref($low, {d}),
                                Greater(
                                    Abs(Ref($high, {d})-Ref($close, {d1})),
                                    Abs(Ref($low, {d})-Ref($close, {d1}))
                                )
                            ),
                            {r}
                        )
                    )
                )
            )""".format(d=d, d1=d+1, r=r)
        return field


    def Negative_DI(self, d=0, r=14):
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


    def ADX(self, d=0, r=14):
        p_DI = self.Positive_DI(d=d, r=r)
        n_DI = self.Negative_DI(d=d, r=r)

        field = "(100 * EMA(Abs(Div(Sub(" + p_DI + ", " + n_DI + "), Add(" + p_DI + ", " + n_DI + "))), {r}))".format(r=r)
        return field


    def ATR(self, d=0, r=14):  # WARNING: Adapt for ML, don't use alone
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


    def CHOP(self, d=0, r=14):
        if d == 0:
            field = """(
                100
                * Log(Sum({A_T_R}, {r}) / (Max($high, {r}) - Min($low, {r})))
                / Log($close-$close + {r})
            )""".format(A_T_R=self.ATR(d=d, r=1), r=r)
        else:
            field = """(
                100
                * Log(Sum({A_T_R}, {r}) / (Max(Ref($high, {d}), {r}) - Min(Ref($low, {d}), {r})))
                / Log($close-$close + {r})
            )""".format(A_T_R=self.ATR(d=d, r=1), r=r, d=d)
        return field


    def Bulls_Power(self, d=0, r=14, adapt=True):
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


    def Bears_Power(self, d=0, r=14, adapt=True):
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


    def Money_Flow_Index(self, d=0, r=14):
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


    def OBV(self, d=0):  # WARNING: Adapt for ML, don't use alone
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


    def AD_Line(self, d=0):  # WARNING: Adapt for ML, don't use alone
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
