import sqlite3
import random
from passlib.hash import bcrypt
import smtplib
from email.mime.text import MIMEText

DB_NAME = "app.db"

# --- DB Connection ---
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# --- One-time Schema Setup ---
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT,
            is_verified INTEGER DEFAULT 0,
            otp TEXT
        )
    """)
    conn.commit()
    conn.close()


# --- OTP Generation ---
def generate_otp():
    return str(random.randint(100000, 999999))


# --- Email Sending ---
def send_otp_email(to_email: str, otp: str):
    sender_email = "redmi10miui13@gmail.com"
    sender_password = "opvb posk drfz cxit"

    message = MIMEText(f"Your OTP for admin verification is: {otp}")
    message["Subject"] = "Login OTP Verification"
    message["From"] = sender_email
    message["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
    except Exception as e:
        print("Email failed:", e)


# --- Admin Registration ---
def register_admin(username: str, password: str, email: str) -> bool:
    hashed = bcrypt.hash(password)
    otp = generate_otp()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO admins (username, password_hash, email, is_verified, otp)
            VALUES (?, ?, ?, 0, ?)
        """, (username, hashed, email, otp))
        conn.commit()
        conn.close()  # ✅ Close DB FIRST

        send_otp_email(email, otp)  # ✅ THEN sends email
        return True
    except sqlite3.IntegrityError:
        return False


# --- Admin Login Check ---
def verify_admin(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, is_verified FROM admins WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash, is_verified = result
        if is_verified and bcrypt.verify(password, stored_hash):
            return True
    return False



# --- OTP Verification ---
def verify_admin_otp(username: str, otp: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT otp FROM admins WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and result[0] == otp:
        cursor.execute("""
            UPDATE admins SET is_verified = 1, otp = NULL WHERE username = ?
        """, (username,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_admin_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email FROM admins WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"username": row[0], "email": row[1]}
    return None

def update_admin_email(username: str, new_email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE admins SET email = ? WHERE username = ?", (new_email, username))
    conn.commit()
    conn.close()

def change_admin_password(username: str, current_password: str, new_password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return False
    stored_hash = result[0]
    if not bcrypt.verify(current_password, stored_hash):
        conn.close()
        return False

    new_hash = bcrypt.hash(new_password)
    cursor.execute("UPDATE admins SET password_hash = ? WHERE username = ?", (new_hash, username))
    conn.commit()
    conn.close()
    return True
  
