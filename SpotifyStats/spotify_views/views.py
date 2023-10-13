from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import redirect
import requests

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''


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
    
    return HttpResponse("Callback handled")