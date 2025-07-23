from models import User, UserIn
from typing import List, Optional
from database import get_connection

def create_user(user_in: UserIn) -> User:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, position) VALUES (?, ?, ?)",
        (user_in.name, user_in.email, user_in.position)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return User(id=user_id, **user_in.dict())

def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return [User(**row) for row in rows]

def get_user(user_id: int) -> Optional[User]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return User(**row) if row else None

def update_user(user_id: int, user_in: UserIn) -> Optional[User]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, email = ?, position = ? WHERE id = ?",
        (user_in.name, user_in.email, user_in.position, user_id)
    )
    conn.commit()
    conn.close()
    return get_user(user_id)

def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
