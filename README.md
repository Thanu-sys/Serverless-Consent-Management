# Consent Management System

A modern, full-stack consent management application with a Flask backend API and React frontend. Features GDPR-compliant consent collection, real-time analytics, and a beautiful, responsive UI.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js 14+

### 1. Start the Backend
```sh
cd backend
python -m venv venv
# Activate venv, then:
pip install -r requirements.txt
python test_local.py
```
Backend runs at: http://localhost:5001

### 2. Start the Frontend
```sh
cd frontend
npm install
npm start
```
Frontend runs at: http://localhost:3000

---

## 🎨 Features
- **GDPR-compliant Cookie Consent Banner**
- **Granular Consent Management** (individual & bulk)
- **Real-time Analytics Dashboard**
- **Mobile Responsive & Modern UI**
- **RESTful API** for easy integration

---

## 🛠️ Technology Stack
- **Frontend:** React 18, JavaScript, CSS3, Axios
- **Backend:** Python, Flask, SQLAlchemy, SQLite/PostgreSQL
- **Design:** Responsive, Glass Morphism, CSS Animations

---

## 📁 Project Structure
```
hackthon/
├── backend/
│   ├── app.py
│   ├── test_local.py
│   ├── create_db.py
│   ├── seed_data.py
│   ├── requirements.txt
│   ├── README.md
│   ├── API_DOCUMENTATION.md
│   ├── start_server.py
│   ├── test_api.py
│   ├── test_connection.py
│   ├── serverless.yml
│   └── instance/
│       └── test_consent.db
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── favicon.ico
│   ├── package.json
│   ├── package-lock.json
│   └── README.md
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License. 