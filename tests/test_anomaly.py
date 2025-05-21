from app.anomaly import load_logins, detect_anomalies

logins = load_logins('data/sample_logins.json')
anomalies = detect_anomalies(logins)

for a in anomalies:
    print(a)
