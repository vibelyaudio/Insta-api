import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "IBely API Working! Use /api?url=INSTAGRAM_LINK"

@app.route('/api')
def download():
    insta_url = request.args.get('url')
    if not insta_url:
        return jsonify({"error": "URL missing, add ?url=LINK"}), 400
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(insta_url, download=False)
            # direct video url
            video_url = info.get('url')
            if not video_url and 'entries' in info:
                video_url = info['entries'][0].get('url')
            return jsonify({
                "video_url": video_url,
                "title": info.get('title'),
                "status": "ok"
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
