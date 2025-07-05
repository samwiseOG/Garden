import os
import json
from flask import Flask, request, jsonify
from datetime import datetime
from threading import Lock, Thread
import time
import shutil

app = Flask(__name__)

DATA_DIR = "data/active_data"
ARCHIVE_DIR = "data/closed_jsons"
file_base = "weatherJson_"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

lock = Lock()
current_filename = None
current_hour = None

def get_current_filename():
    now = datetime.now()
    filename = file_base + now.strftime("%Y-%m-%d_%H.json")
    return filename, now.hour

def archive_old_file(filename):
    src = os.path.join(DATA_DIR, filename)
    dst = os.path.join(ARCHIVE_DIR, filename)
    if os.path.exists(src):
        shutil.move(src, dst)

def hourly_file_manager():
    global current_filename, current_hour
    while True:
        with lock:
            filename, hour = get_current_filename()
            if filename != current_filename:
                if current_filename:
                    archive_old_file(current_filename)
                current_filename = filename
                current_hour = hour
                file_path = os.path.join(DATA_DIR, current_filename)
                with open(file_path, "w") as f:
                    json.dump([], f)
        time.sleep(60)

@app.route('/data', methods=['POST'])
def submit_data():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    with lock:
        file_path = os.path.join(DATA_DIR, current_filename)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f)

        with open(file_path, "r+") as f:
            existing_data = json.load(f)
            existing_data.append(data)
            f.seek(0)
            json.dump(existing_data, f, indent=2)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Start the hourly file manager in a separate thread
    Thread(target=hourly_file_manager, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)