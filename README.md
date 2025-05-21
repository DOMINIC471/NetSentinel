# NetSentinel
#### Video Demo: [https://youtu.be/MAOYZP5TNDk](https://youtu.be/MAOYZP5TNDk)
#### Live Demo: [https://netsentinel-production.up.railway.app](https://netsentinel-production.up.railway.app)

---

## 📝 Description

NetSentinel is a web-based anomaly detection dashboard that simulates user login activity and flags suspicious behavior based on customizable rule thresholds. Designed for CS50’s Final Project, it showcases full-stack web development with real-time visualization and simulated backend analytics.

The app supports user login, anomaly monitoring, chart-based analytics, and custom rule configuration. Users can explore anomalies like multiple failed login attempts, rapid location changes, login from multiple IPs, and activity during abnormal hours. The system uses rule-based logic to detect these anomalies from simulated data.

---

## 📂 File Overview

- `run.py` – Entry point that initializes and runs the Flask app.
- `app/__init__.py` – Application factory that sets up routing, session, and templates.
- `app/routes.py` – Contains all route handlers for UI views, API endpoints, login, logout, and rule management.
- `app/anomaly.py` – Core logic to detect anomalies using rule-based methods based on time, IP, location, and login outcomes.
- `templates/` – Jinja2 HTML templates for login, home, and anomalies dashboard.
- `static/css/style.css` – Custom UI enhancements for cards, table striping, and theme.
- `utils/simulate_logins.py` – Generates simulated login data with injected anomalies (location switches, IP usage, failed logins).
- `utils/load_json_to_db.py` – Loads JSON logins into an SQLite database.
- `data/` – Stores the SQLite database, rules config, and user list in JSON.

---

## 🔐 Login System

The app features a simple authentication system with two pre-defined users stored in a local JSON file (`data/users.json`):

| Username | Password    |
|----------|-------------|
| admin1   | password123 |
| admin2   | adminpass   |

If incorrect credentials are entered, an error message is shown and access is denied.

---

## 🏠 Home Dashboard

Upon login, users are taken to the dashboard with:

- **Top Offending Users** – Highlights users with the most anomalies.
- **Anomaly Summary** – Pie chart of anomalies grouped by rule type.
- **Detection Rule Settings** – UI form to adjust sensitivity for each rule:
  - Max failed logins
  - Time window for location/IP change
  - Abnormal hours (UTC)
  - Countries to ignore (e.g. US, UK)

There is also a quick link to jump to the anomaly dashboard.

---

## 📊 Anomalies Dashboard

On the Anomalies page, the following features are displayed:

- **Bar chart** – Color-coded anomaly frequency by type.
- **Line chart** – Login activity over time.
- **Detailed anomaly table** – Showing timestamp, user, IP, rule, and transitions (`from` / `to`).

The anomaly detection is powered by rule logic in `anomaly.py`, processed live from SQLite data.

---

## 🔄 Regenerate Data

A navigation option allows users to **regenerate synthetic login data**, which injects:
- Random login events (~3000 entries)
- Configurable number of anomaly events

This keeps the visualization fresh and testable.

---

## 🚪 Logout

Secure session-based login is used. Logging out clears the session and returns the user to the login page.

---

## ⚙️ Tech Stack

- **Backend**: Python, Flask, SQLite
- **Frontend**: Bootstrap 5, Chart.js, Jinja2, JavaScript
- **Hosting**: [Railway](https://railway.app) – free 24/7 deployment

---

## ⚙️ Local Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/DOMINIC471/NetSentinel.git
cd NetSentinel

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run locally
flask run
