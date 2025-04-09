# 🧼 Car Wash Booking System

A web-based application to manage car wash bookings with an admin dashboard, calendar scheduling, and real-time booking management.

---

## 🚀 Features

- 📅 **FullCalendar integration** for visual scheduling
- 🧍 **User Booking Form**: Customers enter car plate, name, car type, contact number, wash type, date, and time
- 🧑‍💼 **Admin Panel**:
  - View bookings in calendar or list mode
  - Mark bookings as **Attended** ✅ or **No Show** ❌
  - Status shown with color coding and strikethrough on the calendar
- 🔎 **Filter, Search, Sort, and Pagination** on the admin booking list
- 🔒 Admin authentication (login & registration)
- 💾 Uses **SQLite** for persistent data storage
- 🧱 Follows **Flask Application Factory** and **Blueprints** for modular architecture

---

## 🧰 Tech Stack

- **Backend**: Flask + Flask-Login + SQLAlchemy + Flask-Migrate
- **Frontend**: Bootstrap 5, HTMX, FullCalendar
- **Database**: SQLite (file-based, portable)
- **Structure**: Application Factory + Blueprints

---

## 📁 Project Structure
```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── db.py
│   ├── forms.py
│   ├── models.py
│   ├── static
│   │   ├── bootstrap.bundle.js
│   │   ├── bootstrap.css
│   │   ├── img
│   │   │   └── ourodev.png
│   │   ├── index.global.js
│   │   ├── index.global.min.js
│   │   ├── script.js
│   │   └── styles.css
│   ├── templates
│   │   ├── admin.html
│   │   ├── admin_base.html
│   │   ├── base.html
│   │   ├── booking_form.html
│   │   ├── calendar.html
│   │   ├── delete_booking.html
│   │   ├── edit_booking.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   └── register.html
│   └── views
│       ├── __pycache__
│       ├── admin.py
│       └── main.py
├── config.py
├── instance
├── migrations
│   ├── README
│   ├── __pycache__
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 40f3fc9f6606_initial_migration.py
│       └── __pycache__
├── populate_db.py
├── requirement.txt
└── run.py
```

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/car-wash-app.git
cd car-wash-app
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

### 5. Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the App
```bash
flask run
```

## 🔐 Admin Access

    - Register via /admin/register

    - Then login at /admin/login

    - Access the dashboard via:

       - /admin/calendar (FullCalendar)

       - /admin/dashboard (Booking list)

## 🧪 Development Notes

    - Wash durations are defined in WASH_DURATIONS

    - Admin panel uses vertical sidebar for navigation

    - Calendar is fully interactive (click to edit, see status visually)

## 👤 Author

OuroDev
