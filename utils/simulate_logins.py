import json
import random
from datetime import datetime, timedelta, timezone

usernames = [f"user{i}" for i in range(1, 21)]
locations = ['US', 'UK', 'DE', 'IN', 'CN', 'RU', 'JP', 'BR']
ip_bases = ['192.168.1.', '10.0.0.', '172.16.0.']

def random_ip():
    return random.choice(ip_bases) + str(random.randint(1, 254))

def generate_logins(num_entries):
    logs = []
    now = datetime.now(timezone.utc)

    for _ in range(num_entries):
        user = random.choice(usernames)
        location = random.choices(
            ['US', 'UK', 'DE', 'IN', 'CN', 'RU'], weights=[0.3, 0.2, 0.15, 0.15, 0.1, 0.1]
        )[0]
        ip = random_ip()
        timestamp = (now - timedelta(minutes=random.randint(0, 1440))).isoformat()

        # 2% abnormal hour logins
        if random.random() < 0.02:
            timestamp = (now - timedelta(minutes=random.randint(0, 30))).replace(hour=random.choice([2, 3])).isoformat()

        # 5% fail login rate
        success = random.random() > 0.05

        logs.append({
            "timestamp": timestamp,
            "username": user,
            "ip_address": ip,
            "location": location,
            "success": success
        })

    return logs

def inject_failed_logins(logs, count):
    now = datetime.now(timezone.utc)
    for _ in range(count):
        user = random.choice(usernames)
        for i in range(6):
            logs.append({
                "timestamp": (now - timedelta(minutes=random.randint(0, 10))).isoformat(),
                "username": user,
                "ip_address": random_ip(),
                "location": "US",
                "success": False
            })

def inject_location_switches(logs, count):
    now = datetime.now(timezone.utc)
    for _ in range(count):
        user = random.choice(usernames)
        base_time = now - timedelta(minutes=random.randint(0, 60))
        logs.append({
            "timestamp": base_time.isoformat(),
            "username": user,
            "ip_address": random_ip(),
            "location": "US",
            "success": True
        })
        logs.append({
            "timestamp": (base_time + timedelta(minutes=30)).isoformat(),
            "username": user,
            "ip_address": random_ip(),
            "location": "CN",
            "success": True
        })

def inject_multi_ip_usage(logs, count):
    now = datetime.now(timezone.utc)
    for _ in range(count):
        user = random.choice(usernames)
        base_time = now - timedelta(minutes=random.randint(0, 60))
        for i in range(3):
            logs.append({
                "timestamp": (base_time + timedelta(minutes=i * 10)).isoformat(),
                "username": user,
                "ip_address": random_ip(),
                "location": "UK",
                "success": True
            })

if __name__ == "__main__":
    # Randomize counts
    total_logins = random.randint(2800, 3500)
    failed_bursts = random.randint(10, 20)
    location_changes = random.randint(15, 30)
    multi_ip_cases = random.randint(15, 30)

    logs = generate_logins(total_logins)

    inject_failed_logins(logs, failed_bursts)
    inject_location_switches(logs, location_changes)
    inject_multi_ip_usage(logs, multi_ip_cases)

    # Sort by time
    logs.sort(key=lambda x: x['timestamp'])

    with open('data/sample_logins.json', 'w') as f:
        json.dump(logs, f, indent=2)
