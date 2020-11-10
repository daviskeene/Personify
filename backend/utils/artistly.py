import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd

"""
Code inspired by:
https://morioh.com/p/31b8a607b2b0
"""


def get_client():
    """
    Returns the spotipy client, used to make requests to the Spotify API.
    """
    return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_artist(name):
    """
    Get a Spotify artist's data
    :param name: Artist's name
    :return: JSON data containing artist information
    """
    sp = get_client()
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    return items[0] if len(items) > 0 else None


def get_album_track_features(album):
    """
    Return track features for all songs on a given album.
    :param album: Album ID
    :return: List containing track features for each song in the album.
    """
    tracks = []
    sp = get_client()
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    track_features = []
    for i, track in enumerate(tracks):
        print(i+1, track['name'])
        track_features.append(get_track_features(track['id']))
    return track_features


def get_track_features(id):
    """
    Get features for one specific track.
    :param id: Track ID
    :return: list containing track features for one song.
    """
    sp = get_client()
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

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track


def get_discography_data(artist):
    """
    Saves an Artist's discography data to a csv, with track features for each song.
    :param artist: Artist information (JSON), acquired from get_artist()
    :return: Pandas DataFrame with an artists' discography and track features for each song.
    """
    albums = []
    sp = get_client()
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
            tracks.extend(get_album_track_features(album))
    # create dataset
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
    df.to_csv(f"discography_{artist['name']}.csv", sep = ',')
    return df


def get_user_top_tracks(sp_range):
    from spotipy.oauth2 import SpotifyOAuth

    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    ids = []
    results = sp.current_user_top_tracks(time_range=sp_range, limit=75)
    for i, item in enumerate(results['items']):
        ids.append(item['id'])
    return ids

def get_user_top_tracks_data():

    ranges = ['short_term', 'medium_term', 'long_term']
    for r in ranges:
        track_ids = get_user_top_tracks(r)

        features = []
        for id in track_ids:
            features.append(get_track_features(id))

        df = pd.DataFrame(features, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
        df.to_csv(f"user_daviskeene_{r}.csv", sep = ',')
    

def main(artist):
    artist = get_artist(artist)
    get_discography_data(artist)

if __name__ == "__main__":
    # get_user_top_tracks_data()
    main("Clairo")