import math
from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd  # type: ignore
from sklearn.cluster import KMeans  # type: ignore


def crossing2ma(fast_ma: pd.Series, slow_ma: pd.Series) -> pd.Series:
    _fast_ma = fast_ma.shift(1)
    _slow_ma = slow_ma.shift(1)
    crossing = ((fast_ma <= slow_ma) & (_fast_ma >= _slow_ma)) | (
        (fast_ma >= slow_ma) & (_fast_ma <= _slow_ma)
    )

    return crossing


def detection_support_resistance_lvl(close_price: pd.Series, k: int = 4) -> list:
    kmeans = KMeans(n_clusters=k, n_init="auto").fit(np.array(close_price).reshape(-1, 1))
    clusters = kmeans.predict(np.array(close_price).reshape(-1, 1))

    min_max_values = []
    for i in range(k):
        min_max_values.append([math.inf, -math.inf])

    for i in range(len(close_price)):
        cluster = clusters[i]

        if close_price[i] < min_max_values[cluster][0]:
            min_max_values[cluster][0] = close_price[i]

        if close_price[i] > min_max_values[cluster][1]:
            min_max_values[cluster][1] = close_price[i]

    filtered_maxmin_lvl = []
    sorted_maxmin_lvl = sorted(min_max_values, key=lambda x: x[0])
    for i, (_min, _max) in enumerate(sorted_maxmin_lvl):
        if i == 0:
            filtered_maxmin_lvl.append(_min)

        if i == len(min_max_values) - 1:
            filtered_maxmin_lvl.append(_max)
        else:
            filtered_maxmin_lvl.append(sum([_max, sorted_maxmin_lvl[i + 1][0]]) / 2)
    return filtered_maxmin_lvl


def resample_weekly2daily(
    daily_df: pd.DataFrame, weekly_df: pd.DataFrame, column_name: str
) -> pd.DataFrame:
    weekly_df_fit_daterange = weekly_df[weekly_df.index >= daily_df.index[0]]
    resampled_sma = weekly_df_fit_daterange[column_name].resample("D").interpolate(method="linear")

    merged_daily_df = pd.merge(daily_df, resampled_sma, on="Date", how="left")
    merged_daily_df[column_name] = merged_daily_df[column_name].fillna(resampled_sma[-1])
    return merged_daily_df


def get_last_weekday_date() -> date:
    today_datetime = datetime.now().date()

    diff = 1
    if today_datetime.weekday() == 0:
        return today_datetime
    if today_datetime.weekday() == 6:
        diff = 2

    return today_datetime - timedelta(days=diff)
