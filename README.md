# NetSentinel

NetSentinel is a lightweight, full-stack web application that simulates login activity and detects suspicious behavior using rule-based anomaly detection. Designed as a CS50 Final Project, it's ideal for showcasing backend logic, frontend visualizations, and real-time data simulation.

---

## 🚀 Features

* 🔐 Login system (admin1 / admin2)
* 📈 Anomaly Dashboard with bar + line charts
* 🛠 Customizable detection rules (UI based)
* 👤 Top offending users overview
* 🧪 Simulated login data with injected anomalies
* 💾 SQLite-backed data store
* 🎨 Bootstrap-based responsive UI

---

## 🛠 Technologies Used

* Python + Flask (Backend)
* SQLite (Database)
* Chart.js (Frontend Visualizations)
* Bootstrap 5 (UI)
* JavaScript + Jinja2 (Templating)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/netsentinel.git
cd netsentinel
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
flask run
```

Then visit: `http://127.0.0.1:5000`

---

## 👤 Default Users

| Username | Password    |
| -------- | ----------- |
| admin1   | password123 |
| admin2   | adminpass   |

---

## 📊 Detection Rules

* Too many failed logins
* Location change within 1 hour
* Multiple IPs within 1 hour
* Login during abnormal hours

Rules are customizable via the homepage.

---

## 📸 Screenshots

*Insert screenshots of anomalies dashboard, login screen, homepage config UI, etc.*

---

## 🎥 CS50 Demo Video

*Insert YouTube link when available.*

---

## 🌐 Optional: Deploying to Render

1. Add `render.yaml` or `Procfile`
2. Push to GitHub
3. Create a new Web Service on [Render](https://render.com)
4. Set environment: `FLASK_APP=run.py`, `FLASK_ENV=production`

---

## 🧠 Author

Built by Dominicus Adjie Wicaksono as part of the CS50 Final Project.
