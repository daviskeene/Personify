import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd

from .predictions import _compute_rank, _get_sorted_discography_list

"""
Code inspired by:
https://morioh.com/p/31b8a607b2b0
"""


def get_client():
    """
    Returns the spotipy client, used to make requests to the Spotify API.
    """
    return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_artist(sp, name):
    """
    Get a Spotify artist's data
    :param name: Artist's name
    :return: JSON data containing artist information
    """
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    return items[0] if len(items) > 0 else None


def get_album_track_features(sp, album):
    """
    Return track features for all songs on a given album.
    :param album: Album ID
    :return: List containing track features for each song in the album.
    """
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    track_features = []
    for i, track in enumerate(tracks):
        print(i+1, track['name'])
        track_features.append(get_track_features(sp, track['id']))
    return track_features


def get_track_features(sp, id):
    """
    Get features for one specific track.
    :param id: Track ID
    :return: list containing track features for one song.
    """
    meta = sp.track(id)
    features = sp.audio_features(id)
    print(meta['name'])

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    url = meta['external_urls']['spotify']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature, url]
    return track


def get_discography_data(sp, artist, save=False):
    """
    Saves an Artist's discography data to a csv, with track features for each song.
    :param artist: Artist information (JSON), acquired from get_artist()
    :return: Pandas DataFrame with an artists' discography and track features for each song.
    """
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album,single')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    print(f'Total albums: {len(albums)}')
    unique = set()  # skip duplicate albums
    tracks = []
    for album in albums:
        name = album['name'].lower()
        if name not in unique:
            print(f'ALBUM: {name}')
            unique.add(name)
            tracks.extend(get_album_track_features(sp, album))
    # create dataset
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'url'])
    if save:
        df.to_csv(f"data/discography_{artist['name']}.csv", sep = ',')
    return df


def get_user_top_tracks(sp, sp_range, local=False):
    if local:
        from spotipy.oauth2 import SpotifyOAuth
        scope = 'user-top-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    ids = []
    results = sp.current_user_top_tracks(time_range=sp_range, limit=75)
    for i, item in enumerate(results['items']):
        ids.append(item['id'])
    return ids

def get_user_top_tracks_data(sp, save=False, local=False):

    ranges = ['short_term']
    dfs = []
    for r in ranges:
        track_ids = get_user_top_tracks(sp, r, local)

        features = []
        for id in track_ids:
            features.append(get_track_features(sp, id))

        df = pd.DataFrame(features, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'url'])
        if save:
            df.to_csv(f"data/user_daviskeene_{r}.csv", sep = ',')
        dfs.append(df)
    print(dfs[0].columns)
    return dfs
    

def save_artist_data(sp, artist, save=False):
    artist = get_artist(sp, artist)
    return get_discography_data(sp, artist, save)

if __name__ == "__main__":
    sp = get_client()
    personal_dfs = get_user_top_tracks_data(sp, save=True, local=True)
    df_discography = save_artist_data(sp, "Still Woozy", save=True)

    # print(_get_sorted_discography_list(df_discography, personal_dfs[0]))