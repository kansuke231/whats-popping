from flask import Flask, jsonify, send_from_directory
import json
import os
import glob
from pathlib import Path


BACKEND_DIR = Path(__file__).parent
WEB_APP_DIR = BACKEND_DIR.parent
app = Flask(__name__, static_folder=os.path.join(WEB_APP_DIR, "frontend/build"))


DATA_DIR = "data"  # Assuming the jsonl files are inside a "data" directory


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/events/<date>', methods=['GET'])
def get_events(date):
    filepaths = glob.glob(os.path.join(BACKEND_DIR, DATA_DIR, date, f"*.jsonl"))
    
    if not filepaths:
        return jsonify({"error": "Date not found"}), 404

    combined_events = []
   
    for filepath in filepaths:
        with open(filepath, "r") as f:
            for line in f:
                event = json.loads(line)
                combined_events.append(event)

    return jsonify(combined_events)

if __name__ == "__main__":
    app.run(debug=True)
