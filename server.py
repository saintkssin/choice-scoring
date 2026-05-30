from flask import Flask, request, jsonify, send_from_directory
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/run', methods=['POST'])
def run_pipeline():
    data = request.json
    
    # Обновляем config.py с новыми параметрами
    config_content = f"""from datetime import datetime, timedelta

DATE_TO = datetime.now().strftime("%Y-%m-%d 23:59:59")
DATE_FROM = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d 00:00:00")

RINGOSTAT_API_KEY = "{data.get('ringostat_key', '')}"
GEMINI_API_KEY = "{data.get('gemini_key', '')}"
MIN_DURATION = {data.get('min_duration', 60)}
MANAGERS = {data.get('managers', [])}
LIMIT = {data.get('limit', 15)}
"""
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    # Запускаем pipeline
    for script in ['1_fetch_calls.py', '2_transcribe.py', '3_score.py', '4_report.py']:
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
    
    return jsonify({'status': 'ok'})

@app.route('/results')
def get_results():
    import csv, json, glob
    
    rows = []
    try:
        with open('output/report.csv', encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))
    except:
        pass
    
    transcripts = {}
    for f in glob.glob('data/transcripts/*.txt'):
        call_id = os.path.basename(f).replace('.txt', '')
        with open(f) as tf:
            transcripts[call_id] = tf.read()
    
    scores = {}
    for f in glob.glob('output/scores/*.json'):
        call_id = os.path.basename(f).replace('.json', '')
        with open(f) as sf:
            scores[call_id] = json.load(sf)
    
    calls = []
    try:
        with open('data/calls.csv') as f:
            for row in csv.DictReader(f):
                calls.append(row)
    except:
        pass
    
    return jsonify({
        'rows': rows,
        'transcripts': transcripts,
        'scores': scores,
        'calls': calls
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)