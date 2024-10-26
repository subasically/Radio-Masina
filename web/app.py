from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_socketio import SocketIO, emit
import subprocess
import requests

app = Flask(__name__, static_folder='./', template_folder='./')
socketio = SocketIO(app)

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
        socketio.emit('queue_next', {'title': title, 'artist': artist})
        return "Success", 200
    else:
        return f"Error: {result.stderr}", 500

@app.route('/now_playing', methods=['GET'], endpoint='now_playing')
def now_playing():
    try:
        response = requests.get('http://10.10.10.5:8005/status-json.xsl')
        data = response.json()
        total_listeners = 0
        current_title = "Unknown"
        current_artist = "Unknown"
        
        for source in data['icestats']['source']:
            total_listeners += source.get('listeners', 0)
            if source.get('title') and source.get('artist'):
                current_title = source.get('title', 'Unknown')
                current_artist = source.get('artist', 'Unknown')
        
        return jsonify({"title": current_title, "artist": current_artist, "listeners": total_listeners})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)