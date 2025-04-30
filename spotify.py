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
                    track_uri = track['uri']
                    # track_id = track['id']
                    top_tracks.append({"track_name": track_name, "track_uri": track_uri})
                
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
    if len(top_tracks) > 0:
        top_tracks_uris = [element['track_uri'] for element in top_tracks]
        return top_tracks_uris
    return []

def create_playlist(user_id, name):
    current_playlists_json = sp.current_user_playlists()['items']
    for playlist in current_playlists_json:
        if name == playlist['name']:
            print("Playlist \'" + name + "\' exists, appending instead of creating.")
            return playlist['id']

    print("Creating new playlist \'" + name + "\'")
    playlist_output = sp.user_playlist_create(user=user_id, name=name)
    return playlist_output['id']

def add_tracks_to_playlist(playlist_id, top_track_uris):
    playlist_tracks_json = sp.playlist_tracks(playlist_id)['items']
    playlist_track_uris = [element['track']['uri'] for element in playlist_tracks_json]
    for uri in top_track_uris:
        if uri in playlist_track_uris:
            continue
        sp.playlist_add_items(playlist_id,[uri])

def main():
    artists = ['prevention', 'big ass truck i.e.', 'barrio slam']
    acceptable_genres = ['hardcore', 'hardcore punk', 'metalcore']
    setup()
    user_id = sp.current_user()['id']

    playlist_id = create_playlist(user_id, 'python_test')
    
    for artist in artists:
        top_track_uris = artist_query(artist, acceptable_genres)
        if len(top_track_uris) == 0:
            print("There was no match found for \'" + artist + ".\' Continuing")
            continue

        add_tracks_to_playlist(playlist_id, top_track_uris)
        
if __name__=="__main__":
    main()