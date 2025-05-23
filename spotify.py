from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64

def setup():
    # load credentials + set up client
    load_dotenv()
    scope = "user-library-read playlist-modify-private playlist-modify-public user-library-modify ugc-image-upload"
    global sp 
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_artist_top_tracks(artist_items, artist_query, acceptable_genres):
    print("\nSEARCH RESULTS FOR \'" + artist_query + "\'")
    print("-------------------------------------------------------")
    n = 0

    for item in artist_items:
        n += 1
        # check genre to make sure it is the correct band
        genres = item['genres']
        common_genres = [element for element in genres if element in acceptable_genres]
        # check name for same
        name = item['name']

        print()
        print(str(n) + ". Name: " + name)
        print("   Genres: ", genres)
        
        # name matches but no common genres
        if name.lower() == artist_query.lower() and len(common_genres) == 0:
            if not live_input_mode:
                print("Found an artist named " + name + " but with no matching genres. Skipping. Adjust the acceptable genres list to contain at least one of the genres from this search result if you believe this is a mistake.\n")
                continue

            print("Found an artist named " + name + " but with no matching genres. Their genres are listed as:")
            print(genres)
            add_to_playlist = input("Would you like to add them to the playlist? (y/n) ")
            
            if add_to_playlist.lower() == 'n' or add_to_playlist.lower() == 'no':
                # move onto next search result
                print("Skipping.")
                continue

        # name does not match but similar result appears with common genres
        elif name.lower() != artist_query.lower() and len(common_genres) > 0:
            if not live_input_mode:
                print("Did you mean " + name + " instead of \'" + artist_query + "\'? If so, please correct the list of artists in main function.\n")
                continue

            print("Found an artist named " + name + " with common genres: ")
            print(common_genres)
            add_to_playlist = input("Would you like to add them to the playlist? (y/n) ")
            if add_to_playlist.lower() == 'n' or add_to_playlist.lower() == 'no':
                # move onto next search result
                print("Skipping.")
                continue
        elif name.lower() != artist_query.lower() and len(common_genres) == 0:
            print("   Not a match.\n")
            continue

        # match found or user decided to add the suggested band
        print("\nArtist " + name + " found with common genres: ", common_genres)
        print("Adding to playlist.")
        id = item['id']
        top_tracks_json = sp.artist_top_tracks(id, country='US')['tracks']
        top_tracks = []
        for track in top_tracks_json:
            track_name = track['name']
            track_uri = track['uri']
            top_tracks.append({"track_name": track_name, "track_uri": track_uri})
        
        return top_tracks
        

    return []

def artist_query(artist_query, acceptable_genres):
    search_results = sp.search(q='artist:' + artist_query, type='artist')
    items = search_results['artists']['items']
    top_tracks = get_artist_top_tracks(items, artist_query, acceptable_genres)
    if len(top_tracks) > 0:
        top_tracks_uris = [element['track_uri'] for element in top_tracks]
        return top_tracks_uris
    return []

def update_description_and_cover(playlist_id, description, encoded_cover_image_string):
    if encoded_cover_image_string:
        sp.playlist_upload_cover_image(playlist_id, image_b64=encoded_cover_image_string)
    if description:
        sp.playlist_change_details(playlist_id, description=description)

def create_playlist(user_id, name, description, encoded_cover_image_string):
    playlist_id = ''
    # check if playlist already exists
    current_playlists_json = sp.current_user_playlists()['items']
    for playlist in current_playlists_json:
        if name == playlist['name']:
            print("Playlist \'" + name + "\' exists, appending instead of creating.")
            playlist_id = playlist['id']

    if not playlist_id:
        # create new if doesn't exist already
        print("Creating new playlist \'" + name + "\'")
        playlist_output = sp.user_playlist_create(user=user_id, name=name)
        playlist_id = playlist_output['id']

    # update cover image and description if there
    update_description_and_cover(playlist_id, description, encoded_cover_image_string)
    
    return playlist_id

def add_tracks_to_playlist(playlist_id, top_track_uris):
    playlist_tracks_json = sp.playlist_tracks(playlist_id)['items']
    playlist_track_uris = [element['track']['uri'] for element in playlist_tracks_json]
    for uri in top_track_uris:
        if uri in playlist_track_uris:
            continue
        sp.playlist_add_items(playlist_id,[uri])

def main():
    global live_input_mode
    live_input_mode = input("Would you like to use live input mode? (y/n) ")
    live_input_mode = (False, True)[live_input_mode.lower() == 'y' or live_input_mode.lower() == 'yes']

    artists = ['e-town concrete', 'cold world', 'never ending game', 'big boy', 'eighteen visions', 'fury', 'apex predator', 'bad beat', 'cosmic joke', 'cyadine', 'd-bloc', 'death before dishonor', 'doflame', 'gag', 'home invasion', 'queensway', 'limb from limb', 'si dios quiere', 'warhound', 'world of pain',
               'the killer', 'sector', 'homicidal', 'silverhammer', 'heavy down', 'hell is real',
               'cloakroom', 'bleached cross', 'turquoise', 'illusion of choice',
               'outta pocket', 'pain clinic', 'power of fear', 'cyclops', 'absent soul']
    acceptable_genres = ['hardcore', 'hardcore punk', 'metalcore', 'metal', 'thrash metal', 'speed metal', 'grindcore']
    playlist_name = 'THE RUMBLE 2025 (comprehensive)'
    playlist_description = "Main event and preshow/aftershow artists (6/26/2025-6/28/2025)"   # optional
    playlist_cover_image_path = "/Users/iphone./Downloads/RumbleCover2025_reduced2.jpg"  # optional
    if playlist_cover_image_path:
        with open(playlist_cover_image_path, "rb") as image_file:
            encoded_cover_image_string = base64.b64encode(image_file.read())
    else:
        encoded_cover_image_string = ''

    setup()
    user_id = sp.current_user()['id']
    playlist_id = create_playlist(user_id, playlist_name, playlist_description, encoded_cover_image_string)
    
    for artist in artists:
        top_track_uris = artist_query(artist, acceptable_genres)
        if len(top_track_uris) == 0:
            print("\nNo matches found for query \'" + artist + "\'. Continuing...")
            with open ("error_log.txt", "a") as f:
                f.write(artist)
                f.write('\n')
            continue

        add_tracks_to_playlist(playlist_id, top_track_uris)
        
if __name__=="__main__":
    main()