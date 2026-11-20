# Django SMS Gateway Application

A web-based SMS application built with Django, Bootstrap 5, and the TextBee REST API. This application allows users to send SMS messages to Philippine numbers (`+639...`), validate input formats, track character limits and SMS segments in real time, and view historical sending logs stored in a local SQLite database.

---

## 📌 Project Overview

* **Course:** IT 120 – Integrative Programming and Technologies
* **Academic Term:** 1st Semester, SY 2026–2027
* **Author / Developer:** Benedict Leyros
* **SMS Gateway Service:** TextBee REST API (`textbee.dev`) via Android Gateway Device

---

## ✨ Features

1. **SMS Sending Gateway Integration:** Integrates with TextBee's REST API using Python's `requests` library to transmit messages through an Android gateway device.
2. **Strict E.164 Input Validation:** Validates recipient phone numbers using Django Forms regex patterns (`^\+639\d{9}$`) to ensure proper international format before making API calls.
3. **Live Character & Segment Counter:** Provides real-time feedback using JavaScript, dynamically calculating character counts out of 160 and estimating the required SMS segment count as the user types.
4. **SMS History Dashboard:** Displays a history log table of recent sending attempts retrieved from Django's SQLite database (`SMSLog` model), showing recipient, message preview, timestamp, status badge (`Submitted` / `Failed`), and batch provider ID.
5. **Robust Error Handling:** Safely captures and displays API failures, network exceptions, and validation errors without crashing the application.
6. **Secure Secret Management:** Protects API keys using environment variables (`.env`) loaded via `python-dotenv`, keeping sensitive credentials out of version control.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Django 5.x
* **Frontend:** HTML5, Bootstrap 5 (CDN), Vanilla JavaScript
* **Database:** SQLite (Django default ORM)
* **API Integration:** TextBee REST API (`https://api.textbee.dev/api/v1/gateway/send-sms`)
* **HTTP Client:** `requests`
* **Environment Management:** `python-dotenv`

---

## 🔒 Security & Environment Setup

This project uses `python-dotenv` to isolate sensitive credentials. The actual `.env` file containing secrets is strictly excluded from version control via `.gitignore`.

### 1. `.env` File (Local Only - NEVER commit to Git)
Create a file named `.env` in the root directory (next to `manage.py`):

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
TEXTBEE_API_KEY=txb_your_actual_textbee_api_key_here
```

### 2. `.env.example` File (Committed to Git)
A safe template file provided for reference:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
TEXTBEE_API_KEY=your_textbee_api_key_here
```

---

## 🚀 Installation & Local Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/django-sms-app.git
cd django-sms-app
```

### Step 2: Create and Activate Virtual Environment
* **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory matching the format shown in `.env.example`, and insert your valid `TEXTBEE_API_KEY`.

### Step 5: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Start the Django Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your web browser.

---

## 🧪 Testing Procedures & Results

The application was tested against key test scenarios to ensure stability and user feedback accuracy:

| Test Case ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Empty Form Submission | Django form validation fails; displays field-level error messages. | Form prevented submission; red error alert displayed. | **PASS** |
| **TC-02** | Invalid Phone Format (`0917...`) | Regex validator rejects number; requires `+639...` format. | Rejected with clear message: *"Phone number must start with +639 followed by 9 digits."* | **PASS** |
| **TC-03** | Character Counter Test | JS counter updates character count and segment calculation in real time. | Counter accurately updated as characters were typed/deleted. | **PASS** |
| **TC-04** | Valid SMS Submission | API returns HTTP 200/201; green success banner with Batch ID displayed; DB log created with `Submitted` status. | SMS queued on gateway phone; green alert shown; log entry added to history table. | **PASS** |
| **TC-05** | Missing API Key | View catches missing settings; creates `Failed` DB log entry without making HTTP request. | Failed gracefully with alert: *"SMS service is not properly configured."* | **PASS** |
| **TC-06** | Invalid Provider Credentials | Provider returns HTTP error (e.g., 401/403); error detail captured safely in database log. | App remained stable; red error banner rendered with safe provider message. | **PASS** |

---

## 📂 Project Structure

```text
django-sms-app/
├── sms_project/            # Project configuration folder
│   ├── __init__.py
│   ├── settings.py         # Loads environment variables via dotenv
│   ├── urls.py             # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
├── sms_app/                # Main application folder
│   ├── migrations/         # Database migrations
│   ├── templates/
│   │   └── sms_app/
│   │       └── index.html  # Main Bootstrap UI with live counter & history table
│   ├── __init__.py
│   ├── admin.py            # Admin registrations for SMSLog
│   ├── apps.py
│   ├── forms.py            # SMSForm with E.164 phone number validation
│   ├── models.py           # SMSLog database model
│   ├── urls.py             # App URL routing
│   └── views.py            # Request handler & TextBee API integration logic
├── .env                    # Local secrets (ignored by Git)
├── .env.example            # Environment template for repository
├── .gitignore              # Git ignore file (excludes .env, venv/, __pycache__)
├── manage.py               # Django CLI utility
├── README.md               # Project documentation
└── requirements.txt        # Python package dependencies
```

---

## ⚠️ Known Limitations

* **Gateway Device Dependency:** Delivery relies on the Android device running the TextBee app having active network connectivity and cellular signal/SMS balance.
* **Carrier Delays:** Message submission status (`Submitted`) confirms placement into the gateway queue; final delivery to recipient handsets depends on local telecom networks (Globe/Smart/DITO).

---

## 👥 Authors & Acknowledgments

* **Benedict Leyros** — Full Stack Development (Django Models, Forms, Views, Bootstrap 5 UI, TextBee API Integration, Testing, Documentation).