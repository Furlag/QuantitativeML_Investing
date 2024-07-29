
class Filters():  # "module_path": "qlib.data.filter"

    spain = [
        {   # Filter: At least 60 days of somewhat regular trading
            "filter_type": "ExpressionDFilter",
            "rule_expression": "Sum(If($volume > 0, 1, 0), 60) >= 55",
            "keep": True,
            "filter_start_time": None,
            "filter_end_time": None,

            "label_filter": False,
        },
        {   # Eliminate Indexes
            "filter_type": "NameDFilter",
            "name_rule_re": "(?!\^IBEX|INDC.MC|INDS.MC)",  # noqa
            "filter_start_time": None,
            "filter_end_time": None,

            "label_filter": False,
        },
        {   # Keep only desired tickers
            "filter_type": "NameDFilter",
            "name_rule_re": """
                |IBE.MC|ITX.MC|SAN.MC|BBVA.MC|CLNX.MC|AMS.MC|TEF.MC|FER.MC|CABK.MC|AENA.MC|
                |REP.MC|RED.MC|SGRE.MC|ELE.MC|IAG.MC|GRF.MC|ANA.MC|ACS.MC|MTS.MC|ENG.MC|
                |NTGY.MC|FDR.MC|MRL.MC|BKT.MC|COL.MC|MAP.MC|SAB.MC|ACX.MC|CIE.MC|ROVI.MC|
                |SLR.MC|IDR.MC|ALM.MC|PHM.MC|MEL.MC|

                |TL5.MC|SCYR.MC|EBRO.MC|VIS.MC|APPS.MC|ANE.MC|GEST.MC|LOG.MC|
            """,
            "filter_start_time": None,
            "filter_end_time": None,

            "label_filter": False,
        }
    ]

    # -------------------------------------------------------------------------------------

    us = [
        {   # Eliminate Indexes
            "filter_type": "NameDFilter",
            "name_rule_re": "(?!\^GSPC)",  # noqa
            "filter_start_time": None,
            "filter_end_time": None,

            "label_filter": False,
        },
        {   # Filter: At least 120 days of somewhat regular trading
            "filter_type": "ExpressionDFilter",
            "rule_expression": "Sum(If($volume > 0, 1, 0), 120) >= 115",
            "keep": True,
            "filter_start_time": None,
            "filter_end_time": None,

            "label_filter": False,
        },
    ]

    ################################
    # Label filter generator
    ################################
    def label_filter(self, expression, threshold=1.00):
        label_filter = [
            {   # Filter extreme y values
                "filter_type": "ExpressionDFilter",
                "rule_expression": "And({ex} < {thr}, {ex} > -{thr})".format(ex=expression, thr=threshold),
                "keep": True,
                "filter_start_time": None,
                "filter_end_time": None,

                "label_filter": True,
            }
        ]
        return label_filter
