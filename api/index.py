import feedparser
import time
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SOURCES = {
    "VAARA": "https://112.fi/vaaratiedotteet-rss",
    "POLIISI": "https://poliisi.fi/ajankohtaista/uutiset/-/asset_publisher/vK9pUnk5iI9i/rss",
    "PELASTUS": "https://www.tilannehuone.fi/haelytykset-rss.php"
}

@app.route('/api/full_feed')
def get_full_feed():
    all_events = []
    for name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                all_events.append({
                    "id": entry.id if hasattr(entry, 'id') else entry.link,
                    "source": name,
                    "title": entry.title,
                    "summary": entry.summary if hasattr(entry, 'summary') else "",
                    "published": entry.published if hasattr(entry, 'published') else "Nyt"
                })
        except Exception as e:
            print(f"Haku epäonnistui: {e}")
    return jsonify(all_events)

app = app
