# 👥 User Management System – FastAPI

A secure and responsive web-based user management system built with **FastAPI**, designed for admin control over user records, including registration with OTP verification, login/logout, profile management, and CRUD operations for users.  
🔗 **Live demo**: [user-management-lmnk.onrender.com](https://user-management-lmnk.onrender.com)

---

## 🚀 Features

- 🔐 Admin registration with email OTP verification  
- 🔑 Secure admin login/logout using session cookies  
- 👤 Admin profile view and password/email update  
- ➕ Add new users with password & Gmail validation  
- 📝 Edit user details  
- ❌ Delete users  
- 👁️ View user details  
- 📱 Fully mobile responsive UI  
- 🔒 Passwords stored using bcrypt hashing  
- 📧 OTP email support using Gmail SMTP

---

## 🛠️ Built With

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), Uvicorn  
- **Frontend**: HTML5, CSS3, Jinja2 Templates  
- **Database**: SQLite  
- **Security**: bcrypt (password hashing), OTP verification  
- **Deployment**: [Render](https://render.com/)

---

## 🧑‍💻 How to Run Locally

1. **Clone the Repo**
   ```bash
   git clone https://github.com/Kishore1407/User-management.git
   cd User-management
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```bash
   uvicorn main:app --reload
   ```

4. Open your browser and go to:
   ```
   http://127.0.0.1:8000
   ```

---

## 🌐 Deployment (Render)

Already deployed on [Render](https://render.com/).  
To deploy manually:

- Create new Web Service
- Set build command:  
  ```bash
  pip install -r requirements.txt
  ```
- Set start command:  
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- Add environment variables if needed

---

## 🔐 Environment Variables (for Email OTP)

Create a `.env` file or set in Render dashboard:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

---

## 📁 Project Structure

```
.
├── main.py
├── auth_db.py
├── crud.py
├── models.py
├── utils.py
├── static/
│   └── style.css
├── templates/
│   └── *.html
├── requirements.txt
└── README.md
```

---

## ✨ Future Enhancements

- ✅ Add pagination & search filters
- ✅ Export user data to Excel/PDF
- 🚧 Dark mode support
- 🚧 REST API access (with Swagger docs)

---

## 🤝 Contributions

All contributions, issues, and suggestions are welcome!  
Feel free to fork the repository and submit a pull request.

---

## 📬 Contact

Made with ❤️ by **Kishore**  
🔗 [GitHub Profile](https://github.com/Kishore1407)
