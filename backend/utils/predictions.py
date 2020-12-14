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
    return [(x[0], x[1]['likeability']) for x in df.iterrows()]

def _get_sorted_discography_list(df_disc, df_personal):
    df = _compute_rank(df_disc, df_personal)
    print(df.columns)
    print(df.head())
    return [(x[0], x[1]['likeability']) for x in df.iterrows()]

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
    # Feed values through activation function
    likeability = [activation(alpha) for alpha in sum_zs]
    df_disc['likeability'] = likeability
    df_disc = df_disc.groupby('name').mean().sort_values(by='likeability', ascending=False)

    return df_disc

def activation(alpha):
    """
    Activation function given a z-score sum alpha.
    """
    factor = 8.5
    return np.e ** -((alpha/factor) ** 2)


def compute_weighted_mean(df):
    # get an average of all the columns for my songs
    features = [0] * len(df.mean())
    total_entries = 0
    for i, song_metrics in enumerate(df._get_numeric_data().iterrows()):
        # print(song_metrics)
        for idx, feature in enumerate(song_metrics[1]):
            features[idx] += (len(df) - i) * feature
        total_entries += (len(df) - i)

    ideal_features = [x / total_entries for x in features]
    return ideal_features


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
