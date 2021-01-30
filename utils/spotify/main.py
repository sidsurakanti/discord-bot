import spotipy
from spotipy import SpotifyClientCredentials
from utils.config import SPOTIFY_CLIENT, SPOTIFY_SECRET


def get_track(track_id: str = None):
    """Get the link to the specified track."""
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT,
                                                                                  client_secret=SPOTIFY_SECRET))
    results = spotify.track(track_id=track_id)
    return results['external_urls']['spotify']







