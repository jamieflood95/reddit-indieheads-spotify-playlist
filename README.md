# reddit-indieheads-spotify-playlist
Add all new songs posted on /r/indieheads into a spotify playlist when this application is run

# Stack
- Python 2.7
- Flask
- Spotify API (Spotipy)
- Reddit API

# Setup
- Check out the project
- Configure your Spotify and Reddit API keys in app.py variables. Set your redirect uri to be something like 'http://localhost:5000/callback'. You also need to add your spotify playlist id and user id to the file.
- Run the project in command line (```python index.py```)
- A window may open in your browser. Copy the link and paste it in the console to verify your user information.
- The program will attempt to add all new songs (tagged with [FRESH] into the playlist)
- When it has finished the screen will show all song id's that have been added.

# Resources
- https://developer.spotify.com/web-api/
- https://www.reddit.com/dev/api/
- https://github.com/plamere/spotipy
