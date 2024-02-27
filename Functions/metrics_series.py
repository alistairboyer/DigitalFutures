import pandas
from sklearn import metrics
from typing import Any


def metrics_series(y_true: Any, y_pred: Any, **series_kwargs: Any) -> Any:
    """get metrics data as a pandas.Series"""
    return pandas.Series(
        {
            "accuracy": metrics.accuracy_score(y_true, y_pred),
            "precision": metrics.precision_score(y_true, y_pred),
            "recall": metrics.recall_score(y_true, y_pred),
            "f1": metrics.f1_score(y_true, y_pred),
        },
        dtype=series_kwargs.pop("dtype", float),
        **series_kwargs,
    )
