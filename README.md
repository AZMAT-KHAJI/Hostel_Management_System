<div align="center">

# 🏨 Hostel Management System

**A full-stack web application built with Django to digitize and streamline hostel operations.**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-Backend-green?style=flat-square&logo=django)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## 📖 Overview

The **Hostel Management System** replaces error-prone manual processes with a centralized digital platform for hostel administrators and students alike. It automates key hostel workflows — from student onboarding to fee receipt generation — ensuring better efficiency, transparency, and scalability.

---

## ✨ Features

### 👨‍🎓 Student Module
- Secure registration and login
- Personal dashboard with profile information
- Room request and room change functionality
- Complaint submission and real-time tracking
- Fee payment management
- Downloadable fee receipts in PDF format

### 🏢 Admin Module
- Secure access via Django Admin Panel
- Full student record management
- Approve / reject room allocation requests
- Handle and resolve student complaints
- Monitor and verify fee payments
- Complete control over hostel operations

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Frontend | HTML, CSS |
| Database | SQLite (default Django DB) |
| Authentication | Django built-in auth system |
| PDF Generation | ReportLab / Django utilities |

---

## 🗂️ Project Structure

```
Hostel_Management_System/
│
├── hostel/            # Core app — models, views, business logic
├── hostel_mgmt/       # Project config — settings.py, urls.py
├── templates/         # HTML templates
├── static/            # CSS and static assets
├── manage.py          # Django entry point
└── db.sqlite3         # SQLite database (git-ignored)
```

---

## ⚙️ Getting Started


### Installation

```bash
# 1. Clone the repository
git clone https://github.com/AZMAT-KHAJI/Hostel_Management_System.git
cd Hostel_Management_System

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install django

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (admin account)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

---

## 🌐 Application URLs

| Page | URL |
|---|---|
| Home | http://127.0.0.1:8000/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |

---

## 🚀 Future Enhancements

- [ ] Mobile-responsive UI
- [ ] Payment gateway integration
- [ ] Email / SMS notifications
- [ ] Enhanced dashboard analytics
- [ ] UI/UX redesign

---

## 👨‍💻 Developers

| Name | GitHub |
|---|---|
| Azmat Khaji | [@AZMAT-KHAJI](https://github.com/AZMAT-KHAJI) |
| Chaithanya R | [@Chaithanya](https://github.com/ChaithanyaGowda2005) |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
