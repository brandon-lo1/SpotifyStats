from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
import requests

SPOTIPY_CLIENT_ID = 'dc77fc145bf745d4a57a1c35ff15009b'
SPOTIPY_CLIENT_SECRET = 'fa41f2bd61804591a46f29845f197363'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'

# Create your views here.
def login_page(request):
     return HttpResponse('Login Here!')

def login_template(request):
    return render(request, 'login.html')

def spotify_login(request):
    sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-read-currently-playing user-top-read')
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback(request):
    sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-read-currently-playing user-top-read')
    if request.GET.get('code'):
        request.session['token_info'] = sp_oauth.get_access_token(request.GET.get('code'))

        # Store the token_info in the session or database for future use
        return redirect('top_tracks')  # Redirect to another page or perform actions as needed
    return redirect('')  # Redirect back to login page if authentication failed

def top_tracks(request):
    token_info = request.session.get('token_info')
    access_token = token_info['access_token']

    # Spotipy client with the token
    sp = spotipy.Spotify(auth = access_token)

    # Fetch top tracks
    results = sp.current_user_top_tracks(limit = 10)
    tracks = results['items']
    print(tracks)
    return render(request, 'top_tracks.html', {'top_tracks': tracks})
