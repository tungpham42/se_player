from flask import Flask, request, redirect, render_template_string
import os
import requests
import urllib.parse

app = Flask(__name__)

# Player settings
PLAYER_FONT = "Verdana"
PLAYER_BG_COLOR = "000000"  # background color
PLAYER_FONT_COLOR = "ffffff"  # font color
PLAYER_PRIMARY_COLOR = "00edc3"  # primary color for loader and buttons
PLAYER_SECONDARY_COLOR = "10fdd3"  # secondary color for hovers and elements
PLAYER_LOADER = 1  # player loader (1 to 10)
PREFERRED_SERVER = 0  # server number (0 for no preference)
PLAYER_SOURCES_TOGGLE_TYPE = 1  # source list style (1 or 2)

@app.route('/')
def player():
    # Extract query parameters
    video_id = request.args.get('video_id')
    is_tmdb = request.args.get('tmdb', '0')
    season = request.args.get('season') or request.args.get('s', '0')
    episode = request.args.get('episode') or request.args.get('e', '0')

    if not video_id:
        return "Missing video_id"

    # Construct the request URL
    base_url = "https://getsuperembed.link/"
    params = {
        'video_id': video_id,
        'tmdb': is_tmdb,
        'season': season,
        'episode': episode,
        'player_font': PLAYER_FONT,
        'player_bg_color': PLAYER_BG_COLOR,
        'player_font_color': PLAYER_FONT_COLOR,
        'player_primary_color': PLAYER_PRIMARY_COLOR,
        'player_secondary_color': PLAYER_SECONDARY_COLOR,
        'player_loader': PLAYER_LOADER,
        'preferred_server': PREFERRED_SERVER,
        'player_sources_toggle_type': PLAYER_SOURCES_TOGGLE_TYPE
    }
    request_url = base_url + '?' + urllib.parse.urlencode(params)

    try:
        # Make the HTTP request
        response = requests.get(
            request_url,
            timeout=7,
            allow_redirects=True,
            verify=False
        )
        player_url = response.text

        # Check if the response is a valid URL
        if player_url.startswith('https://'):
            return redirect(player_url)
        else:
            return f"<span style='color:red'>{player_url}</span>"

    except requests.RequestException:
        return "Request server didn't respond"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
