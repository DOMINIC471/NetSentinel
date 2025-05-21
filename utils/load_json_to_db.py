import json
import sqlite3

def load_data(json_path='data/sample_logins.json', db_path='data/net_sentinel.db'):
    with open(json_path, 'r') as f:
        logins = json.load(f)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for entry in logins:
        c.execute('''
            INSERT INTO logins (timestamp, username, ip_address, location, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            entry['timestamp'],
            entry['username'],
            entry['ip_address'],
            entry['location'],
            int(entry['success'])
        ))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    load_data()
