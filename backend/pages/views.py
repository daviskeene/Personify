from django.shortcuts import render, HttpResponseRedirect
import spotipy
import spotipy.util as util
from spotipy import oauth2
import pandas as pd
scope = 'user-top-read'
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''
username = ''

from utils.artistly import get_user_top_tracks_data, save_artist_data, _get_sorted_discography_list
# Create your views here.


def next_offset(n):
    try:
        return int(n['next'].split('?')[1].split('&')[0].split('=')[1])
    except ValueError:
        return None
    except AttributeError:
        return None
    except TypeError:
        return None


def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})


def sign_in(request):

    # token = util.prompt_for_user_token(username, scope)
    # print(token)
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + username)
    token_info = sp_oauth.get_cached_token()
    print(token_info)
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(auth_url)
        return HttpResponseRedirect(auth_url)
    sp = spotipy.Spotify(auth=token_info['access_token'])

    if request.method == "POST":
        # Get the artists' discography
        screenname = request.POST.get("handle", None)
        df_disc = save_artist_data(sp, screenname)
        df_personal = get_user_top_tracks_data(sp)[0]
        sorted_list = _get_sorted_discography_list(df_disc, df_personal)
        print(screenname)
        series = list(df_disc.loc[df_disc['name'] == x[0]] for x in sorted_list)
        tups = []
        for s in series:
            tup = (s.name.values[0], s.url.values[0])
            tups.append(tup)
        for i in range(len(tups)):
            tups[i] = (tups[i][0], tups[i][1], sorted_list[i][1])
        results = [{'name' : x[0], 'href' : x[1], 'score' : x[2]} for x in tups]
        return render(request, 'sign-in.html', {'results' : results, 'artist' : screenname})

    total = []
    ids = []
    tracks = []
    # results = sp.current_user_top_tracks(time_range='short_term', limit=75)
    # for i, item in enumerate(results['items']):
    #     tracks.append(item)
    # print(results)
    # for r in results:
    #     print([x for x in r])
    #     for track in r['items']:
    #         tracks.append(track)

    return render(request, 'sign-in.html', {'results': tracks, 'artist' : ''})


def after_sign_in(request):
    results = {}
    token = 'http://localhost:8000/after-sign-in/?{}'.format(request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + username)
    code = sp_oauth.parse_response_code(token)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_saved_tracks()
    return render(request, 'sign-in.html', {'results': results['items'], 'artist' : ''})
