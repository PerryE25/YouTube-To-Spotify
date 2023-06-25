# Handle everything related to the Spotify API

import webbrowser
from urllib.parse import urlencode
import base64
import requests

from secret import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_ID

# Create a Spotify playlist using the give song names
def create_playlist(songs):
    access_token = get_user_permission()
    track_uris = get_track_uris(songs, access_token)
    new_playlist_id = create_new_playlist(access_token)

    populate_playlist(track_uris, new_playlist_id, access_token)

def get_user_permission():
    # Obtain an access code by redirecting the user
    query = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "https://www.google.com/",
        "scope": "playlist-modify-private"
    }

    # Open the web browser for the user
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(query))
    auth_code = input("Plz gimmie the authorization code: ")

    # Use the access code to get the access token
    auth_header = base64.urlsafe_b64encode((SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET).encode())
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % auth_header.decode("ascii")
    }
    body = {
        "grant-type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "https://www.google.com/"
    }
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data = body, headers = header)

    print(response)
    return response.json()["access_token"]

# Get YT name and retrieve Spotify unique ID
def get_track_uris(songs, token):
    header = {
        "Authorization": "Bearer {}".format(token)
    }

    track_uris = []
    for track in songs:
        # Send a GET request to retrieve the song info
        base_url = "https://api.spotify.com/v1/search?q=remaster%2520track%3A{}%2520artist%3A{}&type=track"
        url = base_url.format(track["song"], track["artist"])
        response = requests.get(url, headers = header)

        uri = response.json()["tracks"]["items"][0]["uri"]
        track_uris.append(uri)

    return track_uris

def create_new_playlist(token):
    header = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    body = {
        "name": "My YouTube Playlist",
        "description": "Playlist created by the tutorial on developer.spotify.com",
        "public": False,
        "collaborative": True
    }
    url = "https://api.spotify.com/v1/users/{}/playlists".format(SPOTIFY_USER_ID)
    response = requests.post(url, json = body, headers = header)

    return response.json()["id"]

def populate_playlist(track_uris, playlist_id, token):
    header = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json"
    }
    body = {
        "uris": track_uris,
        "position": 0
    }
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    requests.post(url, json = body, headers = header)
