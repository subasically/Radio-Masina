from flask import Flask, request, jsonify, send_from_directory, render_template
import subprocess
import requests

app = Flask(__name__, static_folder='./', template_folder='./')

@app.route('/', endpoint='index')
def index():
    return render_template('index.html')

@app.route('/<path:path>', endpoint='static_proxy')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/queue_next', methods=['POST'], endpoint='queue_next')
def queue_next():
    title = request.form.get('title')
    artist = request.form.get('artist')
    result = subprocess.run(["python3", "queue_next.py", title, artist], capture_output=True, text=True)
    print(f"queue_next.py output: {result.stdout}", "app")
    if result.returncode == 0:
        return "Success", 200
    else:
        return f"Error: {result.stderr}", 500

@app.route('/now_playing', methods=['GET'], endpoint='now_playing')
def now_playing():
    try:
        response = requests.get('http://radio_masina_icecast:8000/status-json.xsl')
        data = response.json()
        # Extract metadata for the specific mountpoint
        mountpoint = '/radio.ogg'
        for source in data['icestats']['source']:
            if source['listenurl'].endswith(mountpoint):
                title = source.get('title', 'Unknown')
                artist = source.get('artist', 'Unknown')
                listeners = source.get('listeners', 0)
                return jsonify({"title": title, "artist": artist, "listeners": listeners})
        return jsonify([{"title": "Unknown"}, {"artist": "Unknown"}])
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)