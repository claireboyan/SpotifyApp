from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load credentials + set up client
load_dotenv()

scope = "user-library-read playlist-modify-private playlist-modify-public user-library-modify"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

open('search_results.txt', 'w').close()

# Search for artist
artist_query = 'cold as life'
search_results = sp.search(q='artist:' + artist_query, type='artist')
items = genres = search_results['artists']['items']

for item in items:
    # check genre to make sure it is the correct band
    genres = item['genres']
    # check name for same
    name = item['name']
    print("Name: " + name)
    print("Genres: ", genres)

    # corrects
    if name.lower() == artist_query.lower():
        if 
        print("Artist " + name + " found!")
        with open('search_results.txt', 'w') as f:
            id = item['id']
            uri = item['uri']
            top_tracks_json = sp.artist_top_tracks(id, country='US')['tracks']
            top_tracks = []
            for track in top_tracks_json:
                track_name = track['name']
                # track_uri = track['uri']
                # track_id = track['id']
                top_tracks.append(track_name)
            
            print("Artist: " + name, file=f)
            print("Genres: ", genres, file=f)
            print("ID: " + id, file=f)
            print("URI: " + uri, file=f)
            print("Top tracks: ", top_tracks, file=f)
            print("\n\n", file=f)
        
        break

    print("NO MATCH\n\n")