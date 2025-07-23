## 🛠️ User Management System

This is a simple Admin Dashboard project built with **FastAPI**, **Jinja2 templates**, and **SQLite**, allowing admin users to:

- Register and log in
- Verify OTP via email
- Perform full CRUD operations on users
- Manage admin profile and password securely

Live Demo: [🔗 Hosted on Render](https://user-management-d3ta.onrender.com)

---

## 🚀 Features

- 🔐 Admin registration, login & logout
- ✉️ OTP verification via email
- 👤 Admin profile page with email/password update
- 📋 Add, edit, view, and delete users
- 🧩 Session-based authentication with cookies
- 🎨 Responsive UI with pure HTML + CSS (no JS)
- 📦 SQLite for lightweight database needs

---

## 🖥️ Tech Stack

| Layer        | Technology             |
|--------------|-------------------------|
| Backend      | FastAPI                 |
| Frontend     | Jinja2 Templates + CSS  |
| Database     | SQLite + SQLAlchemy     |
| Authentication | OTP + Session Cookies |
| Deployment   | Render (Free Tier)      |


---

## 🛠️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/Kishore1407/User-management.git
cd User-management

# 2. Create virtual env (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python main.py

