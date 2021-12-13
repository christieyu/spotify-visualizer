# Gets data from Spotify following tutorial: 
    # https://medium.com/@rafaelnduarte/how-to-retrieve-data-from-spotify-110c859ab304
    # https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b
    # https://towardsdatascience.com/get-your-spotify-streaming-history-with-python-d5a208bbcbd3

# importing the necessary packages
import spotipy
import spotipy.util as util
import csv

username = 'fabuloxide'
client_id ='f411a63b1fb44971b19d18aaac431a6f'
client_secret = '77072acfd8e04edcbd284c012801063b'
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-private'

token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)

sp = spotipy.Spotify(auth=token)

# name of csv file 
filename = "spotify_data1.csv"

def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results["items"]
    while results['next']:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks

# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 

    # writing the fields 
    csvwriter.writerow(['playlist_id', 'playlist_year', 'playlist_month', 'playlist_week', 'track_id', 'track_year', 'track_genre', 'track_explicit', 'track_valence', 'track_tempo']) 

    # get each playlist
    playlists = sp.user_playlists(username, 50, 54)["items"]
    playlist_year = 2020
    for playlist in playlists:
        playlist_data = []
        # get each playlist's track data
        try:
            tracks = get_playlist_tracks(username, playlist["id"])
            for track in tracks:
                playlist_month = playlist["name"].split("-")[0]
                playlist_week = playlist["name"].split("-")[1].split(":")[0]
                track_features = sp.audio_features(track["track"]["id"])
                track_artist = sp.artist(track["track"]["artists"][0]["id"])
                track_data =    [   # playlist ID
                                    playlist["id"], \
                                    # playlist year
                                    playlist_year, \
                                    # playlist month
                                    playlist_month, \
                                    # playlist week
                                    playlist_week, \
                                    # track ID
                                    track["track"]["id"], \
                                    # track year
                                    track["track"]["album"]["release_date"][:4], \
                                    # track genre (approximate)
                                    (track_artist["genres"][0] if track_artist["genres"] else "unspecified"), \
                                    # track explicitness
                                    track["track"]["explicit"], \
                                    # track valence
                                    track_features[0]["valence"], \
                                    # track tempo
                                    track_features[0]["tempo"]
                                ]
                print(track_data)
                playlist_data.append(track_data)
        except:
            print("MISSING DATA HERE")
        
        # decrement year
        if playlist_month == "january" and playlist_week == "i":
            playlist_year -= 1
        # writing the data rows 
        csvwriter.writerows(playlist_data)

# playlists = sp.user_playlists(username, 1, 0)
# playlist = playlists["items"][0]["id"]

# tracks = sp.playlist_items(playlist)
# for track in tracks["items"]:
#     print(track["track"]["name"])
#     print (sp.audio_analysis(track["track"]["id"]))
#     break