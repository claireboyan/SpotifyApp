from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def setup():
    # Load credentials + set up client
    load_dotenv()
    scope = "user-library-read playlist-modify-private playlist-modify-public user-library-modify"
    global sp 
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # clear txt file for testing
    open('search_results.txt', 'w').close()

def get_artist_top_tracks(items, artist_query, acceptable_genres):
    for item in items:
        # check genre to make sure it is the correct band
        genres = item['genres']
        # check name for same
        name = item['name']
        print("Name: " + name)
        print("Genres: ", genres)

        # correct
        if name.lower() == artist_query.lower():
            print("Artist " + name + " found!")
            common_genres = [element for element in genres if element in acceptable_genres]
            if len(common_genres) == 0:
                print("WARNING: Artist genre not in acceptable genres. Result may be incorrect.")
            with open('search_results.txt', 'a') as f:
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
            
            return top_tracks

        print("NO MATCH\n\n")
        return []

def artist_query(artist_query, acceptable_genres):
    search_results = sp.search(q='artist:' + artist_query, type='artist')
    items = search_results['artists']['items']
    top_tracks = get_artist_top_tracks(items, artist_query, acceptable_genres)
    return top_tracks

def main():
    artists = ['foundation', 'cold as life', 'two witnesses', 'magnitude', 'suburban scum']
    acceptable_genres = ['hardcore', 'hardcore punk', 'metalcore']
    setup()
    for artist in artists:
        top_tracks = artist_query(artist, acceptable_genres)

if __name__=="__main__":
    main()