from flask import Flask, render_template
import requests
import praw
import spotipy
import spotipy.util as util
import time
import datetime

app = Flask(__name__)

spotify_username = 'SPOTIFY_USERNAME'
spotify_playlist_id = 'SPOTIFY_PLAYLIST_ID'
scope = 'playlist-modify-public'
spotify_client_secret= 'SPOTIFY_CLIENT_SECRET'
spotify_client_id= 'SPOTIFY_CLIENT_ID'
spotify_redirect_uri= 'SPOTIFY_REDIRECT_URI'
reddit_client_id='REDDIT_CLIENT_ID'
reddit_client_secret='REDDIT_CLIENT_SECRET'
reddit_user_agent='YOUR_NAME'


@app.route('/')
def index():

    r = praw.Reddit(user_agent=reddit_user_agent, client_id=reddit_client_id,client_secret=reddit_client_secret)
    sp = spotipy.Spotify()
    songs_to_add = []
    song_names_to_add = []
    current_tracks_in_playlist = []

    token = util.prompt_for_user_token(spotify_username, scope, client_id=spotify_client_id,
                                       client_secret=spotify_client_secret, redirect_uri=spotify_redirect_uri)

    tracks_in_playlist = None

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        tracks_in_playlist = sp.user_playlist(spotify_username, spotify_playlist_id)
        tracks_in_playlist = tracks_in_playlist['tracks']['items']
    else:
        print("Can't get token for", spotify_username)

    # get a list of all tracks in the playlist
    for track in tracks_in_playlist:
        current_tracks_in_playlist.insert(len(current_tracks_in_playlist), track['track']['id'])

    # dates that will be searched for new music on reddit
    time_to = time.mktime(datetime.datetime.now().timetuple())
    time_from = time.mktime((datetime.datetime.now() - datetime.timedelta(days=3)).timetuple())

    for submission in r.subreddit('indieheads').submissions(time_from, time_to):
        if '[FRESH]' in submission.title:
            query = submission.title.replace('[FRESH]', '')
            # search for the track on spotify and add to the playlist
            results = sp.search(q=query, limit=1)['tracks']['items']
            for n in results:
                song_id = n['id']
                # if the song is not already in the playlist and
                # 100 songs have not already been found (max for spotipy)
                # and the song is not already in the list of songs to add
                if (len(songs_to_add) < 100) and (song_id not in current_tracks_in_playlist) and (song_id not in songs_to_add):
                    songs_to_add.insert(len(songs_to_add), song_id.encode("utf-8"))

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        # add the tracks to the playlist on spotify
        if len(songs_to_add) > 0:
            print songs_to_add
            sp.user_playlist_remove_all_occurrences_of_tracks(spotify_username, spotify_playlist_id, songs_to_add)
            sp.user_playlist_add_tracks(spotify_username, spotify_playlist_id, songs_to_add)
    else:
        print("Can't get token for", spotify_username)

    return render_template('index.html', title='Home', results=songs_to_add)

if __name__ == '__main__':
   app.run()