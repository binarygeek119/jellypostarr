from flask import Flask, render_template_string, request
import requests
import random

app = Flask(__name__)

# Configuration
JELLYFIN_SERVER = 'http://192.168.1.100:8096'  # Replace with your Jellyfin server URL
API_KEY = 'abc123-ABC456-0000-000-00000'  # Replace with your Jellyfin API key

def get_movie_items(start_index=0, limit=100):
    headers = {'X-Emby-Token': API_KEY}
    params = {
        'IncludeItemTypes': 'Movie',
        'Recursive': 'true',
        'SortBy': 'Random',
        'StartIndex': start_index,
        'Limit': limit
    }
    response = requests.get(f'{JELLYFIN_SERVER}/Items', headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('Items', [])
    return []

def get_random_poster_url(start_index=0, limit=100):
    movies = get_movie_items(start_index, limit)
    if movies:
        movie = random.choice(movies)
        poster_url = f"{JELLYFIN_SERVER}/Items/{movie['Id']}/Images/Primary?api_key={API_KEY}"
        return poster_url
    return None

@app.route('/')
def index():
    start_index = int(request.args.get('start', 0))
    limit = int(request.args.get('count', 100))
    
    poster_url = get_random_poster_url(start_index, limit)
    if poster_url:
        return render_template_string('''
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Random Movie Poster</title>
                <meta http-equiv="refresh" content="60">  <!-- Refresh every 60 seconds -->
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #000000;
                    }
                    img {
                        max-width: 90%;
                        max-height: 90%;
                        border: 2px solid #ccc;
                        border-radius: 10px;
                    }
                </style>
            </head>
            <body>
                <img src="{{ poster_url }}" alt="Random Movie Poster">
            </body>
            </html>
        ''', poster_url=poster_url)
    return 'No posters available', 404

if __name__ == '__main__':
    app.run(debug=True)
