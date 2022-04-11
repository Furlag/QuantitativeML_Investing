from qlib.data.dataset.processor import Processor
from qlib.data.dataset.processor import get_group_columns


"""
def get_group_columns(df: pd.DataFrame, group: Union[Text, None]):
    '''
    get a group of columns from multi-index columns DataFrame
    Parameters
    ----------
    df : pd.DataFrame
        with multi of columns.
    group : str
        the name of the feature group, i.e. the first level value of the group index.
    '''
    if group is None:
        return df.columns
    else:
        return df.columns[df.columns.get_loc(group)]
"""


class DropLabelOutliners(Processor):
    def __init__(self, threshold=None, upper_threshold=None, lower_threshold=None):
        self.threshold = threshold
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

    def __call__(self, df):
        if self.upper_threshold is None and self.threshold is not None:
            self.upper_threshold = self.threshold
        if self.lower_threshold is None and self.threshold is not None:
            self.lower_threshold = - self.threshold

        if self.upper_threshold is not None and self.lower_threshold is not None:
            label_cols = get_group_columns(df, "label")
            df[label_cols] = df[label_cols][
                (df[label_cols] < self.upper_threshold) & (df[label_cols] > self.lower_threshold)
            ]

        return df
