import math
import pandas as pd


def average_minutes(data, activity_col, weight_col="weight"):
    data = data.rename(columns={weight_col: "weight",
                                activity_col: "minutes"})
    data = data[['weight', "minutes"]]
    data['weighted_minutes'] = data.weight * data.minutes
    return data.weighted_minutes.sum() / data.weight.sum()


def stdev_minutes(data, activity_col, weight_col="weight"):
    data_mean = average_minutes(data, activity_col, weight_col)
    data = data.rename(columns={weight_col: "weight",
                                activity_col: "minutes"})
    num_non0_obs = data[data.weight != 0].weight.count()
    data = data[["weight", "minutes"]]
    data['weighted_ss'] = data.weight * (data.minutes - data_mean)**2
    return math.sqrt(data.weighted_ss.sum() /
                     (((num_non0_obs-1)/num_non0_obs)*data.weight.sum()))


def hypothesis_test_plot(data, group_var, test_var, weight_var="weight"):
    data = data[[group_var, test_var, weight_var]]
    data_grouped = data.groupby(group_var)
    frame = pd.DataFrame()
    for group in data_grouped:
        count = group[1][weight_var].count()
        mean = average_minutes(group[1], test_var, weight_var)
        stdev = stdev_minutes(group[1], test_var, weight_var)
        frame = frame.append({group_var: group[0],
                              "mean": mean,
                              "error": (stdev*1.96/math.sqrt(count))},
                             ignore_index=True)
    frame.index = frame.pop(group_var)
    plot = frame.plot(kind="bar", yerr="error", figsize=(12, 8))
    return (frame, plot)
