import requests
from utils.config import LYRICS_KEY as KEY


BASE_URL = f"https://api.musixmatch.com/ws/1.1/"

def get_lyrics(name, artist):
    if artist != None: # if artist isn't provided
        url = f"{BASE_URL}/track.search?apikey={KEY}&q_track={name}&q_artist={artist}"
    else:
        url = f"{BASE_URL}/track.search?apikey={KEY}&q_track={name}"

    response = requests.get(url=url).json()

    # gets the track id
    try: 
        track_id = response['message']['body']['track_list'][0]['track']['track_id']
    except Exception:
        return "Song not found. Please try again."
    
    # gets the lyrics
    try:
        lyrics = requests.get(url=f"{BASE_URL}/track.lyrics.get?apikey={KEY}&track_id={track_id}").json()['message']['body']['lyrics']['lyrics_body'][:-69]
    except Exception:
        lyrics = "Song not found. Please try again."
    return lyrics

