from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
import requests

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'


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
        return redirect('intermediate_page')  # Redirect to another page or perform actions as needed
    return redirect('')  # Redirect back to login page if authentication failed

def intermediate_page(request):
    return render(request, 'intermediate_page.html')


def top_tracks(request):
    token_info = request.session.get('token_info')
    access_token = token_info['access_token']
    
    # Spotipy client with the token
    sp = spotipy.Spotify(auth = access_token)

    # Fetch top tracks
    results = sp.current_user_top_tracks(limit = 10, time_range="long_term")
    tracks = results['items']
    return render(request, 'top_tracks.html', {'top_tracks': tracks})


def top_artists(request):
    token_info = request.session.get('token_info')
    access_token = token_info['access_token']

    # Spotipy client with the token
    sp = spotipy.Spotify(auth=access_token)

    # Fetch top tracks
    results = sp.current_user_top_artists(limit=10, time_range="long_term")
    artist = results['items']
    return render(request, 'top_artists.html', {'top_artists': artist})


def get_recommendations(sp, top_n=10):
    # Fetching the top 5 tracks of the user to use as seed tracks
    users_top_tracks = [item['id'] for item in sp.current_user_top_tracks(limit=5)['items']]
    
    # Get recommendations based on the user's top tracks
    recommendations = sp.recommendations(seed_tracks=users_top_tracks, limit=top_n)
    
    return [track['id'] for track in recommendations['tracks']]


def display_recommendations(request):
    token_info = request.session.get('token_info')
    access_token = token_info['access_token']
    
    # Spotipy client with the token
    sp = spotipy.Spotify(auth = access_token)
    recommended_track_ids = get_recommendations(sp)
    recommended_tracks = sp.tracks(recommended_track_ids)['tracks']

    return render(request, 'recommendations.html', {'recommended_tracks': recommended_tracks})
