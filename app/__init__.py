import os
import json
from flask import Flask
from .routes import main
from utils.simulate_logins import (
    generate_logins,
    inject_failed_logins,
    inject_location_switches,
    inject_multi_ip_usage
)
from utils.load_json_to_db import load_data

def create_app():
    app = Flask(__name__)
    app.secret_key = "net-sentinel-secret-key"
    app.register_blueprint(main)

    # Run once when app starts (good for deployment)
    os.makedirs("data", exist_ok=True)

    if not os.path.exists("data/sample_logins.json"):
        logs = generate_logins(3000)
        inject_failed_logins(logs, 15)
        inject_location_switches(logs, 20)
        inject_multi_ip_usage(logs, 20)
        logs.sort(key=lambda x: x['timestamp'])

        with open("data/sample_logins.json", "w") as f:
            json.dump(logs, f, indent=2)

    if not os.path.exists("data/net_sentinel.db"):
        load_data()

    return app
