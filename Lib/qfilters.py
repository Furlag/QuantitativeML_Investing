
class Filters():  # "module_path": "qlib.data.filter"

    eu = [
        {   # Eliminate Indexes
            "filter_type": "NameDFilter",
            "name_rule_re": "^(?!EXSA\.DE$).*",  # noqa
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
