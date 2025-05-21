import sqlite3
import json
from collections import defaultdict
from datetime import datetime, timedelta

def load_logins_from_db(db_path='data/net_sentinel.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('SELECT timestamp, username, ip_address, location, success FROM logins')
    rows = c.fetchall()

    logins = []
    for row in rows:
        logins.append({
            "timestamp": row[0],
            "username": row[1],
            "ip_address": row[2],
            "location": row[3],
            "success": bool(row[4])
        })

    conn.close()
    return logins

def detect_anomalies(logins):
    anomalies = []

    # Load rule config from JSON
    with open("data/rules_config.json") as f:
        config = json.load(f)

    max_failed = config["max_failed_logins"]
    location_window = timedelta(minutes=config["location_window_minutes"])
    ignored_countries = set(config["ignored_countries"])
    abnormal_hours = set(config["abnormal_hours"])
    multi_ip_window = config["multi_ip_window_minutes"]

    user_failures = defaultdict(int)
    user_recent_logins = defaultdict(list)
    seen_location_anomalies = set()

    for entry in sorted(logins, key=lambda x: x['timestamp']):
        user = entry['username']
        ts = datetime.fromisoformat(entry['timestamp'])
        loc = entry['location']
        ip = entry['ip_address']
        success = entry['success']

        # Rule 1: Too many failed logins
        if not success:
            user_failures[user] += 1
            if user_failures[user] > max_failed:
                anomalies.append({
                    'rule': 'Too many failed logins',
                    'user': user,
                    'time': entry['timestamp'],
                    'ip': ip
                })
        else:
            user_failures[user] = 0

        # Rule 2: Location change within window (configurable)
        recent = user_recent_logins[user]
        for prev_ts, prev_loc in recent:
            if loc != prev_loc and (ts - prev_ts) <= location_window:
                if {loc, prev_loc}.issubset(ignored_countries):
                    continue
                window_key = (user, ts.strftime('%Y-%m-%d %H'))
                if window_key not in seen_location_anomalies:
                    anomalies.append({
                        'rule': 'Location change within 1 hour',
                        'user': user,
                        'time': entry['timestamp'],
                        'ip': ip,
                        'from': prev_loc,
                        'to': loc
                    })
                    seen_location_anomalies.add(window_key)
                break

        recent.append((ts, loc))
        if len(recent) > 10:
            user_recent_logins[user] = recent[-10:]

    # Rule 3: Multiple IPs used within configurable time window
    user_ips = defaultdict(list)
    for entry in logins:
        ts = datetime.fromisoformat(entry['timestamp'])
        user_ips[entry['username']].append((ts, entry['ip_address']))

    for user, records in user_ips.items():
        records.sort()
        seen_windows = set()
        for i in range(len(records)):
            t1, ip1 = records[i]
            for j in range(i + 1, len(records)):
                t2, ip2 = records[j]
                if abs((t2 - t1).total_seconds()) <= multi_ip_window * 60 and ip1 != ip2:
                    key = (user, t1.strftime('%Y-%m-%d %H'))
                    if key not in seen_windows:
                        anomalies.append({
                            'rule': 'Multiple IPs within 1 hour',
                            'user': user,
                            'time': t2.isoformat(),
                            'ip': ip2,
                            'from': ip1,
                            'to': ip2
                        })
                        seen_windows.add(key)
                    break

    # Rule 4: Login at abnormal hours (user-configurable hours)
    for entry in logins:
        ts = datetime.fromisoformat(entry['timestamp'])
        if ts.hour in abnormal_hours:
            anomalies.append({
                'rule': 'Login during abnormal hours',
                'user': entry['username'],
                'time': entry['timestamp'],
                'ip': entry['ip_address']
            })

    return anomalies
