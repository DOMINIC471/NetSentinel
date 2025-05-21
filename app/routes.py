import sqlite3
import json
import random
from datetime import datetime
from collections import defaultdict
from flask import Blueprint, render_template, jsonify, redirect, url_for, make_response, request, session
from functools import wraps

from .anomaly import load_logins_from_db, detect_anomalies
from utils.simulate_logins import generate_logins, inject_failed_logins, inject_location_switches, inject_multi_ip_usage
from utils.load_json_to_db import load_data

main = Blueprint('main', __name__)

# Load users from JSON file
def load_users():
    with open("data/users.json") as f:
        return json.load(f)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('main.index'))
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

# Logout route
@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))

# Home dashboard (protected)
@main.route('/')
@login_required
def index():
    with open("data/rules_config.json") as f:
        config = json.load(f)
    return render_template('index.html', config=config)

# Anomalies page (protected)
@main.route('/anomalies')
@login_required
def anomalies():
    logins = load_logins_from_db()
    detected = detect_anomalies(logins)
    return render_template('anomalies.html', anomalies=detected)

# Anomaly summary data (protected)
@main.route('/anomaly-stats')
@login_required
def anomaly_stats():
    logins = load_logins_from_db()
    detected = detect_anomalies(logins)

    counts = {}
    for a in detected:
        rule = a['rule']
        counts[rule] = counts.get(rule, 0) + 1

    response = make_response(jsonify(counts))
    response.headers['Cache-Control'] = 'no-store'
    return response

# Time-series login activity (protected)
@main.route('/login-activity')
@login_required
def login_activity():
    conn = sqlite3.connect('data/net_sentinel.db')
    c = conn.cursor()

    c.execute('''
        SELECT strftime('%Y-%m-%d %H:00:00', timestamp) AS hour, COUNT(*)
        FROM logins
        GROUP BY hour
        ORDER BY hour
    ''')
    rows = c.fetchall()
    conn.close()

    data = {hour: count for hour, count in rows}
    return jsonify(data)

# Regenerate new simulated data (protected)
@main.route('/generate')
@login_required
def generate():
    total_logins = random.randint(2800, 3500)
    failed_bursts = random.randint(10, 20)
    location_switches = random.randint(15, 30)
    multi_ip_events = random.randint(15, 30)

    logs = generate_logins(total_logins)
    inject_failed_logins(logs, failed_bursts)
    inject_location_switches(logs, location_switches)
    inject_multi_ip_usage(logs, multi_ip_events)
    logs.sort(key=lambda x: x['timestamp'])

    with open('data/sample_logins.json', 'w') as f:
        json.dump(logs, f, indent=2)

    conn = sqlite3.connect('data/net_sentinel.db')
    c = conn.cursor()
    c.execute('DELETE FROM logins')
    conn.commit()
    conn.close()

    load_data()
    return redirect(url_for('main.anomalies'))

# Save user-defined config (protected)
@main.route('/save-config', methods=['POST'])
@login_required
def save_config():
    config = {
        "max_failed_logins": int(request.form["max_failed_logins"]),
        "location_window_minutes": int(request.form["location_window_minutes"]),
        "multi_ip_window_minutes": int(request.form["multi_ip_window_minutes"]),
        "abnormal_hours": [int(h.strip()) for h in request.form["abnormal_hours"].split(',') if h.strip().isdigit()],
        "ignored_countries": [c.strip().upper() for c in request.form["ignored_countries"].split(',') if c.strip()]
    }

    with open("data/rules_config.json", "w") as f:
        json.dump(config, f, indent=2)

    return redirect(url_for('main.index'))
