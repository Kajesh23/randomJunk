from flask import Flask, render_template, Response
import pandas as pd
import time
import json
import os

app = Flask(__name__)

# Paths to CSV files
EEG_CSV_PATH = os.path.join('static', 'eeg_data.csv')
SPEECH_CSV_PATH = os.path.join('static', 'speech_data.csv')

# Function to simulate real-time EEG data from CSV
def generate_eeg_data():
    eeg_df = pd.read_csv(EEG_CSV_PATH)  # Load EEG data from CSV
    for index, row in eeg_df.iterrows():
        timestamp = row['timestamp']  # Assuming 'timestamp' column exists
        eeg_value = row['value']  # Assuming 'value' column exists
        yield f"data: {json.dumps({'time': timestamp, 'value': eeg_value})}\n\n"
        time.sleep(1)  # Simulate real-time delay

# Function to simulate real-time speech data from CSV
def generate_speech_data():
    speech_df = pd.read_csv(SPEECH_CSV_PATH)  # Load speech data from CSV
    for index, row in speech_df.iterrows():
        timestamp = row['timestamp']  # Assuming 'timestamp' column exists
        speech_text = row['text']  # Assuming 'text' column exists
        yield f"data: {json.dumps({'time': timestamp, 'text': speech_text})}\n\n"
        time.sleep(2)  # Simulate real-time delay

@app.route('/')
def index():
    return render_template('index.html')

# SSE endpoint for EEG data
@app.route('/eeg_stream')
def eeg_stream():
    return Response(generate_eeg_data(), mimetype='text/event-stream')

# SSE endpoint for speech data
@app.route('/speech_stream')
def speech_stream():
    return Response(generate_speech_data(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
