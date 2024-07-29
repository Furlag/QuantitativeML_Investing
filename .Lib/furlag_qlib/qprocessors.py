from qlib.data.dataset.processor import Processor
from qlib.data.dataset.processor import get_group_columns


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
