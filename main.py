import os
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import get_username_from_token
from models import UserIn
from crud import create_user, get_users, get_user, update_user, delete_user
from auth_db import (
    verify_admin,
    register_admin,
    verify_admin_otp,
    init_db,
    get_admin_by_username, 
    update_admin_email, 
    change_admin_password
)
from utils import create_session_token, verify_session_token
import uvicorn

app = FastAPI()

# --- Startup: DB Setup ---
init_db()

# --- Static & Template Setup ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Session Helper ---
def is_logged_in(request: Request) -> bool:
    token = request.cookies.get("session_token")
    return verify_session_token(token) if token else False

# ------------------ ROUTES ------------------

@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse("/dashboard", status_code=307)

# --- Login ---
@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None, "show_navbar": False})

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if verify_admin(username, password):
        token = create_session_token(username)
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie("session_token", token, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid or unverified credentials", "show_navbar": False})

# --- Logout ---
@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session_token")
    return response

# --- Register ---
@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None, "show_navbar": False})

@app.post("/register", response_class=HTMLResponse)
def register_post(request: Request, username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    if register_admin(username, password, email):
        return RedirectResponse("/verify-otp", status_code=303)
    return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists", "show_navbar": False})

# --- OTP Verification ---
@app.get("/verify-otp", response_class=HTMLResponse)
def otp_get(request: Request):
    return templates.TemplateResponse("verify_otp.html", {"request": request, "error": None, "show_navbar": False})

@app.post("/verify-otp", response_class=HTMLResponse)
def otp_post(request: Request, username: str = Form(...), otp: str = Form(...)):
    if verify_admin_otp(username, otp):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("verify_otp.html", {"request": request, "error": "Invalid OTP", "show_navbar": False})

# --- Dashboard ---
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    token = request.cookies.get("session_token")
    if not token or not verify_session_token(token):
        return RedirectResponse("/login")
    username = get_username_from_token(token)
    users = get_users()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "users": users,
        "username": username,
        "show_navbar": True
    })

#---View profile---
@app.get("/profile", response_class=HTMLResponse)
def view_profile(request: Request):
    token = request.cookies.get("session_token")
    if not token or not verify_session_token(token):
        return RedirectResponse("/login")
    username = get_username_from_token(token)
    admin = get_admin_by_username(username)
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "username": admin['username'],
        "email": admin['email'],
        "show_navbar": True
    })


@app.post("/profile/update")
def update_email(request: Request, email: str = Form(...)):
    token = request.cookies.get("session_token")
    username = get_username_from_token(token)
    update_admin_email(username, email)
    return RedirectResponse("/profile", status_code=303)


@app.post("/profile/change-password")
def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    token = request.cookies.get("session_token")
    username = get_username_from_token(token)
    if new_password != confirm_password:
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "username": username,
            "email": get_admin_by_username(username)['email'],
            "error": "Passwords do not match",
            "show_navbar": True
        })
    success = change_admin_password(username, current_password, new_password)
    if not success:
        return templates.TemplateResponse("profile.html", {
            "request": request,
            "username": username,
            "email": get_admin_by_username(username)['email'],
            "error": "Incorrect current password",
            "show_navbar": True
        })
    return RedirectResponse("/profile", status_code=303)


# --- Run Server ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's port or default to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port)

