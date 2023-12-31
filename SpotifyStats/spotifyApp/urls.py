"""
URL configuration for SpotifyStats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spotify_views import views as view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.login_template),
    path('spotify-login/', view.spotify_login, name='spotify-login'),
    path('callback/', view.callback, name='callback'),
    path('intermediate-page', view.intermediate_page, name='intermediate_page'),
    path('top_tracks/', view.top_tracks, name='top_tracks'),
    path('top_tracks/', view.top_tracks, name='top_tracks'),
    path('top_artists/', view.top_artists, name='top_artists'),
    path('recommendations/', view.display_recommendations, name='display_recommendations'),
    ]