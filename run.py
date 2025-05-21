import os
import json
from app import create_app
from utils.simulate_logins import (
    generate_logins,
    inject_failed_logins,
    inject_location_switches,
    inject_multi_ip_usage
)
from utils.load_json_to_db import load_data

app = create_app()

@app.before_first_request
def initialize_database():
    os.makedirs("data", exist_ok=True)

    # Generate simulated login data
    logs = generate_logins(3000)
    inject_failed_logins(logs, 15)
    inject_location_switches(logs, 20)
    inject_multi_ip_usage(logs, 20)
    logs.sort(key=lambda x: x['timestamp'])

    # Save to sample JSON
    with open('data/sample_logins.json', 'w') as f:
        json.dump(logs, f, indent=2)

    # Remove existing DB if any
    db_path = 'data/net_sentinel.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    # Load into SQLite
    load_data()

if __name__ == '__main__':
    app.run(debug=True)
