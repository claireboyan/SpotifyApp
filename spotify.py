from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

scope = "playlist-modify-private playlist-modify-public user-library-modify"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
