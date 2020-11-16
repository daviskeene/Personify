from django.shortcuts import render, HttpResponseRedirect
import spotipy
import spotipy.util as util
from spotipy import oauth2
scope = 'user-top-read'
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''
username = ''

from utils.artistly import get_user_top_tracks
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
    total = []
    ids = []
    tracks = []
    results = sp.current_user_top_tracks(time_range='short_term', limit=75)
    for i, item in enumerate(results['items']):
        tracks.append(item)
    # print(results)
    # for r in results:
    #     print([x for x in r])
    #     for track in r['items']:
    #         tracks.append(track)

    print(tracks[0])
    return render(request, 'sign-in.html', {'results': tracks})


def after_sign_in(request):
    results = {}
    token = 'http://localhost:8000/after-sign-in/?{}'.format(request.GET.urlencode())
    sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,
                                   scope=scope, cache_path=".cache-" + username)
    code = sp_oauth.parse_response_code(token)
    print(code)
    token_info = sp_oauth.get_access_token(code)
    print(token_info)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        results = sp.current_user_saved_tracks()
    return render(request, 'sign-in.html', {'results': results['items']})