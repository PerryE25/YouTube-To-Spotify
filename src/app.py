# Where we're going to run this program
# Program that we run
import youtube
import spotify

def run():
    # indentation is important in python so make sure it's consistent
    # python determines scope based on indenting
    
    # Get the songs from the YouTube playlist
    songs = youtube.get_songs()

    # Use the song names to create a Spotify playlist
    spotify.create_playlist(songs)

# Code to actually run the function
if __name__ == "__main__":
    run()