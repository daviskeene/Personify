import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def csv_to_df(path):
    """
    Convert path to csv to Pandas DataFrame
    """
    return pd.read_csv(path)

def get_sorted_discography_list(path_to_disc, path_to_personal):
    df = compute_rank(path_to_disc, path_to_personal)
    return [(x[0], x[1]['zscore_sum']) for x in df.iterrows()]

def _get_sorted_discography_list(df_disc, df_personal):
    df = _compute_rank(df_disc, df_personal)
    return [(x[0], x[1]['zscore_sum']) for x in df.iterrows()]

def compute_rank(path_to_disc, path_to_personal):
    """
    Returns a DataFrame sorted by rank
    """
    return _compute_rank(csv_to_df(path_to_disc), csv_to_df(path_to_personal))

def _compute_rank(df_disc, df_personal):
    """
    Return dataframe sorted by rank
    """
    df_disc = clean_df(df_disc)
    df_personal = clean_df(df_personal)

    w_mean = compute_weighted_mean(df_personal)
    stds = df_disc.std()

    sum_zs = [sum_z(list(df_disc._get_numeric_data().loc[i]), w_mean, stds) for i in range(df_disc.shape[0])]
    df_disc['zscore_sum'] = sum_zs
    df_disc = df_disc.groupby('name').mean().sort_values(by='zscore_sum', ascending=True)

    return df_disc


def compute_weighted_mean(df):
    # get an average of all the columns for my songs
    my_mean = df.mean()
    weighted_mean = [0] * len(my_mean)
    for entry in df._get_numeric_data().iterrows():
        for i in range(len(entry[1])):
            weighted_mean[i] += entry[1][i] * (np.e ** (-1.0 * entry[0]))
    return weighted_mean


def clean_df(df):
    if "Unnamed: 0" in df.columns:
        cols_to_drop = ["Unnamed: 0", "time_signature", "release_date", "popularity", "tempo", "length", "loudness", "danceability.1"]
    else:
        cols_to_drop = ["time_signature", "release_date", "popularity", "tempo", "length", "loudness"]
    df = df.drop(columns=cols_to_drop)
    return df


# Try using sum of z-scores as a metric
def sum_z(x, y, stdevs):
    """
    :param x: list of means
    :param y: song features
    :param stdevs: my stdevs
    """
    s = 0
    for i in range(len(x)):
        s += abs((y[i] - x[i]) / stdevs[i])
    return s

if __name__ == "__main__":
    # df = compute_rank("data/discography_Taylor Bennett.csv", "data/user_daviskeene_long_term.csv")
    # print(df.shape)
    # for i in df.iterrows():
    #     print(i[0], i[1]['zscore_sum'])
    print(get_sorted_discography_list("data/discography_Taylor Bennett.csv", "data/user_daviskeene_long_term.csv"))
