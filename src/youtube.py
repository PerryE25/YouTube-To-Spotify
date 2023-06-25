# Handle everything related to the YT API

# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from urllib.parse import quote

from secret import YOUTUBE_PLAYLIST_ID

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Get all the songs from a specified YouTube playlist
def get_songs():
    # use as a place holder when we implement more stuf in the future
    videos = get_videos_from_playlist()

    songs = []
    for video in videos["items"]:
        song_info = extract_song_info(video["snippet"]["title"])
        songs.append(song_info)

        return songs

def get_videos_from_playlist():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "src/credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=YOUTUBE_PLAYLIST_ID
    )
    response = request.execute()

    return response

# return the song info using a video title
# Miley Cyrus - Party in the USA => {
#   artist: "Miley%20Cyrus"
#   song: "Party%20in%20the%20USA"
# }
def extract_song_info(video_title):
    # Get the artist name in the song title
    info = video_title.split("-")
    artist_name = quote(info[0].strip(), safe = '')
    song_name = quote(info[1].strip(), safe = '')

    return {
        "artist": artist_name,
        "song": song_name
    }